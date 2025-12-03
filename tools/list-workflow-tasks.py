import argparse
import os

import process_street


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id", type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    prst = process_street.ProcessStreetClient(api_key=os.getenv("PRST_API_KEY"))
    for f in prst.yield_workflow_tasks(args.workflow_id):
        print(f.get("id"), "/", f.get("name"), "/", f.get("taskType"))


if __name__ == "__main__":
    main()
