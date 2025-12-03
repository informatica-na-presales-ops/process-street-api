import argparse
import os

import process_street


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id", type=str)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prst = process_street.ProcessStreetClient(api_key=os.getenv("PRST_API_KEY"))
    for f in prst.yield_workflow_form_fields(args.workflow_id):
        print(
            " / ".join(
                f.get(key) for key in ("id", "taskId", "fieldType", "key", "label")
            )
        )


if __name__ == "__main__":
    main()
