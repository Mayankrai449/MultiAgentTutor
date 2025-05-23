import re
import math
from typing import Dict, Any

class CalculatorTool:
    #safe math functions
    def __init__(self):
        self.safe_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'pi': math.pi,
            'e': math.e
        }
    
    def _sanitize_expression(self, expression: str) -> str:
        expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        replacements = {
            'x': '*',
            'X': '*',
            'plus': '+',
            'minus': '-',
            'times': '*',
            'divided by': '/',
            'divide': '/'
        }
        
        for old, new in replacements.items():
            expression = expression.replace(old, new)
        
        return expression.strip()
    
    def _safe_eval(self, expression: str) -> float:
        try:
            safe_dict = {
                '__builtins__': {},
                **self.safe_functions
            }
            
            result = eval(expression, safe_dict)
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Could not evaluate expression '{expression}': {str(e)}")
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        try:
            clean_expression = self._sanitize_expression(expression)
            
            if not clean_expression:
                return {
                    'success': False,
                    'error': 'No valid mathematical expression found',
                    'expression': expression
                }
            
            # Perform the calculation
            result = self._safe_eval(clean_expression)
            
            return {
                'success': True,
                'result': result,
                'expression': clean_expression,
                'original_expression': expression,
                'formatted_result': self._format_result(result)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }
    
    def _format_result(self, result: float) -> str:
        if result.is_integer():
            return str(int(result))
        
        if abs(result) < 0.001 or abs(result) > 1000000:
            return f"{result:.2e}"
        else:
            return f"{result:.6f}".rstrip('0').rstrip('.')

    #basic calc
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        return base ** exponent