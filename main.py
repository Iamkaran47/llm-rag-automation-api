# src/api/main.py

from fastapi import FastAPI
from src.core.rag_engine import RAGEngine
from src.core.code_generator import CodeGenerator
from src.core.context_manager import ContextManager
from src.api.models import ExecuteRequest, ExecuteResponse

app = FastAPI(title="LLM + RAG Automation API")
rag_engine = RAGEngine()
code_generator = CodeGenerator()
context_manager = ContextManager()

@app.post("/execute", response_model=ExecuteResponse)
async def execute_function(request: ExecuteRequest):
    """Execute an automation function based on the user prompt."""
    context = context_manager.get_context(request.session_id)
    augmented_query = f"{context}\nCurrent prompt: {request.prompt}" if context else request.prompt

    function_metadata = rag_engine.retrieve_function(augmented_query)
    if not function_metadata:
        raise ValueError("No matching function found.")

    code = code_generator.generate_code(function_metadata, request.params)

    context_manager.add_interaction(request.session_id, request.prompt, function_metadata)

    return ExecuteResponse(function=function_metadata["name"], code=code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)