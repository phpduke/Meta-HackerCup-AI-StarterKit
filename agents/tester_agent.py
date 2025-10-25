from langchain_google_genai import ChatGoogleGenerativeAI


class TesterAgent:
    """Agent responsible for generating small test cases from problem statement."""

    def __init__(self, model_name: str):
        # Parse model name (format: "google:model-name")
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name

        # Remove 'models/' prefix if present - LangChain adds it automatically
        if model.startswith("models/"):
            model = model.replace("models/", "")

        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.7)
        self.system_prompt = """You are a test case generation expert for programming problems.

Your task is to generate SMALL, simple test cases that adhere to the input format specified in the problem statement.

Guidelines:
- Generate 3-5 small test cases
- Follow the exact input format specified
- Use small values (arrays of size 2-5, numbers < 100, etc.)
- Cover edge cases (empty, single element, boundary values)
- Output ONLY the test input, nothing else - NO markdown, NO code blocks, NO explanations
- Each test case should be separated by a blank line if multiple cases
- DO NOT wrap output in ``` markers or any other formatting

Example format for multiple test cases:
3
1 2 3

2
5 10

1
42

CRITICAL: Output ONLY the raw test input data above, nothing else!
"""

    def generate_test_cases(self, problem_statement: str) -> str:
        """Generate test cases for the given problem statement."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Generate small test cases for this problem:\n\n{problem_statement}"}
        ]

        response = self.model.invoke(messages)
        content = response.content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first and last lines if they are markdown markers
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        return content
