"""
Advanced API Tester Agent - Production Grade
A Postman alternative powered by AI and LangGraph
"""

import asyncio
import json
import logging
import os
import statistics
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict, Annotated

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import StateGraph, END
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, HttpUrl, validator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI app initialization
app = FastAPI(
    title="Advanced API Tester Agent",
    description="AI-Powered API Testing Tool - Postman Alternative",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================================================
# PYDANTIC MODELS
# ========================================================================

class HTTPMethod(str, Enum):
    """Supported HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class TestConfig(BaseModel):
    """Structured test configuration"""
    name: str = Field(..., description="Test case name")
    method: HTTPMethod = Field(..., description="HTTP method")
    url: HttpUrl = Field(..., description="Target URL")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = Field(default=None)
    auth: Optional[Dict[str, str]] = Field(default=None)
    expected_status: Optional[int] = Field(default=None)
    expected_contains: Optional[List[str]] = Field(default_factory=list)
    expected_not_contains: Optional[List[str]] = Field(default_factory=list)
    timeout: int = Field(default=30, ge=1, le=300)


class NaturalLanguageRequest(BaseModel):
    """Natural language test request"""
    instruction: str = Field(..., description="Natural language test instruction")
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context (base_url, auth, etc.)"
    )


class LoadTestRequest(BaseModel):
    """Load testing request"""
    test_config: TestConfig
    iterations: int = Field(default=10, ge=1, le=1000)
    concurrent: bool = Field(default=False)


class TestResult(BaseModel):
    """Test execution result"""
    success: bool
    status_code: Optional[int] = None
    response_time_ms: float
    response_body: Optional[Any] = None
    response_headers: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    validations: List[Dict[str, Any]] = Field(default_factory=list)
    ai_analysis: Optional[str] = None


class LoadTestResult(BaseModel):
    """Load test result"""
    total_requests: int
    successful: int
    failed: int
    min_time_ms: float
    max_time_ms: float
    avg_time_ms: float
    median_time_ms: float
    std_dev_ms: float
    requests_per_second: float
    ai_performance_analysis: Optional[str] = None


# ========================================================================
# LANGGRAPH STATE DEFINITION
# ========================================================================

class AgentState(TypedDict):
    """State passed through the agent workflow"""
    # Input
    raw_input: Optional[str]
    test_config: Optional[Dict[str, Any]]
    context: Dict[str, Any]
    
    # Processing
    parsed_config: Optional[TestConfig]
    validation_errors: List[str]
    
    # Execution
    http_response: Optional[httpx.Response]
    execution_time_ms: float
    execution_error: Optional[str]
    
    # Analysis
    analysis_results: Dict[str, Any]
    ai_insights: str
    bug_fixes: List[str]
    
    # Output
    final_result: Optional[TestResult]
    generated_tests: List[TestConfig]


# ========================================================================
# AI HELPER FUNCTIONS
# ========================================================================

async def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    response_format: Optional[Dict[str, str]] = None
) -> str:
    """
    Call OpenAI LLM with robust error handling
    
    Args:
        system_prompt: System instruction
        user_prompt: User message
        model: Model identifier
        temperature: Sampling temperature
        response_format: Optional response format (e.g., {"type": "json_object"})
    
    Returns:
        LLM response text
    """
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        return f"AI analysis unavailable: {str(e)}"


async def parse_natural_language_to_config(instruction: str, context: Dict[str, Any]) -> TestConfig:
    """
    Convert natural language instruction to structured TestConfig using AI
    
    Args:
        instruction: Natural language test description
        context: Additional context like base_url, auth tokens
    
    Returns:
        Parsed TestConfig object
    """
    system_prompt = """You are an expert API testing assistant. Convert natural language test instructions into structured JSON test configurations.

Output ONLY valid JSON with this exact structure:
{
  "name": "descriptive test name",
  "method": "GET|POST|PUT|PATCH|DELETE",
  "url": "complete URL",
  "headers": {"key": "value"},
  "params": {"key": "value"},
  "body": {"key": "value"} or null,
  "expected_status": 200,
  "expected_contains": ["field1", "field2"],
  "expected_not_contains": ["error"],
  "timeout": 30
}

Rules:
- Infer method from verbs (get/fetch=GET, create/post=POST, update=PUT/PATCH, delete/remove=DELETE)
- Build complete URLs from context
- Extract query params, headers, body from instruction
- Set realistic expectations
- Handle auth tokens from context"""

    user_prompt = f"""Instruction: {instruction}

Context: {json.dumps(context, indent=2)}

Convert to JSON test config:"""

    try:
        response = await call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        config_dict = json.loads(response)
        return TestConfig(**config_dict)
    
    except Exception as e:
        logger.error(f"Failed to parse natural language: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not parse instruction: {str(e)}"
        )


async def analyze_api_response(
    test_config: TestConfig,
    response: Optional[httpx.Response],
    execution_error: Optional[str],
    execution_time_ms: float
) -> Dict[str, Any]:
    """
    Deep AI-powered analysis of API response
    
    Args:
        test_config: Original test configuration
        response: HTTP response object
        execution_error: Any execution error
        execution_time_ms: Response time
    
    Returns:
        Analysis dictionary with insights and suggestions
    """
    if execution_error:
        system_prompt = """You are an expert API debugging assistant. Analyze API execution errors and provide:
1. Root cause explanation
2. Specific backend code fixes
3. Security considerations
4. Best practices

Be concise but actionable."""

        user_prompt = f"""API Test Failed:

Request:
- Method: {test_config.method}
- URL: {test_config.url}
- Headers: {json.dumps(test_config.headers)}
- Body: {json.dumps(test_config.body)}

Error: {execution_error}

Provide debugging analysis:"""

        ai_analysis = await call_llm(system_prompt, user_prompt, temperature=0.4)
        
        return {
            "success": False,
            "error_analysis": ai_analysis,
            "suggestions": ["Check network connectivity", "Verify URL correctness", "Validate auth tokens"]
        }
    
    # Analyze successful response
    status_code = response.status_code if response else None
    
    try:
        response_body = response.json() if response else None
    except:
        response_body = response.text if response else None
    
    system_prompt = """You are an expert API response analyst. Analyze API responses and provide:
1. Response structure analysis
2. Data quality assessment
3. Security observations
4. Performance evaluation
5. Potential issues or improvements

Be specific and actionable."""

    user_prompt = f"""API Response Analysis:

Request:
- Method: {test_config.method}
- URL: {test_config.url}
- Expected Status: {test_config.expected_status}

Response:
- Status Code: {status_code}
- Response Time: {execution_time_ms}ms
- Body: {json.dumps(response_body, indent=2) if response_body else 'No body'}

Expected Contains: {test_config.expected_contains}
Expected NOT Contains: {test_config.expected_not_contains}

Provide detailed analysis:"""

    ai_analysis = await call_llm(system_prompt, user_prompt, temperature=0.5)
    
    # Validate expectations
    validations = []
    
    if test_config.expected_status and status_code != test_config.expected_status:
        validations.append({
            "type": "status_code_mismatch",
            "expected": test_config.expected_status,
            "actual": status_code,
            "passed": False
        })
    
    response_text = json.dumps(response_body) if response_body else ""
    
    for field in test_config.expected_contains:
        found = field in response_text
        validations.append({
            "type": "contains_check",
            "field": field,
            "passed": found
        })
    
    for field in test_config.expected_not_contains:
        found = field in response_text
        validations.append({
            "type": "not_contains_check",
            "field": field,
            "passed": not found
        })
    
    return {
        "success": all(v.get("passed", True) for v in validations),
        "ai_analysis": ai_analysis,
        "validations": validations,
        "response_structure": analyze_structure(response_body) if response_body else None
    }


def analyze_structure(data: Any, max_depth: int = 3) -> Dict[str, Any]:
    """
    Analyze JSON response structure
    
    Args:
        data: Response data
        max_depth: Maximum nesting depth to analyze
    
    Returns:
        Structure analysis dictionary
    """
    if isinstance(data, dict):
        return {
            "type": "object",
            "keys": list(data.keys()),
            "nested": {
                k: analyze_structure(v, max_depth - 1) 
                for k, v in list(data.items())[:5]
            } if max_depth > 0 else {}
        }
    elif isinstance(data, list):
        return {
            "type": "array",
            "length": len(data),
            "sample": analyze_structure(data[0], max_depth - 1) if data and max_depth > 0 else None
        }
    else:
        return {"type": type(data).__name__}


async def generate_test_cases(test_config: TestConfig) -> List[TestConfig]:
    """
    Generate comprehensive test cases from a base configuration using AI
    
    Args:
        test_config: Base test configuration
    
    Returns:
        List of generated test configurations
    """
    system_prompt = """You are an expert QA engineer. Generate comprehensive test cases for an API endpoint.

Create 5 test variations:
1. Happy path (valid input)
2. Invalid data test
3. Missing required fields test
4. Boundary value test
5. Security/injection test

Output ONLY a JSON array of test configs:
[{test_config1}, {test_config2}, ...]

Each config must be valid and complete."""

    user_prompt = f"""Base API Test:
{test_config.json(indent=2)}

Generate 5 comprehensive test case variations:"""

    try:
        response = await call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        
        # Parse response - handle if it's wrapped in object
        parsed = json.loads(response)
        if isinstance(parsed, dict) and "tests" in parsed:
            test_list = parsed["tests"]
        elif isinstance(parsed, dict) and "test_cases" in parsed:
            test_list = parsed["test_cases"]
        elif isinstance(parsed, list):
            test_list = parsed
        else:
            test_list = [parsed]
        
        return [TestConfig(**tc) for tc in test_list]
    
    except Exception as e:
        logger.error(f"Test generation failed: {str(e)}")
        return [test_config]  # Return original if generation fails


# ========================================================================
# LANGGRAPH NODES
# ========================================================================

async def parse_input_node(state: AgentState) -> AgentState:
    """
    Parse natural language or structured input
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with parsed configuration
    """
    logger.info("Node: ParseInput")
    
    try:
        if state.get("raw_input"):
            # Natural language input
            parsed_config = await parse_natural_language_to_config(
                instruction=state["raw_input"],
                context=state.get("context", {})
            )
            state["parsed_config"] = parsed_config
        
        elif state.get("test_config"):
            # Structured input
            state["parsed_config"] = TestConfig(**state["test_config"])
        
        else:
            state["validation_errors"] = ["No input provided"]
        
        return state
    
    except Exception as e:
        state["validation_errors"] = [str(e)]
        return state


async def validate_config_node(state: AgentState) -> AgentState:
    """
    Validate test configuration
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with validation results
    """
    logger.info("Node: ValidateConfig")
    
    errors = []
    parsed_config = state.get("parsed_config")
    
    if not parsed_config:
        errors.append("No configuration to validate")
        state["validation_errors"] = errors
        return state
    
    # URL validation
    if not str(parsed_config.url).startswith(("http://", "https://")):
        errors.append("URL must start with http:// or https://")
    
    # Body validation for methods that shouldn't have body
    if parsed_config.method in [HTTPMethod.GET, HTTPMethod.HEAD] and parsed_config.body:
        errors.append(f"{parsed_config.method} requests should not have a body")
    
    state["validation_errors"] = errors
    return state


async def execute_request_node(state: AgentState) -> AgentState:
    """
    Execute HTTP request
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with execution results
    """
    logger.info("Node: ExecuteRequest")
    
    parsed_config = state.get("parsed_config")
    
    if not parsed_config or state.get("validation_errors"):
        return state
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=parsed_config.timeout) as client:
            # Prepare request kwargs
            kwargs = {
                "method": parsed_config.method.value,
                "url": str(parsed_config.url),
                "headers": parsed_config.headers or {},
                "params": parsed_config.params or {}
            }
            
            # Add body for appropriate methods
            if parsed_config.method not in [HTTPMethod.GET, HTTPMethod.HEAD]:
                if parsed_config.body:
                    kwargs["json"] = parsed_config.body
            
            # Add authentication
            if parsed_config.auth:
                if "bearer" in parsed_config.auth:
                    kwargs["headers"]["Authorization"] = f"Bearer {parsed_config.auth['bearer']}"
                elif "basic" in parsed_config.auth:
                    kwargs["auth"] = (
                        parsed_config.auth["basic"].get("username", ""),
                        parsed_config.auth["basic"].get("password", "")
                    )
            
            # Execute request
            response = await client.request(**kwargs)
            
            execution_time_ms = (time.time() - start_time) * 1000
            
            state["http_response"] = response
            state["execution_time_ms"] = execution_time_ms
            state["execution_error"] = None
    
    except httpx.TimeoutException:
        state["execution_error"] = f"Request timeout after {parsed_config.timeout}s"
        state["execution_time_ms"] = (time.time() - start_time) * 1000
    
    except httpx.NetworkError as e:
        state["execution_error"] = f"Network error: {str(e)}"
        state["execution_time_ms"] = (time.time() - start_time) * 1000
    
    except Exception as e:
        state["execution_error"] = f"Execution error: {str(e)}"
        state["execution_time_ms"] = (time.time() - start_time) * 1000
    
    return state


async def analyze_response_node(state: AgentState) -> AgentState:
    """
    Analyze response with AI
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with analysis results
    """
    logger.info("Node: AnalyzeResponse")
    
    parsed_config = state.get("parsed_config")
    response = state.get("http_response")
    execution_error = state.get("execution_error")
    execution_time_ms = state.get("execution_time_ms", 0)
    
    analysis = await analyze_api_response(
        test_config=parsed_config,
        response=response,
        execution_error=execution_error,
        execution_time_ms=execution_time_ms
    )
    
    state["analysis_results"] = analysis
    state["ai_insights"] = analysis.get("ai_analysis", "")
    
    return state


async def generate_report_node(state: AgentState) -> AgentState:
    """
    Generate final test report
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with final result
    """
    logger.info("Node: GenerateReport")
    
    parsed_config = state.get("parsed_config")
    response = state.get("http_response")
    execution_error = state.get("execution_error")
    execution_time_ms = state.get("execution_time_ms", 0)
    analysis = state.get("analysis_results", {})
    
    # Build result
    if execution_error:
        result = TestResult(
            success=False,
            response_time_ms=execution_time_ms,
            error=execution_error,
            ai_analysis=analysis.get("error_analysis", "")
        )
    else:
        try:
            response_body = response.json() if response else None
        except:
            response_body = response.text if response else None
        
        result = TestResult(
            success=analysis.get("success", True),
            status_code=response.status_code if response else None,
            response_time_ms=execution_time_ms,
            response_body=response_body,
            response_headers=dict(response.headers) if response else None,
            validations=analysis.get("validations", []),
            ai_analysis=analysis.get("ai_analysis", "")
        )
    
    state["final_result"] = result
    return state


# ========================================================================
# LANGGRAPH WORKFLOW
# ========================================================================

def create_agent_graph() -> StateGraph:
    """
    Create the LangGraph workflow for API testing
    
    Returns:
        Compiled state graph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("parse_input", parse_input_node)
    workflow.add_node("validate_config", validate_config_node)
    workflow.add_node("execute_request", execute_request_node)
    workflow.add_node("analyze_response", analyze_response_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # Define edges
    workflow.set_entry_point("parse_input")
    workflow.add_edge("parse_input", "validate_config")
    
    # Conditional edge after validation
    def should_execute(state: AgentState) -> str:
        if state.get("validation_errors"):
            return "generate_report"
        return "execute_request"
    
    workflow.add_conditional_edges(
        "validate_config",
        should_execute,
        {
            "execute_request": "execute_request",
            "generate_report": "generate_report"
        }
    )
    
    workflow.add_edge("execute_request", "analyze_response")
    workflow.add_edge("analyze_response", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()


# Create global agent graph
agent_graph = create_agent_graph()


# ========================================================================
# FASTAPI ENDPOINTS
# ========================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "API Tester Agent",
        "version": "1.0.0"
    }


@app.post("/api/test/natural", response_model=TestResult, tags=["Testing"])
async def test_natural_language(request: NaturalLanguageRequest):
    """
    Execute API test from natural language instruction
    
    Args:
        request: Natural language test request
    
    Returns:
        Test execution result
    """
    logger.info(f"Natural language test: {request.instruction}")
    
    try:
        initial_state = AgentState(
            raw_input=request.instruction,
            test_config=None,
            context=request.context or {},
            parsed_config=None,
            validation_errors=[],
            http_response=None,
            execution_time_ms=0,
            execution_error=None,
            analysis_results={},
            ai_insights="",
            bug_fixes=[],
            final_result=None,
            generated_tests=[]
        )
        
        # Run agent graph
        final_state = await agent_graph.ainvoke(initial_state)
        
        if not final_state.get("final_result"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent failed to produce result"
            )
        
        return final_state["final_result"]
    
    except Exception as e:
        logger.error(f"Natural language test failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/test/run", response_model=TestResult, tags=["Testing"])
async def run_structured_test(test_config: TestConfig):
    """
    Execute API test from structured configuration
    
    Args:
        test_config: Structured test configuration
    
    Returns:
        Test execution result
    """
    logger.info(f"Structured test: {test_config.name}")
    
    try:
        initial_state = AgentState(
            raw_input=None,
            test_config=test_config.dict(),
            context={},
            parsed_config=None,
            validation_errors=[],
            http_response=None,
            execution_time_ms=0,
            execution_error=None,
            analysis_results={},
            ai_insights="",
            bug_fixes=[],
            final_result=None,
            generated_tests=[]
        )
        
        # Run agent graph
        final_state = await agent_graph.ainvoke(initial_state)
        
        if not final_state.get("final_result"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent failed to produce result"
            )
        
        return final_state["final_result"]
    
    except Exception as e:
        logger.error(f"Structured test failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/test/load", response_model=LoadTestResult, tags=["Load Testing"])
async def run_load_test(request: LoadTestRequest):
    """
    Execute load testing on an API endpoint
    
    Args:
        request: Load test configuration
    
    Returns:
        Load test results with performance metrics
    """
    logger.info(f"Load test: {request.test_config.name} ({request.iterations} iterations)")
    
    results = []
    successful = 0
    failed = 0
    
    async def execute_single_test():
        try:
            initial_state = AgentState(
                raw_input=None,
                test_config=request.test_config.dict(),
                context={},
                parsed_config=None,
                validation_errors=[],
                http_response=None,
                execution_time_ms=0,
                execution_error=None,
                analysis_results={},
                ai_insights="",
                bug_fixes=[],
                final_result=None,
                generated_tests=[]
            )
            
            final_state = await agent_graph.ainvoke(initial_state)
            return final_state.get("final_result")
        except:
            return None
    
    start_time = time.time()
    
    if request.concurrent:
        # Concurrent execution
        tasks = [execute_single_test() for _ in range(request.iterations)]
        test_results = await asyncio.gather(*tasks, return_exceptions=True)
    else:
        # Sequential execution
        test_results = []
        for _ in range(request.iterations):
            result = await execute_single_test()
            test_results.append(result)
    
    total_time = time.time() - start_time
    
    # Analyze results
    response_times = []
    
    for result in test_results:
        if isinstance(result, TestResult) and result:
            if result.success:
                successful += 1
            else:
                failed += 1
            response_times.append(result.response_time_ms)
        else:
            failed += 1
    
    if not response_times:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="All load test requests failed"
        )
    
    # Calculate statistics
    min_time = min(response_times)
    max_time = max(response_times)
    avg_time = statistics.mean(response_times)
    median_time = statistics.median(response_times)
    std_dev = statistics.stdev(response_times) if len(response_times) > 1 else 0
    rps = request.iterations / total_time if total_time > 0 else 0
    
    # AI performance analysis
    performance_analysis = await call_llm(
        system_prompt="You are a performance testing expert. Analyze load test results and provide insights on performance, bottlenecks, and recommendations.",
        user_prompt=f"""Load Test Results:
- Total Requests: {request.iterations}
- Successful: {successful}
- Failed: {failed}
- Min Response Time: {min_time:.2f}ms
- Max Response Time: {max_time:.2f}ms
- Avg Response Time: {avg_time:.2f}ms
- Median Response Time: {median_time:.2f}ms
- Std Deviation: {std_dev:.2f}ms
- Requests/Second: {rps:.2f}

Provide performance analysis and recommendations:""",
        temperature=0.5
    )
    
    return LoadTestResult(
        total_requests=request.iterations,
        successful=successful,
        failed=failed,
        min_time_ms=min_time,
        max_time_ms=max_time,
        avg_time_ms=avg_time,
        median_time_ms=median_time,
        std_dev_ms=std_dev,
        requests_per_second=rps,
        ai_performance_analysis=performance_analysis
    )


@app.post("/api/test/generate", response_model=List[TestConfig], tags=["Test Generation"])
async def generate_tests(test_config: TestConfig):
    """
    Generate comprehensive test cases from a base configuration
    
    Args:
        test_config: Base test configuration
    
    Returns:
        List of generated test cases
    """
    logger.info(f"Generating test cases for: {test_config.name}")
    
    try:
        generated = await generate_test_cases(test_config)
        return generated
    
    except Exception as e:
        logger.error(f"Test generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ========================================================================
# SERVER STARTUP
# ========================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting API Tester Agent on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
