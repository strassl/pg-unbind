import argparse
import re


def main():
    parser = argparse.ArgumentParser(description="Hacky script to create a query with inlined parameters from a query logged by postgres with bind parameters")
    parser.add_argument(
        "--input",
        type=str,
        help="log section with statement and bind parameters",
        required=True,
    )

    args = parser.parse_args()

    stmt = None
    params = None
    for line in args.input.split("\n"):
        if params is not None:
            params += line
        elif stmt is not None:
            params_match = re.match(
                "^.*?parameters: (.*?)$",
                line,
            )
            if params_match:
                params = params_match[1]
            else:
                stmt += line
        else:
            exec_match = re.match(r"^.*?execute .*?: (.*?)$", line)

            if exec_match:
                stmt = exec_match[1]
            else:
                continue

    inlined = stmt
    for binding in params.split(","):
        [k, v] = binding.split("=")
        k = k.strip()
        v = v.strip()
        inlined = re.sub(f"{re.escape(k)}(?![\d])", v, inlined)

    print(inlined)


if __name__ == "__main__":
    main()
