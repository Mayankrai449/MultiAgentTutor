from google import genai
import re
from tools.calculator_tool import CalculatorTool
from typing import Dict, Any

class MathAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.calculator = CalculatorTool()

    def _needs_calculation(self, query: str) -> bool:
        calculation_patterns = [
            r'\d+\s*[\+\-\*\/]\s*\d+',  # Basic arithmetic
            r'calculate\s+\d',           # Calculate keyword
            r'what\s+is\s+\d+',          # What is keyword
            r'solve\s+\d',               # Solve keyword
            r'to\s+the\s+power\s+of',    # Exponentiation (e.g., 2 to the power of 10)
            r'raised\s+to\s+\d+',        # Exponentiation (e.g., 2 raised to 3)
            r'\d+\s*\^+\s*\d+'          # Exponentiation (e.g., 2^3)
        ]
        return any(re.search(pattern, query.lower()) for pattern in calculation_patterns)

    def _extract_calculation(self, query: str) -> str:
        # Handle basic arithmetic
        match = re.search(r'(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)', query)
        if match:
            num1, op, num2 = match.groups()
            return f"{num1} {op} {num2}"

        # Handle exponentiation
        power_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:to\s+the\s+power\s+of|raised\s+to|\^)\s*(\d+(?:\.\d+)?)', query.lower())
        if power_match:
            base, exponent = power_match.groups()
            return f"{base} ** {exponent}"

        # Fallback for other calculations
        calc_match = re.search(r'(?:calculate|solve|what is)\s+([^?]+)', query.lower())
        return calc_match.group(1).strip() if calc_match else query

    async def handle_query(self, query: str) -> Dict[str, Any]:
        tools_used = []
        calc_info = ""

        if self._needs_calculation(query):
            tools_used.append("Calculator")
            expression = self._extract_calculation(query)
            calc_result = self.calculator.calculate(expression)
            if calc_result['success']:
                calc_info = f"Calculation result: {calc_result['result']}"
                

        prompt = f"""
        You are a mathematics tutor. A student asked: "{query}"

        {calc_info}

        Provide a response that:
        1. Shows steps if applicable
        2. Explains the concept
        3. Includes the answer
        4. Is educational
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}