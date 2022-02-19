from pymongo import MongoClient
import re
import typer

cli = typer.Typer()

@cli.command()
def main(filepath: str, user: str, mongopass: str, cluster: str, collection_name: str):
    parse_input = []
    try:
        with open(filepath, encoding="utf8") as content:
            parse_input = content.read().splitlines()
            content.close()
    except FileNotFoundError:
        print("File not found")
        raise
    org, repo = get_org_and_repo(parse_input[0])    
    grade_content = parse_input[1]
    print(grade_content)
    output_dict = {}
    output_dict["class"] = org
    output_dict["assignment"] = repo
    # all_checks = []
    checks = re.findall(r"[✔|✘][a-z0-9\s\.\\\/\-\(\)_'\"\[\]]+\s", grade_content, flags=re.I)

    checks = [check.strip() for check in checks]
    # check = []
    # begin_check = False
    # check_list = grade_content.split(" ")
    # for index, item in enumerate(check_list):
    #     #print(f"Index: {index}\tItem: {item}")
    #     try:
    #         next_character = check_list[index + 1]
    #     except:
    #         raise
    #     if item == "✔" or item == "✘":
    #         begin_check = True
    #     if begin_check:
    #         check.append(str(item))
    #     if next_character == "✔" or next_character == "✘":
    #         print(f"Check: {check}")
    #         all_checks.append(" ".join(check))
    #         check = []
    #         begin_check = False
    #     elif "-~-" in next_character or "┏" in next_character:
    #         all_checks.append(" ".join(check))
    #         break
    output_dict["checks"] = parse_check_values(checks)
    print(f"Checks: {checks}")
    for item in output_dict:
        if item == "checks":
            for object in output_dict[item]:
                print(f"Result: {output_dict['checks'][object]}\tCheck:  {object}")
        else:
            print(f"{item}: {output_dict[item]}")
    upload_to_mongo(output_dict, user, mongopass, cluster, collection_name)

def get_org_and_repo(repository:str):
    org, repo = repository.split("/")
    if "-" in repo:
        repo = repo.split("-")
        del repo[-1]
        repo = " ".join(repo)
    return org, repo

def parse_check_values(check_list: list):
    output = {}
    for item in check_list:
        name = ""
        if item[0] ==  "✔":
            name = item[2:]
            output[name] = True
        else:
            name = item[2:]
            output[name] = False
    return output

def upload_to_mongo(info: str, user: str, password: str, cluster_name: str, database: str):
    try:
        client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster_name}.u4cyq.mongodb.net/{database}?retryWrites=true&w=majority")
        db = client.test
        db = client.get_database(database)
    except:
        raise
    db.StudentData.insert_one(info)
if __name__ == "__main__":
    cli()

    