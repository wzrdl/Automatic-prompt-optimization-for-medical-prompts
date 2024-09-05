import json
import random

class JSONDataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_jsonl_file(self):
        data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                json_data = json.loads(line.strip())
                data.append(json_data)
        return data

    def get_question(self, json_data):
        return json_data["question"]

    def get_answer(self, json_data):
        return json_data["answer"]

    def get_options(self, json_data):
        options=json_data["options"]
        options_str = '\n'.join([f"{key}: {value}" for key, value in options.items()])
        return options_str

    def get_meta_info(self, json_data):
        return json_data["meta_info"]

    def get_answer_idx(self, json_data):
        return json_data["answer_idx"]

    def get_random_jsonl_data(self, num_samples):
        jsonl_data = self.read_jsonl_file()
        random_jsonl_data = random.sample(jsonl_data, num_samples)
        return random_jsonl_data
    

"""
if __name__ == "__main__":
    # JSONL 文件路径
    jsonl_file_path = 'D:/LLMdata/MedQA/questions/Mainland/train.jsonl'

    # 实例化 JSONDataExtractor 类
    data_extractor = JSONDataExtractor(jsonl_file_path)

    # 随机选择前100个数据
    random_jsonl_data = data_extractor.get_random_jsonl_data(2)

    # 实例化 JSONDataExtractor 类并打印提取的数据
    for data in random_jsonl_data:
        question = data_extractor.get_question(data)
        answer = data_extractor.get_answer(data)
        options = data_extractor.get_options(data)
        options=json.dumps(options,ensure_ascii=False)
        meta_info = data_extractor.get_meta_info(data)
        answer_idx = data_extractor.get_answer_idx(data)
        
        # 打印提取的数据
        print("问题:", question)
        print("答案:", answer)
        print("选项:", options)
        print("元信息:", meta_info)
        print("答案索引:", answer_idx)
"""




