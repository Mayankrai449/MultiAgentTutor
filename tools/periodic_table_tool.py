from typing import Optional, Dict, Any

class PeriodicTableTool:
    def __init__(self):
        self.elements = {
            'hydrogen': {
                'atomic_number': 1, 'atomic_mass': 1.008, 'symbol': 'H',
                'group': 1, 'period': 1, 'electron_configuration': '1s¹',
                'description': 'A colorless, odorless gas, highly reactive.',
                'category': 'nonmetal', 'state': 'gas'
            },
            'helium': {
                'atomic_number': 2, 'atomic_mass': 4.0026, 'symbol': 'He',
                'group': 18, 'period': 1, 'electron_configuration': '1s²',
                'description': 'A noble gas, inert and used in balloons.',
                'category': 'noble_gas', 'state': 'gas'
            },
            'lithium': {
                'atomic_number': 3, 'atomic_mass': 6.941, 'symbol': 'Li',
                'group': 1, 'period': 2, 'electron_configuration': '[He] 2s¹',
                'description': 'A soft, silvery alkali metal.',
                'category': 'alkali_metal', 'state': 'solid'
            },
            'beryllium': {
                'atomic_number': 4, 'atomic_mass': 9.0122, 'symbol': 'Be',
                'group': 2, 'period': 2, 'electron_configuration': '[He] 2s²',
                'description': 'A hard, grayish alkaline earth metal.',
                'category': 'alkaline_earth_metal', 'state': 'solid'
            },
            'boron': {
                'atomic_number': 5, 'atomic_mass': 10.811, 'symbol': 'B',
                'group': 13, 'period': 2, 'electron_configuration': '[He] 2s² 2p¹',
                'description': 'A metalloid used in semiconductors.',
                'category': 'metalloid', 'state': 'solid'
            },
            'carbon': {
                'atomic_number': 6, 'atomic_mass': 12.011, 'symbol': 'C',
                'group': 14, 'period': 2, 'electron_configuration': '[He] 2s² 2p²',
                'description': 'Basis of organic chemistry, exists as graphite and diamond.',
                'category': 'nonmetal', 'state': 'solid'
            },
            'nitrogen': {
                'atomic_number': 7, 'atomic_mass': 14.007, 'symbol': 'N',
                'group': 15, 'period': 2, 'electron_configuration': '[He] 2s² 2p³',
                'description': 'A colorless gas, makes up 78% of Earth\'s atmosphere.',
                'category': 'nonmetal', 'state': 'gas'
            },
            'oxygen': {
                'atomic_number': 8, 'atomic_mass': 15.999, 'symbol': 'O',
                'group': 16, 'period': 2, 'electron_configuration': '[He] 2s² 2p⁴',
                'description': 'Essential for life, supports combustion.',
                'category': 'nonmetal', 'state': 'gas'
            },
            # Adding more elements for better coverage
            'fluorine': {
                'atomic_number': 9, 'atomic_mass': 18.998, 'symbol': 'F',
                'group': 17, 'period': 2, 'electron_configuration': '[He] 2s² 2p⁵',
                'description': 'Most electronegative element, highly reactive.',
                'category': 'halogen', 'state': 'gas'
            },
            'neon': {
                'atomic_number': 10, 'atomic_mass': 20.180, 'symbol': 'Ne',
                'group': 18, 'period': 2, 'electron_configuration': '[He] 2s² 2p⁶',
                'description': 'Noble gas used in neon signs.',
                'category': 'noble_gas', 'state': 'gas'
            },
            'sodium': {
                'atomic_number': 11, 'atomic_mass': 22.990, 'symbol': 'Na',
                'group': 1, 'period': 3, 'electron_configuration': '[Ne] 3s¹',
                'description': 'Soft alkali metal, reacts violently with water.',
                'category': 'alkali_metal', 'state': 'solid'
            },
            'magnesium': {
                'atomic_number': 12, 'atomic_mass': 24.305, 'symbol': 'Mg',
                'group': 2, 'period': 3, 'electron_configuration': '[Ne] 3s²',
                'description': 'Light metal used in alloys and fireworks.',
                'category': 'alkaline_earth_metal', 'state': 'solid'
            },
            'aluminum': {
                'atomic_number': 13, 'atomic_mass': 26.982, 'symbol': 'Al',
                'group': 13, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p¹',
                'description': 'Light, corrosion-resistant metal.',
                'category': 'post_transition_metal', 'state': 'solid'
            },
            'silicon': {
                'atomic_number': 14, 'atomic_mass': 28.085, 'symbol': 'Si',
                'group': 14, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p²',
                'description': 'Metalloid, basis of computer chips.',
                'category': 'metalloid', 'state': 'solid'
            },
            'phosphorus': {
                'atomic_number': 15, 'atomic_mass': 30.974, 'symbol': 'P',
                'group': 15, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p³',
                'description': 'Essential for life, used in fertilizers.',
                'category': 'nonmetal', 'state': 'solid'
            },
            'sulfur': {
                'atomic_number': 16, 'atomic_mass': 32.066, 'symbol': 'S',
                'group': 16, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p⁴',
                'description': 'Yellow nonmetal, used in vulcanization.',
                'category': 'nonmetal', 'state': 'solid'
            },
            'chlorine': {
                'atomic_number': 17, 'atomic_mass': 35.452, 'symbol': 'Cl',
                'group': 17, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p⁵',
                'description': 'Greenish gas, used in water purification.',
                'category': 'halogen', 'state': 'gas'
            },
            'argon': {
                'atomic_number': 18, 'atomic_mass': 39.948, 'symbol': 'Ar',
                'group': 18, 'period': 3, 'electron_configuration': '[Ne] 3s² 3p⁶',
                'description': 'Noble gas, used in welding.',
                'category': 'noble_gas', 'state': 'gas'
            },
            'iron': {
                'atomic_number': 26, 'atomic_mass': 55.845, 'symbol': 'Fe',
                'group': 8, 'period': 4, 'electron_configuration': '[Ar] 3d⁶ 4s²',
                'description': 'Most common metal on Earth, essential for life.',
                'category': 'transition_metal', 'state': 'solid'
            },
            'copper': {
                'atomic_number': 29, 'atomic_mass': 63.546, 'symbol': 'Cu',
                'group': 11, 'period': 4, 'electron_configuration': '[Ar] 3d¹⁰ 4s¹',
                'description': 'Excellent conductor of electricity.',
                'category': 'transition_metal', 'state': 'solid'
            },
            'zinc': {
                'atomic_number': 30, 'atomic_mass': 65.380, 'symbol': 'Zn',
                'group': 12, 'period': 4, 'electron_configuration': '[Ar] 3d¹⁰ 4s²',
                'description': 'Used in galvanization and alloys.',
                'category': 'transition_metal', 'state': 'solid'
            },
            'silver': {
                'atomic_number': 47, 'atomic_mass': 107.868, 'symbol': 'Ag',
                'group': 11, 'period': 5, 'electron_configuration': '[Kr] 4d¹⁰ 5s¹',
                'description': 'Precious metal with highest electrical conductivity.',
                'category': 'transition_metal', 'state': 'solid'
            },
            'gold': {
                'atomic_number': 79, 'atomic_mass': 196.967, 'symbol': 'Au',
                'group': 11, 'period': 6, 'electron_configuration': '[Xe] 4f¹⁴ 5d¹⁰ 6s¹',
                'description': 'Noble metal, highly valued and corrosion-resistant.',
                'category': 'transition_metal', 'state': 'solid'
            }
        }
    
    def get_element_info(self, element_name: str) -> Optional[str]:
        element = self.elements.get(element_name.lower())
        if element:
            return (f"Element: {element_name.capitalize()}\n"
                    f"Symbol: {element['symbol']}\n"
                    f"Atomic Number: {element['atomic_number']}\n"
                    f"Atomic Mass: {element['atomic_mass']} u\n"
                    f"Group: {element['group']}\n"
                    f"Period: {element['period']}\n"
                    f"Category: {element['category'].replace('_', ' ').title()}\n"
                    f"State: {element['state'].capitalize()}\n"
                    f"Electron Configuration: {element['electron_configuration']}\n"
                    f"Description: {element['description']}")
        return None

    def get_element_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        for name, data in self.elements.items():
            if data['symbol'].lower() == symbol.lower():
                return data
        return None
    
    def get_elements_by_group(self, group: int) -> Dict[str, Dict[str, Any]]:
        """Get all elements in a specific group"""
        group_elements = {}
        for name, data in self.elements.items():
            if data['group'] == group:
                group_elements[name] = data
        return group_elements
    
    def get_elements_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get all elements in a specific category"""
        category_elements = {}
        category = category.lower().replace(' ', '_')
        for name, data in self.elements.items():
            if data['category'] == category:
                category_elements[name] = data
        return category_elements