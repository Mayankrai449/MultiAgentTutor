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
            r'what is the atomic number of',
            r'electron configuration of',
            r'properties of',
            r'element\s+\w+'
        ]
        return any(re.search(pattern, query.lower()) for pattern in patterns)

    def _extract_element(self, query: str) -> str:
        match = re.search(r'element\s+(\w+)', query.lower())
        return match.group(1) if match else None

    async def handle_query(self, query: str) -> Dict[str, Any]:
        tools_used = []
        element_info = ""

        if self._needs_periodic_table(query):
            element = self._extract_element(query)
            if element:
                info = self.periodic_table.get_element_info(element)
                if info:
                    element_info = f"Element info: {info}"
                    tools_used.append("Periodic Table")
                else:
                    element_info = f"No data found for {element}"

        prompt = f"""
        You are a chemistry tutor. A student asked: "{query}"

        {element_info}

        Provide a response that:
        1. Explains the chemistry concept clearly
        2. Uses the provided element info if relevant
        3. Shows calculations or reactions if needed
        4. Is educational and engaging
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}