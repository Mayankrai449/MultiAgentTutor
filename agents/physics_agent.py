from google import genai
from typing import Dict, Any
import re
from tools.physics_constants_tool import PhysicsConstantsTool
from tools.unit_converter_tool import UnitConverterTool

class PhysicsAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.constants_tool = PhysicsConstantsTool()
        self.unit_converter = UnitConverterTool()

    def _needs_constants(self, query: str) -> bool:                     # check for physics constants
        constant_keywords = [
            'speed of light', 'light speed', 'c =',
            'gravitational constant', 'gravity constant', 'g =', 'G =',
            'planck', 'boltzmann', 'avogadro', 'electron mass',
            'proton mass', 'neutron mass', 'elementary charge',
            'permittivity', 'permeability', 'constant'
        ]
        return any(keyword in query.lower() for keyword in constant_keywords)

    def _identify_constants_needed(self, query: str) -> list:           # identify which constants are needed
        constant_mapping = {
            'speed of light': 'speed_of_light',
            'light speed': 'speed_of_light',
            'gravitational constant': 'gravitational_constant',
            'gravity constant': 'gravitational_constant',
            'planck': 'planck_constant',
            'boltzmann': 'boltzmann_constant',
            'avogadro': 'avogadro_number',
            'electron mass': 'electron_mass',
            'proton mass': 'proton_mass',
            'elementary charge': 'elementary_charge'
        }
        return [constant_mapping[k] for k in constant_mapping if k in query.lower()]

    def _needs_unit_conversion(self, query: str) -> bool:
        patterns = [r'convert\s+\d+\s*\w+\s+to\s+\w+', r'\d+\s*\w+\s+in\s+\w+']
        return any(re.search(pattern, query.lower()) for pattern in patterns)

    def _extract_conversion(self, query: str) -> tuple:
        match = re.search(r'convert\s+(\d+(?:\.\d+)?)\s*(\w+)\s+to\s+(\w+)', query.lower())
        if match:
            return float(match.group(1)), match.group(2), match.group(3)
        match = re.search(r'(\d+(?:\.\d+)?)\s*(\w+)\s+in\s+(\w+)', query.lower())
        if match:
            return float(match.group(1)), match.group(2), match.group(3)
        return None, None, None

    async def handle_query(self, query: str) -> Dict[str, Any]:
        tools_used = []
        constants_info = ""
        conversion_info = ""

        if self._needs_constants(query):
            needed = self._identify_constants_needed(query)
            if needed:
                constants_data = {c: self.constants_tool.get_constant(c) for c in needed if self.constants_tool.get_constant(c)}
                if constants_data:
                    constants_info = "Constants:\n" + "\n".join(
                        f"- {data['name']}: {data['value']} {data['unit']}" for data, name in constants_data.items()
                    )
                    tools_used.append("Physics Constants")

        if self._needs_unit_conversion(query):
            value, from_unit, to_unit = self._extract_conversion(query)
            if value is not None:
                result = self.unit_converter.convert(value, from_unit, to_unit)
                if result is not None:
                    conversion_info = f"Conversion: {value} {from_unit} = {result} {to_unit}"
                    tools_used.append("Unit Converter")

        prompt = f"""
        You are a physics tutor. A student asked: "{query}"

        {constants_info}
        {conversion_info}

        Provide a response that:
        1. Explains the concept
        2. Uses provided data
        3. Shows steps if needed
        4. Is educational
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}