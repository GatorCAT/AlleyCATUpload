# GatorCATUpload
A python based tool for uploading Gator Grader data from Github Actions to a MongoDB Atlas Cluster

## Requirements:
* [Python](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/#installing-with-pipx)

## Usage:

### Github Actions
To utilize this tool within github actions insert these steps into your current github workflow:

```yml
- name: Set up outputfile
          if: always()
          run:  | 
            echo "${{ github.repository }}" > output.txt
            cat output.txt

        - name: Gather GatorGrader Output
          if: always()
          run:  |
            echo $(gradle grade) >> output.txt

        - name: Fetch Upload Repo
          if: always()
          uses: actions/checkout@v2
          with: 
            repository: GatorCAT/GatorCATUpload
            path: ./Mongo_Upload
        
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

        - name: Display Output
          if: always()
          run: cat output.txt
```
**NOTE:** This action requires the use of [Python](https://www.python.org/) in the action, and all the requirements for [Gator Gradle](https://github.com/GatorEducator/gatorgradle)