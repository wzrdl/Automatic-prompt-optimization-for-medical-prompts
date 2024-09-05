# -*- coding: utf-8 -*-
import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from data_pro.MedQA_data  import JSONDataExtractor
import json

class AnsPromptGenerator:
    def __init__(self,temp):
        self.template = temp

    def generate_prompt(self, text):
        cat_prompt = PromptTemplate.from_template(self.template)
        prompt_template = cat_prompt.format(text=text)
        return prompt_template  

old_prompt="你现在是一名医生，具备丰富的医学知识和临床经验。你擅长诊断和治疗各种疾病，能为病人提供专业的医疗建议。在你思考这个问题的时候，首先要梳理提供的文本内容分析提供的信息，并且根据提出的问题对应到相关的领域，如果是选择题，先根据之前整理出来的信息，对于每一个选项逐步思考能否选择该选项及其理由。最后告诉我答案。如果不是选择题，那么需要你根据整理出来的信息逐步分析，最后回答问题。"
my_prompt="\nAs a highly skilled and experienced doctor, you possess a wealth of medical knowledge and clinical expertise. Your ability to diagnose and treat various diseases is exceptional, and you are adept at providing professional medical advice to patients. In order to effectively approach this problem, it is crucial for you to carefully analyze the information provided in the text and apply it to the relevant domains when addressing the given question. Thorough analysis is key to arriving at the correct answer.\n\nIf the question is a multiple-choice question, it is important to systematically evaluate each option based on the information you have gathered. Consider whether or not each option is a viable choice and provide a logical rationale for your decision. Take into account all the relevant domains and consider the implications of each option in relation to the given information.\n\nIf the question is not a multiple-choice question, you will need to analyze the information you have compiled step by step. Start by carefully reading and understanding the given text. Identify the key points and any relevant details that may help you answer the question. Consider the different domains that may be involved and how they relate to the question at hand. Evaluate the information and use your medical expertise to provide a comprehensive response.\n\nTo ensure a successful performance in this task, it is essential to address the issues and incorporate the advice from the previous prompts. The false examples provided in the previous prompts lacked thorough analysis, contained incorrect reasoning, and lacked clarity in explaining the thought process behind the answers. To rectify these problems, the following modifications have been made:\n\n1. Clear instructions: This prompt emphasizes the importance of analyzing the given information before answering the question. It explicitly states that a thorough analysis is required and encourages the examinee to consider all options and provide reasoning for their chosen answer.\n\n2. Critical thinking: The prompt prompts the examinee to think critically and analyze the information provided. It instructs them to identify discrepancies, evaluate the options, and provide logical reasoning for their chosen answer.\n\n3. Step-by-step approach: The prompt provides a structured approach for the examinee to follow. It guides them through the process of analyzing the information and answering the question by suggesting steps such as analyzing the given text, identifying relevant domains, evaluating each option, and providing a final answer.\n\nBy implementing these modifications, this prompt aims to better guide the examinee in analyzing the information and selecting the correct answer based on logical reasoning. This will enhance the examinee's performance and ensure a more accurate and comprehensive response.\n"
my_prompt="let's think step by step"
jsonl_file_path = 'D:/LLMdata/MedQA/questions/Mainland/train.jsonl'

# 实例化 JSONDataExtractor 类
data_extractor = JSONDataExtractor(jsonl_file_path)

# 随机选择前100个数据
random_jsonl_data = data_extractor.get_random_jsonl_data(50)

results = []

for data in random_jsonl_data:
    question = data_extractor.get_question(data)
    answer = data_extractor.get_answer(data)
    options = data_extractor.get_options(data)
    options = json.dumps(options, ensure_ascii=False)
    meta_info = data_extractor.get_meta_info(data)
    answer_idx = data_extractor.get_answer_idx(data)
    
    text = question+ " " + options
    prompt_generator = AnsPromptGenerator(my_prompt + " " + "文本, {text}" )
    prompt = prompt_generator.generate_prompt(text)
    
    # 使用 prompt 获取完成
    response = get_completion(prompt)
    
    # 创建结果字典
    result_entry = {
        "question": question,
        "answer": answer,
        "options": options,
        "generated_answer": response,
        "meta_info": meta_info,
        "answer_idx": answer_idx,
        "prompt": old_prompt
    }
    
    # 将结果字典添加到结果列表中
    results.append(result_entry)

# 将结果列表写入 JSON 文件
output_file_path="D:LLMdata/test_acc/medQA_test2.json"
with open(output_file_path, "w") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)