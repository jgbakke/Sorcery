import os
import json


class Notebook:
    def __init__(self) -> None:
        self.data = {}

    def check_and_create():
        if not os.path.isfile("./notes.json"):
            with open('notes.json', 'w') as file:
                file.write(json.dumps({}))
                file.close()

    def read_and_update(self, update=True):
        with open("notes.json", 'r') as readFile:
            old_results = json.load(readFile)
            if update:
                old_results.update(self.data)
            readFile.close()
        return old_results


    def read_results(self):
        Notebook.check_and_create()
                
        return str(self.read_and_update(False))

    def write_results(self, new_data):
        if new_data is not None and type(new_data) is dict:
            self.data.update(new_data)            
        else:
            print("Didn't write because data is not a dict")


    def flush_data(self):
        Notebook.check_and_create()

        fileData = self.read_and_update()

        with open("notes.json", 'w') as writeFile:
            json.dump(fileData, writeFile)
            writeFile.close()

