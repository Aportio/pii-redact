# =========================================================
# MIT license.
#
# (c) 2025 Aportio Developments Ltd.
# =========================================================


def get_aruments() -> dict:
    # create parser
    parser = argparse.ArgumentParser(description=f"PII Email Redactor {VERSION}")

    # add arguments to the parser
    parser.add_argument("file", help="File to process")
    parser.add_argument(
        "-o", "--out", help="Output directory", default="redacted-emails"
    )
    parser.add_argument(
        "-m", "--map", help="Define mappings for input fields", action="append"
    )

    # parse the arguments
    args = parser.parse_args()
    return args


def main():
    print("Hello from pii-redact!")


if __name__ == "__main__":
    main()
