import re
from enum import Enum


class Port:
    class Type(Enum):
        Input = 'input'
        Output = 'output'

    def __init__(self, port_type: Type, vector_high: str, vector_low: str, name: str):
        self.type = port_type
        self.vector_high = vector_high
        self.vector_low = vector_low
        self.name = name


def parse_verilog_module(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('\n', ' ')

    # Find module declaration and port list
    module_match = re.search(r'module\s+(\w+)\s*\((.*?)\);', content, re.DOTALL)
    if not module_match:
        raise ValueError("Failed to find module declaration")

    module_name = module_match.group(1)
    port_list = module_match.group(2)

    # Find input and output ports
    ports = re.findall(r'(input|output)'
                       r'(?:\s*(\[\w+:\w+\]\s*)|\s+)'
                       r'([^;]*);',
                       content)

    input_ports = []
    output_ports = []
    for port in ports:
        port_type, port_range, port_names = port
        same_line_ports = port_names.split(',')
        same_line_ports = [p.strip() for p in same_line_ports]

        # Extract port type
        if 'input' in port:
            port_type = Port.Type.Input
        elif 'output' in port:
            port_type = Port.Type.Output

        # Extract port range
        vector_high, vector_low = 0, 0
        if port_range:
            vector_high, vector_low = port_range[1:-1].split(':')

        # Create Port object
        for port_name in same_line_ports:
            port = Port(port_type, vector_high, vector_low, port_name)
            # Append to respective port list
            if port_type == Port.Type.Input:
                input_ports.append(port)
            elif port_type == Port.Type.Output:
                output_ports.append(port)

    return input_ports, output_ports
