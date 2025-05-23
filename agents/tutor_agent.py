from google import genai
from google.genai import types
import os
from typing import Dict, Any
from .math_agent import MathAgent
from .physics_agent import PhysicsAgent

class TutorAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)

        self.math_agent = MathAgent(self.client)
        self.physics_agent = PhysicsAgent(self.client)

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
    
    def _classify_query(self, query: str) -> str:
        query_lower = query.lower()

        math_score = sum(1 for keyword in self.math_keywords if keyword in query_lower)
        physics_score = sum(1 for keyword in self.physics_keywords if keyword in query_lower)

        if math_score > physics_score and math_score > 0:
            return 'math'
        elif physics_score > math_score and physics_score > 0:
            return 'physics'
        else:
            return self._classify_with_gemini(query)
    
    def _classify_with_gemini(self, query: str) -> str:
        try:
            classification_prompt = f"""
            Classify this student question into one of these categories: math, physics, or general.
            
            Question: "{query}"
            
            Guidelines:
            - Math: arithmetic, algebra, geometry, calculations, equations
            - Physics: forces, motion, energy, constants, physical laws
            - General: anything else
            
            Respond with only one word: math, physics, or general
            """
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=classification_prompt
            )
            
            classification = response.text.strip().lower()
            if classification in ['math', 'physics', 'general']:
                return classification
            else:
                return 'general'
                
        except Exception:
            return 'general'
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        category = self._classify_query(query)

        if category == 'math':
            answer = await self.math_agent.handle_query(query)
            agent_used = 'Math Agent'
        elif category == 'physics':
            answer = await self.physics_agent.handle_query(query)
            agent_used = 'Physics Agent'
        else:
            answer = await self._handle_general_query(query)
            agent_used = 'Tutor Agent'
        
        return {
            'answer': answer,
            'agent_used': agent_used,
            'query_category': category
        }
    
    async def _handle_general_query(self, query: str) -> str:
        try:
            prompt = f"""
            You are a helpful AI tutor assistant. Answer this student's question clearly and educationally.
            
            Student Question: {query}
            
            Provide a clear, helpful response that would be appropriate for a student.
            """
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"