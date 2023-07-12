import verilog_parser


def main():
    inputs, outputs = verilog_parser.parse_verilog_module('../test/verilog/test.v')
    print('Input ports:', [i.name for i in inputs])
    print('Output ports:', [o.name for o in outputs])


if __name__ == '__main__':
    main()
