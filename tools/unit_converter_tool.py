from typing import Tuple, Optional, Dict, Any

class UnitConverterTool:
    def __init__(self):
        # Define comprehensive conversion factors
        self.conversions = {
            # Length conversions
            ('m', 'km'): lambda x: x / 1000,
            ('km', 'm'): lambda x: x * 1000,
            ('m', 'cm'): lambda x: x * 100,
            ('cm', 'm'): lambda x: x / 100,
            ('m', 'mm'): lambda x: x * 1000,
            ('mm', 'm'): lambda x: x / 1000,
            ('km', 'cm'): lambda x: x * 100000,
            ('cm', 'km'): lambda x: x / 100000,
            
            # Imperial length
            ('m', 'ft'): lambda x: x * 3.28084,
            ('ft', 'm'): lambda x: x / 3.28084,
            ('m', 'in'): lambda x: x * 39.3701,
            ('in', 'm'): lambda x: x / 39.3701,
            ('km', 'mi'): lambda x: x * 0.621371,
            ('mi', 'km'): lambda x: x / 0.621371,
            
            # Speed conversions
            ('km/h', 'm/s'): lambda x: x * 1000 / 3600,
            ('m/s', 'km/h'): lambda x: x * 3600 / 1000,
            ('mph', 'm/s'): lambda x: x * 0.44704,
            ('m/s', 'mph'): lambda x: x / 0.44704,
            ('mph', 'km/h'): lambda x: x * 1.60934,
            ('km/h', 'mph'): lambda x: x / 1.60934,
            
            # Temperature conversions
            ('c', 'f'): lambda x: (x * 9/5) + 32,
            ('f', 'c'): lambda x: (x - 32) * 5/9,
            ('c', 'k'): lambda x: x + 273.15,
            ('k', 'c'): lambda x: x - 273.15,
            ('f', 'k'): lambda x: (x - 32) * 5/9 + 273.15,
            ('k', 'f'): lambda x: (x - 273.15) * 9/5 + 32,
            
            # Mass conversions
            ('kg', 'g'): lambda x: x * 1000,
            ('g', 'kg'): lambda x: x / 1000,
            ('kg', 'lb'): lambda x: x * 2.20462,
            ('lb', 'kg'): lambda x: x / 2.20462,
            ('g', 'oz'): lambda x: x * 0.035274,
            ('oz', 'g'): lambda x: x / 0.035274,
            
            # Time conversions
            ('s', 'min'): lambda x: x / 60,
            ('min', 's'): lambda x: x * 60,
            ('min', 'h'): lambda x: x / 60,
            ('h', 'min'): lambda x: x * 60,
            ('h', 'day'): lambda x: x / 24,
            ('day', 'h'): lambda x: x * 24,
            
            # Energy conversions
            ('j', 'cal'): lambda x: x / 4.184,
            ('cal', 'j'): lambda x: x * 4.184,
            ('j', 'kwh'): lambda x: x / 3600000,
            ('kwh', 'j'): lambda x: x * 3600000,
        }
    
    def convert(self, value: float, from_unit: str, to_unit: str) -> Optional[float]:
        # Normalize unit names
        from_unit = self._normalize_unit(from_unit.lower())
        to_unit = self._normalize_unit(to_unit.lower())
        
        key = (from_unit, to_unit)
        if key in self.conversions:
            return self.conversions[key](value)
        return None
    
    def _normalize_unit(self, unit: str) -> str:
        """Normalize unit names to standard forms"""
        unit_mappings = {
            'meter': 'm', 'metre': 'm', 'meters': 'm', 'metres': 'm',
            'kilometer': 'km', 'kilometre': 'km', 'kilometers': 'km', 'kilometres': 'km',
            'centimeter': 'cm', 'centimetre': 'cm', 'centimeters': 'cm', 'centimetres': 'cm',
            'millimeter': 'mm', 'millimetre': 'mm', 'millimeters': 'mm', 'millimetres': 'mm',
            'foot': 'ft', 'feet': 'ft',
            'inch': 'in', 'inches': 'in',
            'mile': 'mi', 'miles': 'mi',
            'celsius': 'c', 'fahrenheit': 'f', 'kelvin': 'k',
            'kilogram': 'kg', 'kilograms': 'kg',
            'gram': 'g', 'grams': 'g',
            'pound': 'lb', 'pounds': 'lb',
            'ounce': 'oz', 'ounces': 'oz',
            'second': 's', 'seconds': 's',
            'minute': 'min', 'minutes': 'min',
            'hour': 'h', 'hours': 'h',
            'joule': 'j', 'joules': 'j',
            'calorie': 'cal', 'calories': 'cal',
        }
        return unit_mappings.get(unit, unit)
    
    def get_supported_conversions(self) -> Dict[str, list]:
        """Return supported conversion categories"""
        categories = {
            'length': ['m', 'km', 'cm', 'mm', 'ft', 'in', 'mi'],
            'speed': ['m/s', 'km/h', 'mph'],
            'temperature': ['c', 'f', 'k'],
            'mass': ['kg', 'g', 'lb', 'oz'],
            'time': ['s', 'min', 'h', 'day'],
            'energy': ['j', 'cal', 'kwh']
        }
        return categories