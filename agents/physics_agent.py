from google import genai
from typing import Dict, Any
from tools.physics_constants_tool import PhysicsConstantsTool

class PhysicsAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.constants_tool = PhysicsConstantsTool()
        
    def _needs_constants(self, query: str) -> bool:
        constant_keywords = [
            'speed of light', 'light speed', 'c =',
            'gravitational constant', 'gravity constant', 'g =', 'G =',
            'planck', 'boltzmann', 'avogadro', 'electron mass',
            'proton mass', 'neutron mass', 'elementary charge',
            'permittivity', 'permeability', 'constant'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in constant_keywords)
    
    def _identify_constants_needed(self, query: str) -> list:
        query_lower = query.lower()
        needed_constants = []

        constant_mapping = {                                        # map keywords to constants
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
        
        for keyword, constant_name in constant_mapping.items():
            if keyword in query_lower:
                needed_constants.append(constant_name)
        
        return needed_constants
    
    async def handle_query(self, query: str) -> str:
        try:
            constants_info = ""
            if self._needs_constants(query):
                needed_constants = self._identify_constants_needed(query)
                if needed_constants:
                    constants_data = {}
                    for constant in needed_constants:
                        value = self.constants_tool.get_constant(constant)
                        if value:
                            constants_data[constant] = value
                    
                    if constants_data:
                        constants_info = "Here are the relevant physics constants:\n"
                        for name, data in constants_data.items():
                            constants_info += f"- {data['name']}: {data['value']} {data['unit']}\n"
                else:
                    all_constants = self.constants_tool.get_all_constants()
                    constants_info = "Here are some relevant physics constants:\n"
                    for name, data in all_constants.items():
                        constants_info += f"- {data['name']}: {data['value']} {data['unit']}\n"

            if constants_info:
                prompt = f"""
                You are a physics tutor. A student asked: "{query}"
                
                {constants_info}
                
                Please provide a comprehensive response that:
                1. Explains the physics concept clearly
                2. Uses the relevant constants if needed for calculations
                3. Shows step-by-step solutions if it's a problem
                4. Provides educational context and real-world applications
                5. Is clear and appropriate for a student learning physics
                
                Make your response engaging and educational.
                """
            else:
                prompt = f"""
                You are a physics tutor. Answer this student's physics question clearly and educationally.
                
                Student Question: {query}
                
                Provide:
                1. A clear explanation of the physics concept
                2. Step-by-step solution if it's a problem
                3. Real-world examples and applications
                4. Educational context
                5. Any relevant formulas or principles
                
                Make your response engaging and appropriate for a student learning physics.
                """
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while answering your physics question: {str(e)}"