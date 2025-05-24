import re
import math
from typing import Dict, Any

class CalculatorTool:
    def __init__(self):
        self.safe_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'floor': math.floor,
            'ceil': math.ceil,
            'factorial': math.factorial,
            'gcd': math.gcd,
            'pi': math.pi,
            'e': math.e,
            'pow': math.pow,
            'degrees': math.degrees,
            'radians': math.radians
        }
    
    def _sanitize_expression(self, expression: str) -> str:
        # Enhanced sanitization with more mathematical operations
        expression = re.sub(r'[^0-9+\-*/().\s**×÷√π]', '', expression)
        
        replacements = {
            'x': '*', 'X': '*',
            '×': '*', '÷': '/',
            'plus': '+', 'minus': '-',
            'times': '*', 'multiplied by': '*',
            'divided by': '/', 'divide': '/',
            'to the power of': '**',
            'raised to': '**',
            '^': '**',
            '√': 'sqrt',
            'π': str(math.pi)
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
            
            # Handle special mathematical functions
            clean_expression = self._handle_special_functions(clean_expression)
            
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
    
    def _handle_special_functions(self, expression: str) -> str:
        """Handle special mathematical functions and operations"""
        # Handle percentage calculations
        expression = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'(\1/100)', expression)
        
        # Handle factorial
        expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)
        
        # Handle square root with sqrt() function
        expression = re.sub(r'sqrt\(([^)]+)\)', r'sqrt(\1)', expression)
        
        return expression
    
    def _format_result(self, result: float) -> str:
        if math.isnan(result):
            return "undefined"
        if math.isinf(result):
            return "infinity"
        if result.is_integer():
            return str(int(result))
        
        if abs(result) < 0.001 or abs(result) > 1000000:
            return f"{result:.2e}"
        else:
            return f"{result:.6f}".rstrip('0').rstrip('.')
    
    # Additional utility functions
    def solve_quadratic(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """Solve quadratic equation ax² + bx + c = 0"""
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return {
                'solutions': [x1, x2],
                'type': 'two_real_solutions',
                'discriminant': discriminant
            }
        elif discriminant == 0:
            x = -b / (2*a)
            return {
                'solutions': [x],
                'type': 'one_real_solution',
                'discriminant': discriminant
            }
        else:
            return {
                'solutions': [],
                'type': 'no_real_solutions',
                'discriminant': discriminant
            }
