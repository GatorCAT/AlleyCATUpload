# GatorCATUpload
A python based tool for uploading Gator Grader data from Github Actions to a MongoDB Atlas Cluster

## Requirements:
* [Python](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/#installing-with-pipx)

## Usage:

### Github Actions
To utilize this tool within github actions insert these steps into your current github workflow:

```yml
# Gather Org and Repo name and create a file to put it into
- name: Set up outputfile
    if: always()
    run:  | 
    echo "${{ github.repository }}" > output.txt
    cat output.txt

# Capture output from Gator Grader and append it to the output file created prior
- name: Gather GatorGrader Output
    if: always()
    run:  |
    echo $(gradle grade) >> output.txt

# Fetch the repository to handle uploading info to MongoDB
- name: Fetch Upload Repo
    if: always()
    uses: actions/checkout@v2
    with: 
    repository: GatorCAT/GatorCATUpload
    path: ./Mongo_Upload

# Run GatorCATUpload to send data to the desired MongoDB
- name: Upload to MongoDB
    if: always()
    env:
    Username: ${{secrets.MONGO_USERNAME}}
    Password: ${{secrets.MONGO_PASSWORD}}
    Cluster_name: ${{secrets.MONGO_CLUSTER_NAME}}
    Collection_name: ${{secrets.MONGO_COLLECTION_NAME}}
    run:  |
    cd Mongo_Upload
    pip install typer
    pip install pymongo[srv]
    python --version
    python3 Upload_to_mongo.py ../output.txt $Username $Password $Cluster_name $Collection_name
```
**NOTE:** This action requires the use of [Python](https://www.python.org/) in the action, and all the requirements for [Gator Gradle](https://github.com/GatorEducator/gatorgradle)

As denoted by the variable names within the `env`, you will need to add Organization, or repository, *secrets* to securely use this code within a public repo.  Otherwise these values can be replaced with the required values.

**NOTE:** Within the code `StudentData` is hard-coded as the database within the collection chosen.  Given the current time restraint research into an alternative method was unable to occur.

### Running GatorCATUpload:
**CLI Arguments in order:**
| Argument | Expected Value |
|----------|----------------|
| inputfile | Path to file containing expected output from Github actions|
| username |Username for Mongodb access|
| password | Password for chosen user|
| cluster_name | Name of desired cluster (Must be exact casing)|
| collection_name | Name of desired collection (Must be exact casing)|

After cloning the repository:
```bash
python Upload_to_mongo.py inputfile username password cluster_name collection_name
```

Or with Poetry:
```bash
poetry run inputfile username password cluster_name colleciton_name
```