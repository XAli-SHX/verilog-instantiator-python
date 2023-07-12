import verilog_parser


def main():
    inputs, outputs = verilog_parser.parse_verilog_module('../test/verilog/test.v')
    print('Input ports:', inputs)
    print('Output ports:', outputs)


if __name__ == '__main__':
    main()
