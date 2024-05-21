from data_formats.control_command import ControlCommand


cc = """
    {
    "left": {
            "direction":"forward"
            },
    "right": {
            "direction":"stop"
            }
    }
"""
z = ControlCommand.parse_raw(cc)

print(z.dict())
