from google import genai
from typing import Dict, Any
import re
from tools.periodic_table_tool import PeriodicTableTool

class ChemistryAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.periodic_table = PeriodicTableTool()

    def _needs_periodic_table(self, query: str) -> bool:
        patterns = [
            # Atomic properties
            r'atomic number of\s+\w+',
            r'what is the atomic number',
            r'atomic mass of\s+\w+',
            r'atomic weight of\s+\w+',
            r'mass number of\s+\w+',
            
            # Electron configuration
            r'electron configuration of\s+\w+',
            r'electronic structure of\s+\w+',
            r'orbital configuration',
            
            # Element properties
            r'properties of\s+\w+',
            r'characteristics of\s+\w+',
            r'information about\s+\w+',
            r'tell me about\s+\w+',
            
            # Element identification
            r'element\s+\w+',
            r'symbol for\s+\w+',
            r'chemical symbol',
            r'what element has',
            
            # Periodic table position
            r'group\s+\d+',
            r'period\s+\d+',
            r'which group',
            r'which period',
            r'family of elements',
            
            # Specific elements (common ones)
            r'\b(?:hydrogen|helium|lithium|beryllium|boron|carbon|nitrogen|oxygen|fluorine|neon)\b',
            r'\b(?:sodium|magnesium|aluminum|silicon|phosphorus|sulfur|chlorine|argon)\b',
            r'\b(?:potassium|calcium|iron|copper|zinc|silver|gold|mercury|lead)\b',
            
            # Chemical symbols
            r'\b[A-Z][a-z]?\b(?:\s+element|\s+atom)',
        ]
        return any(re.search(pattern, query.lower()) for pattern in patterns)

    def _extract_element(self, query: str) -> str:
        # Try different patterns to extract element name
        patterns = [
            r'(?:element|atom|atomic number of|atomic mass of|properties of|electron configuration of)\s+(\w+)',
            r'tell me about\s+(\w+)',
            r'information about\s+(\w+)',
            r'what is\s+(\w+)',
            r'(\w+)\s+(?:element|atom)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                element = match.group(1)
                # Check if it's a valid element name or symbol
                if len(element) <= 3 and element.isalpha():
                    return element
        
        # Look for common element names directly
        common_elements = [
            'hydrogen', 'helium', 'lithium', 'beryllium', 'boron', 'carbon',
            'nitrogen', 'oxygen', 'fluorine', 'neon', 'sodium', 'magnesium',
            'aluminum', 'silicon', 'phosphorus', 'sulfur', 'chlorine', 'argon',
            'potassium', 'calcium', 'iron', 'copper', 'zinc', 'silver', 'gold'
        ]
        
        for element in common_elements:
            if element in query.lower():
                return element
        
        return None

    def _needs_chemical_calculation(self, query: str) -> bool:
        """Check if query needs chemical calculations"""
        calc_patterns = [
            r'molecular weight', r'molar mass', r'formula weight',
            r'moles of', r'molarity', r'concentration',
            r'balanced equation', r'stoichiometry',
            r'percent composition', r'empirical formula',
            r'limiting reagent', r'theoretical yield'
        ]
        return any(re.search(pattern, query.lower()) for pattern in calc_patterns)

    async def handle_query(self, query: str) -> Dict[str, Any]:
        tools_used = []
        element_info = ""
        calculation_info = ""

        if self._needs_periodic_table(query):
            element = self._extract_element(query)
            if element:
                info = self.periodic_table.get_element_info(element)
                if info:
                    element_info = f"Element Information:\n{info}"
                    tools_used.append("Periodic Table")
                else:
                    # Try by symbol if name didn't work
                    symbol_info = self.periodic_table.get_element_by_symbol(element)
                    if symbol_info:
                        element_info = f"Element found by symbol: {element}"
                        tools_used.append("Periodic Table")
                    else:
                        element_info = f"Element '{element}' not found in database"

        if self._needs_chemical_calculation(query):
            calculation_info = "Chemical calculations will be provided."

        prompt = f"""
        You are a chemistry tutor. A student asked: "{query}"

        {element_info}
        {calculation_info}

        Provide a response that:
        1. Explains the chemistry concept clearly
        2. Uses the provided element information if relevant
        3. Shows chemical equations and calculations if needed
        4. Includes molecular structures or diagrams when helpful
        5. Is educational and engaging
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}