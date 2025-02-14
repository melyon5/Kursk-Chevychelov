import sys


def main():
    args = sys.argv[1:]
    flags = {"--count": False, "--num": False, "--sort": False}
    filename = None

    for arg in args:
        if arg in flags:
            flags[arg] = True
        else:
            if filename is None:
                filename = arg

    if filename is None:
        print("ERROR")
        sys.exit()

    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
    except Exception:
        print("ERROR")
        sys.exit()

    if flags["--sort"]:
        lines = sorted(lines)

    if flags["--num"]:
        for i, line in enumerate(lines):
            print(f"{i} {line}")
    else:
        for line in lines:
            print(line)

    if flags["--count"]:
        print("rows count: " + str(len(lines)))


if __name__ == "__main__":
    main()
