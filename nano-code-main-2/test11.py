import json
from daytona_management.agent import generate_report


def main():
    plan_json = "/Users/gengjiawei/Documents/coding/nano-code-main-2/Json—test/test1.json"
    uploadfolder = "/Users/gengjiawei/Desktop/uploadfolder"

    result = generate_report(plan_json, uploadfolder)

    if hasattr(result, "model_dump"):
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
