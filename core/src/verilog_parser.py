import re
from enum import Enum


class Port:
    class Type(Enum):
        Input = 'input'
        Output = 'output'
        InOut = 'inout'

    def __init__(self, port_type: Type, vector_high: int, vector_low: int, name: str):
        self.type = port_type
        self.vector_high = vector_high
        self.vector_low = vector_low
        self.name = name

    def __str__(self):
        return self.name


def parse_verilog_module(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('\n', ' ')

    # Regular expression to match module declaration and port list
    module_regex = r'module\s+(\w+)\s*\((.*?)\);'

    # Find module declaration and port list
    module_match = re.search(module_regex, content, re.DOTALL)
    if not module_match:
        raise ValueError("Failed to find module declaration")

    module_name = module_match.group(1)
    port_list = module_match.group(2)

    # Regular expression to match individual ports
    port_regex = r'\s*(input|output|inout)?\s*(\[\d+:\d+\])?\s*(\w+)\s*(?:|\))'

    # Find input and output ports
    ports = re.findall(port_regex, port_list)

    input_ports = []
    output_ports = []
    for port in ports:
        port_type, port_range, port_name = port

        # Extract port type
        if 'input' in port_type:
            p_type = Port.Type.Input
        elif 'output' in port_type:
            p_type = Port.Type.Output
        else:
            p_type = Port.Type.InOut

        # Extract port range
        if port_range:
            range_match = re.search(r'\[(\d+):(\d+)]', port_range)
            if range_match:
                vector_high = int(range_match.group(1))
                vector_low = int(range_match.group(2))
            else:
                raise ValueError(f"Invalid range format for port: {port}")
        else:
            vector_high = 0
            vector_low = 0

        # Create Port object
        port_obj = Port(p_type, vector_high, vector_low, port_name)

        # Append to respective port list
        if p_type == Port.Type.Input:
            input_ports.append(port_obj)
        elif p_type == Port.Type.Output:
            output_ports.append(port_obj)

    return input_ports, output_ports
