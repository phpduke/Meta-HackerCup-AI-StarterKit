from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional


class OptimalAgent:
    """Agent responsible for generating optimal/efficient solutions."""

    def __init__(self, model_name: str):
        # Parse model name (format: "google:model-name")
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name

        # Remove 'models/' prefix if present - LangChain adds it automatically
        if model.startswith("models/"):
            model = model.replace("models/", "")

        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.3)
        self.system_prompt = """You are an expert competitive programmer.

Your task is to generate an EFFICIENT solution in Python that meets the time/space constraints.

Guidelines:
- Optimize for the given constraints in the problem
- Use efficient algorithms and data structures
- Aim for optimal time and space complexity
- Read input from stdin, write output to stdout
- Handle the exact input/output format specified
- Include proper input parsing
- The solution must be CORRECT (passing all test cases)
- No unnecessary comments or explanations in code
- Make sure the solution is complete and runnable

Output ONLY the Python code, no markdown, no explanations.
"""

    def generate_solution(self, problem_statement: str, feedback: Optional[str] = None, attempt: int = 1) -> str:
        """Generate optimal solution for the given problem."""
        user_message = f"Generate an optimal Python solution for this problem:\n\n{problem_statement}"

        if feedback:
            user_message += f"\n\n=== FEEDBACK FROM ATTEMPT {attempt - 1} ===\n{feedback}\n\nPlease fix the issues and generate a corrected solution."

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = self.model.invoke(messages)
        code = response.content.strip()

        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()

        return code
