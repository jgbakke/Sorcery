import os
import json


class Notebook:
    def __init__(self) -> None:
        pass

    def check_and_create():
        if not os.path.isfile("./notes.json"):
            with open('notes.json', 'w') as file:
                file.write(json.dumps({}))
                file.close()

    def read_results():
        Notebook.check_and_create()
        
        data = None
        with open("notes.json", 'r') as resultsFile:
            data = json.load(resultsFile)
        resultsFile.close()
        
        return str(data)

    def write_results(data):
        if data is not None and type(data) is dict:
            Notebook.check_and_create()
            
            with open("notes.json", 'r') as readFile:
                fileData = json.load(readFile)
                fileData.update(data)
                readFile.close()

            with open("notes.json", 'w') as writeFile:
                json.dump(fileData, writeFile)
                writeFile.close()
        else:
            print("Didn't write because data is not a dict")

