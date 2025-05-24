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
            # Basic arithmetic
            r'\d+\s*[\+\-\*×÷\/]\s*\d+',
            r'\d+\s*plus\s*\d+',
            r'\d+\s*minus\s*\d+',
            r'\d+\s*times\s*\d+',
            r'\d+\s*divided\s+by\s*\d+',
            
            # Keywords
            r'calculate\s+\d',
            r'compute\s+\d',
            r'what\s+is\s+\d+',
            r'solve\s+\d',
            r'find\s+\d+',
            r'evaluate\s+\d',
            
            # Advanced operations
            r'to\s+the\s+power\s+of',
            r'raised\s+to\s+\d+',
            r'\d+\s*\^+\s*\d+',
            r'square\s+root\s+of\s+\d+',
            r'sqrt\s*\(\s*\d+',
            r'\d+\s*squared',
            r'\d+\s*cubed',
            
            # Mathematical functions
            r'sin\s*\(\s*\d+',
            r'cos\s*\(\s*\d+',
            r'tan\s*\(\s*\d+',
            r'log\s*\(\s*\d+',
            
            # Fractions and decimals
            r'\d+\.\d+\s*[\+\-\*\/]\s*\d+',
            r'\d+\s*\/\s*\d+\s*[\+\-\*\/]',
            
            # Word problems with numbers
            r'how\s+much\s+is\s+\d+',
            r'what\s+equals\s+\d+',
            r'result\s+of\s+\d+',
            r'answer\s+to\s+\d+',
            
            # Percentage calculations
            r'\d+\s*percent\s+of\s+\d+',
            r'\d+%\s+of\s+\d+',
            r'percentage\s+of\s+\d+',
        ]
        return any(re.search(pattern, query.lower()) for pattern in calculation_patterns)

    def _extract_calculation(self, query: str) -> str:
        query_lower = query.lower()
        
        # Handle percentage calculations
        percent_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s+of\s+(\d+(?:\.\d+)?)', query_lower)
        if percent_match:
            percentage, number = percent_match.groups()
            return f"({percentage} / 100) * {number}"
        
        # Handle square root
        sqrt_match = re.search(r'square\s+root\s+of\s+(\d+(?:\.\d+)?)', query_lower)
        if sqrt_match:
            return f"sqrt({sqrt_match.group(1)})"
        
        # Handle squared/cubed
        squared_match = re.search(r'(\d+(?:\.\d+)?)\s*squared', query_lower)
        if squared_match:
            return f"{squared_match.group(1)} ** 2"
        
        cubed_match = re.search(r'(\d+(?:\.\d+)?)\s*cubed', query_lower)
        if cubed_match:
            return f"{cubed_match.group(1)} ** 3"
        
        # Handle basic arithmetic with words
        word_ops = {
            'plus': '+', 'minus': '-', 'times': '*', 'multiplied by': '*',
            'divided by': '/', 'to the power of': '**', 'raised to': '**'
        }
        
        for word_op, symbol in word_ops.items():
            if word_op in query_lower:
                query = query.replace(word_op, symbol)
        
        # Handle basic arithmetic
        match = re.search(r'(\d+(?:\.\d+)?)\s*([\+\-\*×÷\/])\s*(\d+(?:\.\d+)?)', query)
        if match:
            num1, op, num2 = match.groups()
            op = op.replace('×', '*').replace('÷', '/')
            return f"{num1} {op} {num2}"

        # Handle exponentiation
        power_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:\*\*|\^)\s*(\d+(?:\.\d+)?)', query)
        if power_match:
            base, exponent = power_match.groups()
            return f"{base} ** {exponent}"

        # Fallback for other calculations
        calc_match = re.search(r'(?:calculate|solve|compute|evaluate|what is|find)\s+([^?]+)', query_lower)
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
        1. Shows step-by-step solution
        2. Explains the mathematical concept
        3. Includes the final answer
        4. Is educational and clear
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}