from typing import Optional, Dict, Any

class PeriodicTableTool:
    def __init__(self):
        self.elements = {
            'hydrogen': {
                'atomic_number': 1,
                'atomic_mass': 1.008,
                'symbol': 'H',
                'group': 1,
                'period': 1,
                'electron_configuration': '1s¹',
                'description': 'A colorless, odorless gas, highly reactive.'
            },
            'helium': {
                'atomic_number': 2,
                'atomic_mass': 4.0026,
                'symbol': 'He',
                'group': 18,
                'period': 1,
                'electron_configuration': '1s²',
                'description': 'A noble gas, inert and used in balloons.'
            },
            'lithium': {
                'atomic_number': 3,
                'atomic_mass': 6.941,
                'symbol': 'Li',
                'group': 1,
                'period': 2,
                'electron_configuration': '[He] 2s¹',
                'description': 'A soft, silvery alkali metal.'
            },
            'beryllium': {
                'atomic_number': 4,
                'atomic_mass': 9.0122,
                'symbol': 'Be',
                'group': 2,
                'period': 2,
                'electron_configuration': '[He] 2s²',
                'description': 'A hard, grayish alkaline earth metal.'
            },
            'boron': {
                'atomic_number': 5,
                'atomic_mass': 10.811,
                'symbol': 'B',
                'group': 13,
                'period': 2,
                'electron_configuration': '[He] 2s² 2p¹',
                'description': 'A metalloid used in semiconductors.'
            },
            'carbon': {
                'atomic_number': 6,
                'atomic_mass': 12.011,
                'symbol': 'C',
                'group': 14,
                'period': 2,
                'electron_configuration': '[He] 2s² 2p²',
                'description': 'Basis of organic chemistry, exists as graphite and diamond.'
            },
            'nitrogen': {
                'atomic_number': 7,
                'atomic_mass': 14.007,
                'symbol': 'N',
                'group': 15,
                'period': 2,
                'electron_configuration': '[He] 2s² 2p³',
                'description': 'A colorless gas, makes up 78% of Earth’s atmosphere.'
            },
            'oxygen': {
                'atomic_number': 8,
                'atomic_mass': 15.999,
                'symbol': 'O',
                'group': 16,
                'period': 2,
                'electron_configuration': '[ Selected elements up to atomic number 20 for brevity. You can extend this further as needed. ]'
            }
        }
    def get_element_info(self, element_name: str) -> Optional[str]:
        element = self.elements.get(element_name.lower())
        if element:
            return (f"Element: {element_name.capitalize()}\n"
                    f"Atomic Number: {element['atomic_number']}\n"
                    f"Atomic Mass: {element['atomic_mass']} u\n"
                    f"Symbol: {element['symbol']}\n"
                    f"Group: {element['group']}\n"
                    f"Period: {element['period']}\n"
                    f"Electron Configuration: {element['electron_configuration']}\n"
                    f"Description: {element['description']}")
        return None

    def get_element_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        for name, data in self.elements.items():
            if data['symbol'].lower() == symbol.lower():
                return data
        return None