from typing import Dict, Any

class PhysicsFormulaTool:
    def __init__(self):
        self.formulas = {
            'newton_second_law': {
                'formula': 'F = m * a',
                'description': 'Force equals mass times acceleration (Newton\'s Second Law)',
                'variables': {'F': 'Force (N)', 'm': 'Mass (kg)', 'a': 'Acceleration (m/s²)'},
                'category': 'Mechanics'
            },
            'kinetic_energy': {
                'formula': 'KE = (1/2) * m * v^2',
                'description': 'Kinetic energy of a moving object',
                'variables': {'KE': 'Kinetic Energy (J)', 'm': 'Mass (kg)', 'v': 'Velocity (m/s)'},
                'category': 'Mechanics'
            },
            'potential_energy': {
                'formula': 'PE = m * g * h',
                'description': 'Gravitational potential energy',
                'variables': {'PE': 'Potential Energy (J)', 'm': 'Mass (kg)', 'g': 'Acceleration due to gravity (m/s²)', 'h': 'Height (m)'},
                'category': 'Mechanics'
            },
            'work_energy': {
                'formula': 'W = F * d * cos(θ)',
                'description': 'Work done by a force over a displacement',
                'variables': {'W': 'Work (J)', 'F': 'Force (N)', 'd': 'Displacement (m)', 'θ': 'Angle between force and displacement (degrees)'},
                'category': 'Mechanics'
            },
            'power': {
                'formula': 'P = W / t',
                'description': 'Power as work done per unit time',
                'variables': {'P': 'Power (W)', 'W': 'Work (J)', 't': 'Time (s)'},
                'category': 'Mechanics'
            },
            'momentum': {
                'formula': 'p = m * v',
                'description': 'Linear momentum of a moving object',
                'variables': {'p': 'Momentum (kg⋅m/s)', 'm': 'Mass (kg)', 'v': 'Velocity (m/s)'},
                'category': 'Mechanics'
            },
            'ohms_law': {
                'formula': 'V = I * R',
                'description': "Ohm's law relating voltage, current, and resistance",
                'variables': {'V': 'Voltage (V)', 'I': 'Current (A)', 'R': 'Resistance (Ω)'},
                'category': 'Electromagnetism'
            },
            'wave_equation': {
                'formula': 'v = f * λ',
                'description': 'Wave speed as frequency times wavelength',
                'variables': {'v': 'Wave speed (m/s)', 'f': 'Frequency (Hz)', 'λ': 'Wavelength (m)'},
                'category': 'Waves'
            },
            'gravitational_force': {
                'formula': 'F = G * m₁ * m₂ / r^2',
                'description': 'Universal law of gravitation',
                'variables': {'F': 'Gravitational force (N)', 'G': 'Gravitational constant (N⋅m²/kg²)', 'm₁,m₂': 'Masses (kg)', 'r': 'Distance between masses (m)'},
                'category': 'Gravitation'
            },
            'impulse': {
                'formula': 'J = F * Δt',
                'description': 'Impulse as force applied over time',
                'variables': {'J': 'Impulse (N⋅s)', 'F': 'Force (N)', 'Δt': 'Time interval (s)'},
                'category': 'Mechanics'
            },
            'projectile_range': {
                'formula': 'R = (v₀^2 * sin(2θ)) / g',
                'description': 'Range of a projectile launched horizontally',
                'variables': {'R': 'Range (m)', 'v₀': 'Initial velocity (m/s)', 'θ': 'Launch angle (degrees)', 'g': 'Acceleration due to gravity (m/s²)'},
                'category': 'Mechanics'
            },
            'hookes_law': {
                'formula': 'F = -k * x',
                'description': "Hooke's law for spring force",
                'variables': {'F': 'Force (N)', 'k': 'Spring constant (N/m)', 'x': 'Displacement from equilibrium (m)'},
                'category': 'Mechanics'
            },
            'electric_field': {
                'formula': 'E = k * q / r^2',
                'description': 'Electric field due to a point charge',
                'variables': {'E': 'Electric field (N/C)', 'k': 'Coulomb constant (N⋅m²/C²)', 'q': 'Charge (C)', 'r': 'Distance (m)'},
                'category': 'Electromagnetism'
            },
            'snells_law': {
                'formula': 'n₁ * sin(θ₁) = n₂ * sin(θ₂)',
                'description': "Snell's law for refraction",
                'variables': {'n₁,n₂': 'Refractive indices', 'θ₁,θ₂': 'Angles of incidence and refraction (degrees)'},
                'category': 'Optics'
            }
        }
    
    def get_formula(self, formula_name: str) -> Dict[str, Any]:
        return self.formulas.get(formula_name.lower(), None)
    
    def search_formulas(self, query: str) -> Dict[str, Dict[str, Any]]:
        matching = {}
        query = query.lower().strip()
        
        # Split query into words
        query_words = query.split()
        
        for name, data in self.formulas.items():
            # Check query word matches
            matches = False
            for word in query_words:
                if (word in name or 
                    word in data['description'].lower() or
                    word in data['category'].lower() or
                    any(word in var.lower() for var in data['variables'].values()) or
                    any(word in key.lower() for key in data['variables'].keys())):
                    matches = True
                    break
            if matches:
                matching[name] = data
                
        return matching