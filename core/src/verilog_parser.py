import re
from enum import Enum


class Port:
    class Type(Enum):
        Input = 'input'
        Output = 'output'
        InOut = 'inout'

    def __init__(self, port_type: Type, vector_high: int, vector_low: int, name: str):
        # port_type [vector_high:vector_low] name;
        self.type = port_type
        self.vector_high = vector_high
        self.vector_low = vector_low
        self.name = name


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
        if 'input' in port_type:
            input_ports.append(port_name)
        if 'output' in port_type:
            output_ports.append(port_name)

    return input_ports, output_ports
