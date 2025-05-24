from google import genai
from typing import Dict, Any
import re
from tools.physics_constants_tool import PhysicsConstantsTool
from tools.unit_converter_tool import UnitConverterTool
from tools.physics_formula_tool import PhysicsFormulaTool

class PhysicsAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.constants_tool = PhysicsConstantsTool()
        self.unit_converter = UnitConverterTool()
        self.formula_tool = PhysicsFormulaTool()

    def _needs_constants(self, query: str) -> bool:
        constant_keywords = [
            # Speed of light variations
            'speed of light', 'light speed', 'velocity of light', 'c =', 'c value',
            
            # Gravitational constant variations
            'gravitational constant', 'gravity constant', 'universal gravity',
            'g =', 'G =', 'big g', 'newton gravity',
            
            # Other constants
            'planck', 'boltzmann', 'avogadro', 'stefan boltzmann',
            'electron mass', 'proton mass', 'neutron mass',
            'elementary charge', ' permittivity', 'permeability',
            'gas constant', 'fine structure', 'vacuum',
            
            # General constant queries
            'physical constant', 'physics constant', 'fundamental constant',
            'what is the value of', 'value of constant',
            'constant equals', 'constant is'
        ]
        return any(keyword in query.lower() for keyword in constant_keywords)

    def _identify_constants_needed(self, query: str) -> list:
        constant_mapping = {
            'speed of light': 'speed_of_light',
            'light speed': 'speed_of_light',
            'velocity of light': 'speed_of_light',
            'c value': 'speed_of_light',
            'gravitational constant': 'gravitational_constant',
            'gravity constant': 'gravitational_constant', 
            'universal gravity': 'gravitational_constant',
            'big g': 'gravitational_constant',
            'planck': 'planck_constant',
            'boltzmann': 'boltzmann_constant',
            'avogadro': 'avogadro_number',
            'electron mass': 'electron_mass',
            'proton mass': 'proton_mass',
            'neutron mass': 'neutron_mass',
            'elementary charge': 'elementary_charge',
            'gas constant': 'gas_constant',
            'stefan boltzmann': 'stefan_boltzmann_constant',
            'fine structure': 'fine_structure_constant',
            'vacuum permittivity': 'vacuum_permittivity',
            'vacuum permeability': 'vacuum_permeability',
            'earth gravity': 'earth_gravity',
            'standard gravity': 'earth_gravity'
        }
        
        found_constants = []
        query_lower = query.lower()
        for keyword, constant_key in constant_mapping.items():
            if keyword in query_lower:
                found_constants.append(constant_key)
        
        return list(set(found_constants))  # Remove duplicates

    def _needs_unit_conversion(self, query: str) -> bool:
        patterns = [
            # Direct conversion requests
            r'convert\s+\d+(?:\.\d+)?\s*\w+\s+to\s+\w+',
            r'\d+(?:\.\d+)?\s*\w+\s+in\s+\w+',
            r'\d+(?:\.\d+)?\s*\w+\s+to\s+\w+',
            r'how many\s+\w+\s+in\s+\d+(?:\.\d+)?\s*\w+',
            
            # Temperature conversions
            r'\d+(?:\.\d+)?\s*(?:degrees?\s*)?(?:celsius|fahrenheit|kelvin)',
            r'convert.*temperature',
            r'celsius to fahrenheit',
            r'fahrenheit to celsius',
            
            # Length conversions
            r'\d+(?:\.\d+)?\s*(?:meter|metre|kilometer|centimeter|millimeter|inch|foot|feet|yard|mile)',
            r'convert.*(?:length|distance)',
            
            # Speed conversions
            r'\d+(?:\.\d+)?\s*(?:m/s|km/h|mph|ft/s)',
            r'convert.*speed',
            r'convert.*velocity',
            
            # Mass conversions
            r'\d+(?:\.\d+)?\s*(?:kg|gram|pound|ounce)',
            r'convert.*(?:mass|weight)',
            
            # Time conversions
            r'\d+(?:\.\d+)?\s*(?:second|minute|hour|day)',
            r'convert.*time',
            
            # Energy conversions
            r'\d+(?:\.\d+)?\s*(?:joule|calorie|watt|kwh)',
            r'convert.*energy'
        ]
        return any(re.search(pattern, query.lower()) for pattern in patterns)

    def _extract_conversion(self, query: str) -> tuple:
        # Try different patterns for extraction
        patterns = [
            r'convert\s+(\d+(?:\.\d+)?)\s*(\w+)\s+to\s+(\w+)',
            r'(\d+(?:\.\d+)?)\s*(\w+)\s+in\s+(\w+)',
            r'(\d+(?:\.\d+)?)\s*(\w+)\s+to\s+(\w+)',
            r'how many\s+(\w+)\s+in\s+(\d+(?:\.\d+)?)\s*(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    try:
                        value = float(groups[0])
                        return value, groups[1], groups[2]
                    except (ValueError, IndexError):
                        continue
        
        return None, None, None

    def _needs_physics_formula(self, query: str) -> bool:
        formula_keywords = [
            'force equals', 'f = ma', 'newton second law',
            'kinetic energy', 'ke =', 'potential energy', 'pe =',
            'momentum', 'p = mv', 'impulse',
            'work done', 'w = fd', 'power', 'p = w/t',
            'frequency', 'wavelength', 'wave equation',
            'ohm law', 'v = ir', 'resistance',
            'acceleration', 'velocity', 'displacement',
            'gravity formula', 'gravitational force'
        ]
        return any(keyword in query.lower() for keyword in formula_keywords)

    async def handle_query(self, query: str) -> Dict[str, Any]:
        tools_used = []
        constants_info = ""
        conversion_info = ""
        formula_info = ""

        # Check for constants
        if self._needs_constants(query):
            needed_constants = self._identify_constants_needed(query)
            if needed_constants:
                constants_data = {}
                for const_key in needed_constants:
                    const_data = self.constants_tool.get_constant(const_key)
                    if const_data:
                        constants_data[const_key] = const_data
                
                if constants_data:
                    constants_info = "Physical Constants:\n" + "\n".join(
                        f"- {data['name']}: {data['value']} {data['unit']}" 
                        for data in constants_data.values()
                    )
                    tools_used.append("Physics Constants")

        # Check for unit conversion
        if self._needs_unit_conversion(query):
            value, from_unit, to_unit = self._extract_conversion(query)
            if value is not None and from_unit and to_unit:
                result = self.unit_converter.convert(value, from_unit, to_unit)
                if result is not None:
                    conversion_info = f"Unit Conversion: {value} {from_unit} = {result} {to_unit}"
                    tools_used.append("Unit Converter")

        # Check for physics formulas
        if self._needs_physics_formula(query):
            formula_matches = self.formula_tool.search_formulas(query)
            if formula_matches:
                formula_info = "Relevant Physics Formulas:\n" + "\n".join(
                    f"- {data['description']}: {data['formula']} (Variables: {', '.join(f'{k}: {v}' for k, v in data['variables'].items())})"
                    for data in formula_matches.values()
                )
                tools_used.append("Physics Formulas")

        prompt = f"""
        You are a physics tutor. A student asked: "{query}"

        {constants_info}
        {conversion_info}
        {formula_info}

        Provide a response that:
        1. Explains the physics concept clearly
        2. Uses the provided constants and conversions
        3. Shows step-by-step calculations if needed
        4. Includes relevant formulas
        5. Is educational and comprehensive
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt
        )
        return {'answer': response.text, 'tools_used': tools_used}