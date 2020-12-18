import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="A tool to automatically style python code to PEP8.")
    parser.add_argument(
        "-i",
        "--input",
        help="The input file",
        required=True
    )
    args = parser.parse_args()
    return args


def indentation(line, level):
    pass



def main():
    args = parse_args()
    code = list()
    with open(args.input, "r") as file:
        for line in file:
            code.append(line)
        else:
            pass
    # Indentation
    level = 0
    for i in range(0, code.__len__()):
        if line.lstrip()[0:2] != "//":
            if line.find("{"):
                indentation(line, level)


if __name__ == '__main__':
    main()