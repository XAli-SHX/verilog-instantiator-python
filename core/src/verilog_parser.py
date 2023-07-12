import re


def parse_verilog_module(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expressions to match input and output port declarations
    input_regex = r'input\s+(\[\d+:\d+\]\s+)?\w+\s*;'
    output_regex = r'output\s+(\[\d+:\d+\]\s+)?\w+\s*;'

    # Find input ports
    input_ports = re.findall(input_regex, content)
    input_ports = [re.search(r'\w+', port).group() for port in input_ports]

    # Find output ports
    output_ports = re.findall(output_regex, content)
    output_ports = [re.search(r'\w+', port).group() for port in output_ports]

    return input_ports, output_ports
