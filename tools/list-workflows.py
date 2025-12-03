import os

import process_street


def main() -> None:
    prst = process_street.ProcessStreetClient(api_key=os.getenv("PRST_API_KEY"))
    for f in prst.yield_workflows():
        print(f.get("id"), "/", f.get("name"))


if __name__ == "__main__":
    main()
