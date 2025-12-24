def voltage_to_value(value: int) -> int:
    """Convert Voltage to a value for a button cluster."""
    value_map = {
        4095: 0,
        0: 1,
        432: 2,
        1150: 3,
        1860: 4,
        2800: 5
    }
    for key in value_map:
        if abs(value - key) <= 50:
            return value_map[key]
    
    