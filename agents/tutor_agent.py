from google import genai
import os
from typing import Dict, Any
from .math_agent import MathAgent
from .physics_agent import PhysicsAgent
from .chemistry_agent import ChemistryAgent

class TutorAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.math_agent = MathAgent(self.client)
        self.physics_agent = PhysicsAgent(self.client)
        self.chemistry_agent = ChemistryAgent(self.client)

        self.math_keywords = [
            'calculate', 'solve', 'equation', 'math', 'mathematics',
            'algebra', 'geometry', 'arithmetic', 'number', 'add',
            'subtract', 'multiply', 'divide', 'sum', 'product'
        ]
        self.physics_keywords = [
            'physics', 'force', 'velocity', 'acceleration', 'newton',
            'gravity', 'mass', 'energy', 'momentum', 'friction',
            'motion', 'speed', 'constant', 'law'
        ]
        self.chemistry_keywords = [
            'chemistry', 'chemical', 'element', 'compound', 'reaction',
            'molecule', 'atom', 'periodic table', 'bond'
        ]

    def _classify_query(self, query: str) -> str:                                                   # classify the query based on keywords
        query_lower = query.lower()
        math_score = sum(1 for keyword in self.math_keywords if keyword in query_lower)
        physics_score = sum(1 for keyword in self.physics_keywords if keyword in query_lower)
        chemistry_score = sum(1 for keyword in self.chemistry_keywords if keyword in query_lower)

        if math_score > max(physics_score, chemistry_score) and math_score > 0:
            return 'math'
        elif physics_score > max(math_score, chemistry_score) and physics_score > 0:
            return 'physics'
        elif chemistry_score > max(math_score, physics_score) and chemistry_score > 0:
            return 'chemistry'
        return self._classify_with_gemini(query)

    def _classify_with_gemini(self, query: str) -> str:                             # use Gemini to classify the query
        try:
            prompt = f"""
            Classify this question into: math, physics, chemistry, or general.

            Question: "{query}"

            Guidelines:
            - Math: arithmetic, algebra, geometry, calculations
            - Physics: forces, motion, energy, constants
            - Chemistry: elements, compounds, reactions
            - General: anything else

            Respond with one word: math, physics, chemistry, or general
            """
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            return response.text.strip().lower() if response.text.strip().lower() in ['math', 'physics', 'chemistry', 'general'] else 'general'
        except Exception:
            return 'general'

    async def process_query(self, query: str) -> Dict[str, Any]:
        category = self._classify_query(query)
        if category == 'math':
            result = await self.math_agent.handle_query(query)
            agent_used = 'Math Agent'
        elif category == 'physics':
            result = await self.physics_agent.handle_query(query)
            agent_used = 'Physics Agent'
        elif category == 'chemistry':
            result = await self.chemistry_agent.handle_query(query)
            agent_used = 'Chemistry Agent'
        else:
            result = await self._handle_general_query(query)
            agent_used = 'Tutor Agent'

        return {
            'answer': result['answer'],
            'agent_used': agent_used,
            'tools_used': result['tools_used'],
            'query_category': category
        }

    async def _handle_general_query(self, query: str) -> Dict[str, Any]:                # handle general queries that don't fit into math, physics, or chemistry
        try:
            prompt = f"""
            You are an AI tutor. Answer this question clearly and educationally.

            Question: {query}

            Provide a helpful response for a student.
            """
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            return {'answer': response.text, 'tools_used': []}
        except Exception as e:
            return {'answer': f"Error: {str(e)}", 'tools_used': []}