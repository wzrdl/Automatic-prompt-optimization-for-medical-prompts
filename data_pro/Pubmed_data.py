import json
import random

class JsonData:
    def __init__(self, data):
        self.question = data.get("QUESTION")
        self.contexts = data.get("CONTEXTS")
        self.labels = data.get("LABELS")
        self.long_answer = data.get("LONG_ANSWER")
        self.meshes = data.get("MESHES")
        self.final_decision = data.get("final_decision")

class JsonDataReader:
    def __init__(self, filename):
        self.filename = filename
        self.json_objects = self.read_json_file()

    def read_json_file(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            json_data = json.load(file)
        json_objects = []
        for key, value in json_data.items():
            json_objects.append(JsonData(value))
        return json_objects

    def get_random_objects(self, count=2):
        return random.sample(self.json_objects, count)
"""
# 用法示例
filename = "D:/LLMdata/pubmed/ori_pqaa (1).json"  # 请将文件名替换为实际的 JSON 文件名
reader = JsonDataReader(filename)
random_objects = reader.get_random_objects(100)
for obj in random_objects:
    print("Question:", obj.question)
    print("Contexts:", obj.contexts)
    print("Labels:", obj.labels)
    print("Long Answer:", obj.long_answer)
    print("Meshes:", obj.meshes)
    print("Final Decision:", obj.final_decision)
    print()

"""
