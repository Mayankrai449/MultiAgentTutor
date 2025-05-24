from typing import Tuple, Optional

class UnitConverterTool:
    def convert(self, value: float, from_unit: str, to_unit: str) -> Optional[float]:
        conversions = {
            ('m', 'km'): lambda x: x / 1000,
            ('km', 'm'): lambda x: x * 1000,
            ('m', 'cm'): lambda x: x * 100,
            ('cm', 'm'): lambda x: x / 100,
            ('km/h', 'm/s'): lambda x: x * 1000 / 3600,
            ('m/s', 'km/h'): lambda x: x * 3600 / 1000,
            ('c', 'f'): lambda x: (x * 9/5) + 32,
            ('f', 'c'): lambda x: (x - 32) * 5/9
        }
        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            return conversions[key](value)
        return None