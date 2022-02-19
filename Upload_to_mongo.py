from pymongo import MongoClient
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
    output_dict = {}
    output_dict["class"] = org
    output_dict["assignment"] = repo
    all_checks = []
    check = []
    begin_check = False
    check_list = grade_content.split(" ")
    passing_break_char = "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    print(check_list)
    colors = ["\x1b[1;32m", "\x1b[0m", "\x1b[1;31m", "\x1b[1;35m", "\x1b[1;33m"]
    for color in colors:
        grade_content.replace(color, "")
    for index, item in enumerate(check_list):
        curr_character = check_list[index + 1]
        if item == "✔" or item == "✘":
            begin_check = True
        if begin_check:
            check.append(str(item))
        if curr_character == "✔" or curr_character == "✘":
            all_checks.append(" ".join(check))
            check = []
            begin_check = False
        elif "-~-" in curr_character or curr_character == passing_break_char:
            all_checks.append(" ".join(check))
            break
    del all_checks[0]
    output_dict["checks"] = parse_check_values(all_checks)
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

    