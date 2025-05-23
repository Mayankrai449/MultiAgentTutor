from google import genai
import re
from tools.calculator_tool import CalculatorTool

class MathAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.calculator = CalculatorTool()
        
    def _needs_calculation(self, query: str) -> bool:
        calculation_patterns = [                        # identify math expressions
            r'\d+\s*[\+\-\*\/]\s*\d+',
            r'calculate\s+\d',
            r'what\s+is\s+\d+',
            r'solve\s+\d',
        ]
        
        query_lower = query.lower()
        for pattern in calculation_patterns:
            if re.search(pattern, query_lower):
                return True
        return False
    
    def _extract_calculation(self, query: str) -> str:
        match = re.search(r'(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)', query)
        if match:
            num1, op, num2 = match.groups()
            return f"{num1} {op} {num2}"

        calc_match = re.search(r'(?:calculate|solve|what is)\s+([^?]+)', query.lower())
        if calc_match:
            expression = calc_match.group(1).strip()
            return expression
            
        return query
    
    async def handle_query(self, query: str) -> str:
        try:
            if self._needs_calculation(query):
                expression = self._extract_calculation(query)

                calc_result = self.calculator.calculate(expression)

                prompt = f"""
                You are a mathematics tutor. A student asked: "{query}"
                
                I used a calculator tool and got this result: {calc_result}
                
                Please provide a complete response that:
                1. Shows the calculation step-by-step if applicable
                2. Explains the mathematical concept involved
                3. Includes the final answer
                4. Is educational and clear for a student
                
                Make your response conversational and helpful.
                """
            else:
                prompt = f"""
                You are a mathematics tutor. Answer this student's math question clearly and educationally.
                
                Student Question: {query}
                
                Provide:
                1. A clear explanation of the mathematical concept
                2. Step-by-step solution if it's a problem
                3. Examples if helpful
                4. Educational context
                
                Make your response appropriate for a student learning mathematics.
                """
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while solving your math problem: {str(e)}"