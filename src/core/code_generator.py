import google.generativeai as genai
from src.config.settings import GEMINI_API_KEY
from typing import Dict, Optional

class CodeGenerator:
    """Generates Python code for function invocation using Gemini Pro."""

    def __init__(self):
        """Initialize the Gemini Model."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_code(self, function_metadata: Dict, params: Optional[Dict] = None) -> str:
        """Generate a Python script using Gemini Model."""
        func_name = function_metadata["name"]
        module = function_metadata["module"]
        class_name = function_metadata["class"]
        params_list = function_metadata.get("params", [])

        # Format function parameters if provided
        param_str = ""
        if params_list and params:
            param_str = ", ".join(
                f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}"
                for k, v in params.items() if k in params_list
            )

        # Construct LLM prompt
        prompt = f"""
        Generate a Python script to invoke the function '{func_name}' from the module 'src.core.{module}' 
        and class '{class_name}'. The script should:
        - Import the class and function
        - Use Python's logging module instead of print statements
        - Define a `main()` function with structured error handling
        - Call the function {'with parameters' if param_str else 'without parameters'}
        - Ensure the script is executable with `if __name__ == "__main__"` block

        The final output should be **only** the Python code (no explanations, no markdown formatting, no extra text).
        """

        try:
            response = self.model.generate_content(prompt)
            if not response or not hasattr(response, "text") or not response.text:
                raise ValueError("Gemini Pro returned an empty response.")

            # Ensure no markdown formatting like ```python
            code = response.text.strip().replace("```python", "").replace("```", "").strip()
            return code

        except Exception as e:
            return f"Error generating code: {str(e)}"

if __name__ == "__main__":
    metadata = {
        "name": "open_chrome",
        "module": "automation_functions",
        "class": "AutomationFunctions"
    }
    generator = CodeGenerator()
    code = generator.generate_code(metadata)
    print("Generated Code:")
    print(code)
