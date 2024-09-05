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
my_prompt="""从文本中提取患者的信息作为条件，形如条件1,2,3,4，然后看信息之间的关联性，关联性强的就合并，并重新编号

第一步，你现在只有条件1，2,3，不允许考虑其他任何条件，给出一个0到0.5之间的数字，表示只在条件1的\
信息下选择每个选项的概率，对每个选项都解释给出该数字的理由，如果概率很小就给一个比较接近0的数，不要给0，如果概\
率比较大就给一个比较接近0.5的数。\

记住要把严重的疾病优先考虑\
第二步，结合你拥有的知识，以一个专业医生的视角，告诉我每一个条件可能的原因，不要漏掉任何一个条件以及数据。\
给出一个0到1之间数字，表示在患者的所有条件下选择每个选项的概率，对每个选项都解释给出该数\
字的理由，尽可能的详细分析每一个条件，如果概率很小就给一个比较接近0的数，不要给0，如果概\
    率很大就给一个比较接近1的数\

最后将每个选项得到的这两个概率相乘，并选出概率最大的选项。"""
#my_prompt="让我们一步一步思考"
jsonl_file_path = 'D:/LLMdata/MedQA/questions/Mainland/train.jsonl'

# 实例化 JSONDataExtractor 类
data_extractor = JSONDataExtractor(jsonl_file_path)

# 随机选择前100个数据
random_jsonl_data = data_extractor.get_random_jsonl_data(10)

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
output_file_path="D:LLMdata/test_acc/medQA_bayes.json"
with open(output_file_path, "w") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)