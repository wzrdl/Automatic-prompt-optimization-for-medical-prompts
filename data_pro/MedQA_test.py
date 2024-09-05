# -*- coding: utf-8 -*-
import json
import random

class JSONDataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_jsonl_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()  # 读取文件内容    
            json_data = json.loads(file_content)
        return json_data

    def get_question(self, json_data):
        return json_data["question"]

    def get_answer(self, json_data):
        return json_data["answer"]

    def get_options(self, json_data):
        return json_data["options"]

    def get_meta_info(self, json_data):
        return json_data["meta_info"]

    def get_answer_idx(self, json_data):
        return json_data["answer_idx"]
    
    def get_error_answer(self, json_data):
        return json_data["generated_answer"]
    
    def get_prompt(self, json_data):
        return json_data["prompt"]

    def get_random_jsonl_data(self, num_samples):
        jsonl_data = self.read_jsonl_file()
        random_jsonl_data = random.sample(jsonl_data, num_samples)
        return random_jsonl_data
    
import os
if __name__ == "__main__":
    # JSONL 文件路径
    #jsonl_file_path = 'D:/LLMdata/MedQA/questions/Mainland/train.jsonl'
    jsonl_file_path = 'D:/LLMdata/test_acc/medQA_old1.json'
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
        g_a=data_extractor.get_error_answer(data)
        
        # 打印提取的数据
        print("问题:", question)
        print("答案:", answer)
        print("选项:", options)
        print("元信息:", meta_info)
        print("答案索引:", answer_idx)






