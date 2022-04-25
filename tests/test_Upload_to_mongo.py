import pytest
from alleycatupload import Upload_to_mongo

@pytest.mark.parametrize(
        "test_input,expected_org,expected_repo",
        [
            ("cmpsc101/assignment1-Student1","cmpsc101","assignment1"),
            ("cmpsc102/assignment2-Student1","cmpsc102","assignment2"),
            ("GatorCAT/GatorCATUpload-Student1","GatorCAT","GatorCATUpload")
        ]
        )
def test_get_org_and_repo_with_student(test_input, expected_org,expected_repo):
    org, repo = Upload_to_mongo.get_org_and_repo(test_input)
    assert org == expected_org
    assert repo == expected_repo

@pytest.mark.parametrize(
        "test_input,expected_org,expected_repo",
        [
            ("cmpsc101/assignment1","cmpsc101","assignment1"),
            ("cmpsc102/assignment2","cmpsc102","assignment2"),
            ("GatorCAT/GatorCATUpload","GatorCAT","GatorCATUpload")
        ]
        )
def test_get_org_and_repo_without_student(test_input, expected_org,expected_repo):
    org, repo = Upload_to_mongo.get_org_and_repo(test_input)
    assert org == expected_org
    assert repo == expected_repo

@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([
            "✔ check1", 
            "✔ check2", 
            "✔ check3", 
            "✘ check4", 
            "✘ check5"
        ], 
        {
            "check1": True, 
            "check2": True, 
            "check3": True, 
            "check4": False, 
            "check5": False
        }),
        ([
            "✘ check1", 
            "✘ check2", 
            "✘ check3", 
            "✘ check4", 
            "✘ check5"
        ], 
        {
            "check1": False, 
            "check2": False, 
            "check3": False, 
            "check4": False, 
            "check5": False
        }),
        ([
            "✔ check1", 
            "✔ check2", 
            "✔ check3", 
            "✔ check4", 
            "✔ check5"
        ], 
        {
            "check1": True, 
            "check2": True, 
            "check3": True, 
            "check4": True, 
            "check5": True
        })
    ]
)
def test_parse_check_values(test_input,expected):
    checks = Upload_to_mongo.parse_check_values(test_input)
    assert checks == expected