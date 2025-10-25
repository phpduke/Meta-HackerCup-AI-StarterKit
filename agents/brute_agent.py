from langchain_google_genai import ChatGoogleGenerativeAI


class BruteAgent:
    """Agent responsible for generating brute force solutions."""

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
        self.system_prompt = """You are a brute force algorithm expert.

Your task is to generate a SIMPLE, CORRECT brute force solution in Python.

Guidelines:
- Prioritize CORRECTNESS over efficiency
- Use simple, straightforward approaches (nested loops, recursion, etc.)
- Don't worry about time/space complexity
- Read input from stdin, write output to stdout
- Handle the exact input/output format specified
- Include proper input parsing
- No unnecessary comments or explanations in code
- Make sure the solution is complete and runnable

Output ONLY the Python code, no markdown, no explanations.
"""

    def generate_solution(self, problem_statement: str) -> str:
        """Generate brute force solution for the given problem."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Generate a brute force Python solution for this problem:\n\n{problem_statement}"}
        ]

        response = self.model.invoke(messages)
        code = response.content.strip()

        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()

        return code
