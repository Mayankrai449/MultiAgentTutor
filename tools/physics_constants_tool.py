from typing import Dict, Any, Optional

class PhysicsConstantsTool:
    
    def __init__(self):
        # physics constants
        self.constants = {
            'speed_of_light': {
                'name': 'Speed of Light',
                'symbol': 'c',
                'value': 299792458,
                'unit': 'm/s',
                'description': 'The speed of light in vacuum'
            },
            'gravitational_constant': {
                'name': 'Gravitational Constant',
                'symbol': 'G',
                'value': 6.67430e-11,
                'unit': 'm³/kg⋅s²',
                'description': 'Universal gravitational constant'
            },
            'planck_constant': {
                'name': 'Planck Constant',
                'symbol': 'h',
                'value': 6.62607015e-34,
                'unit': 'J⋅s',
                'description': 'Planck constant'
            },
            'reduced_planck_constant': {
                'name': 'Reduced Planck Constant',
                'symbol': 'ℏ',
                'value': 1.054571817e-34,
                'unit': 'J⋅s',
                'description': 'Reduced Planck constant (h/2π)'
            },
            'boltzmann_constant': {
                'name': 'Boltzmann Constant',
                'symbol': 'k_B',
                'value': 1.380649e-23,
                'unit': 'J/K',
                'description': 'Boltzmann constant'
            },
            'avogadro_number': {
                'name': 'Avogadro Number',
                'symbol': 'N_A',
                'value': 6.02214076e23,
                'unit': 'mol⁻¹',
                'description': 'Avogadro constant'
            },
            'gas_constant': {
                'name': 'Gas Constant',
                'symbol': 'R',
                'value': 8.314462618,
                'unit': 'J/(mol⋅K)',
                'description': 'Universal gas constant'
            },
            'elementary_charge': {
                'name': 'Elementary Charge',
                'symbol': 'e',
                'value': 1.602176634e-19,
                'unit': 'C',
                'description': 'Elementary electric charge'
            },
            'electron_mass': {
                'name': 'Electron Mass',
                'symbol': 'm_e',
                'value': 9.1093837015e-31,
                'unit': 'kg',
                'description': 'Rest mass of electron'
            },
            'proton_mass': {
                'name': 'Proton Mass',
                'symbol': 'm_p',
                'value': 1.67262192369e-27,
                'unit': 'kg',
                'description': 'Rest mass of proton'
            },
            'neutron_mass': {
                'name': 'Neutron Mass',
                'symbol': 'm_n',
                'value': 1.67492749804e-27,
                'unit': 'kg',
                'description': 'Rest mass of neutron'
            },
            'vacuum_permittivity': {
                'name': 'Vacuum Permittivity',
                'symbol': 'ε₀',
                'value': 8.8541878128e-12,
                'unit': 'F/m',
                'description': 'Electric permittivity of free space'
            },
            'vacuum_permeability': {
                'name': 'Vacuum Permeability',
                'symbol': 'μ₀',
                'value': 1.25663706212e-6,
                'unit': 'H/m',
                'description': 'Magnetic permeability of free space'
            },
            'earth_gravity': {
                'name': 'Standard Gravity',
                'symbol': 'g',
                'value': 9.80665,
                'unit': 'm/s²',
                'description': 'Standard acceleration due to gravity on Earth'
            },
            'stefan_boltzmann_constant': {
                'name': 'Stefan-Boltzmann Constant',
                'symbol': 'σ',
                'value': 5.670374419e-8,
                'unit': 'W/(m²⋅K⁴)',
                'description': 'Stefan-Boltzmann constant'
            },
            'fine_structure_constant': {
                'name': 'Fine Structure Constant',
                'symbol': 'α',
                'value': 7.2973525693e-3,
                'unit': 'dimensionless',
                'description': 'Fine structure constant'
            }
        }
    
    def get_constant(self, constant_name: str) -> Optional[Dict[str, Any]]:
        return self.constants.get(constant_name.lower())
    
    def get_all_constants(self) -> Dict[str, Dict[str, Any]]:
        return self.constants.copy()
    
    def search_constants(self, search_term: str) -> Dict[str, Dict[str, Any]]:
        search_term = search_term.lower()
        matching_constants = {}
        
        for key, constant in self.constants.items():
            # Search in name, symbol, and description
            if (search_term in constant['name'].lower() or 
                search_term in constant['symbol'].lower() or 
                search_term in constant['description'].lower()):
                matching_constants[key] = constant
        
        return matching_constants
    
    def get_constant_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        for constant in self.constants.values():
            if constant['symbol'].lower() == symbol.lower():
                return constant
        return None
    
    def format_constant(self, constant_data: Dict[str, Any]) -> str:
        name = constant_data['name']
        symbol = constant_data['symbol']
        value = constant_data['value']
        unit = constant_data['unit']
        description = constant_data['description']
        
        # format the value
        if isinstance(value, float):
            if value < 0.001 or value > 1000000:
                value_str = f"{value:.6e}"
            else:
                value_str = f"{value:.10f}".rstrip('0').rstrip('.')
        else:
            value_str = str(value)
        
        return f"{name} ({symbol}): {value_str} {unit}\n{description}"