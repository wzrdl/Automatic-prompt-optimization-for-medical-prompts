# -*- coding: utf-8 -*-
import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from data_pro.Pubmed_data  import JsonData,JsonDataReader
import json

class AnsPromptGenerator:
    def __init__(self,temp):
        self.template = temp

    def generate_prompt(self, text):
        cat_prompt = PromptTemplate.from_template(self.template)
        prompt_template = cat_prompt.format(text=text)
        return prompt_template  

old_prompt="你现在是一名医生，具备丰富的医学知识和临床经验。你擅长诊断和治疗各种疾病，能为病人提供专业的医疗建议。在你思考这个问题的时候，首先要梳理提供的文本内容分析提供的信息，并且根据提出的问题对应到相关的领域，如果是选择题，先根据之前整理出来的信息，对于每一个选项逐步思考能否选择该选项及其理由。最后告诉我答案。如果不是选择题，那么需要你根据整理出来的信息逐步分析，最后回答问题。"
my_prompt="作为一名具有丰富医学知识和临床经验的医生，您的任务是分析提供的信息并向患者提供专业的医疗建议。为了有效地处理这项任务，重要的是遵循以下步骤：分析信息：仔细审查文本，并确定相关细节和关键点。注意任何症状、病史或其他可能对诊断或治疗重要的信息。理解背景：为了更好地理解所提供信息的相关性，有些背景上下文是必要的。熟悉涉及的情景或患者，包括他们的年龄、性别、生活方式以及可能影响其健康的任何其他相关因素。确定具体问题：清楚地确定需要回答的具体问题或需要进行的分析类型。这将有助于引导您的思考，并确保您涵盖所有必要的方面。进行全面分析：在回答问题或提供医疗建议时，考虑所有可用信息，并运用您的医学知识和临床经验。根据其可行性、有效性以及潜在的风险或副作用评估选项或潜在的治疗方案。考虑患者病情的任何禁忌症或特殊注意事项。提供清晰的解释：在呈现您的分析或建议时，请确保为您的结论提供清晰的解释。通过参考相关信息和医学原则来证明您的选择或建议。这将帮助患者理解您建议的背后推理，并对他们的健康做出明智的决定。通过遵循这些指导方针，您将能够有效地分析所提供的信息并提供准确而专业的医疗建议。请记住，在您的回答中始终将患者的健康和最佳利益置于首位。"

filename = "D:/LLMdata/pubmed/ori_pqaa (1).json"  # 请将文件名替换为实际的 JSON 文件名

reader = JsonDataReader(filename)
random_objects = reader.get_random_objects(2)
results = []

for data in random_objects:
    question=data.question
    text=data.contexts
    long_answer=data.long_answer
    final_answer=data.final_decision


    prompt_generator = AnsPromptGenerator(my_prompt + " " + "文本, {text}" + " " + question)
    prompt = prompt_generator.generate_prompt(question)
    
    # 使用 prompt 获取完成
    response = get_completion(prompt)
    
    # 创建结果字典
    result_entry = {
        "question": question,
        "generated_answer": response,
        "answer": long_answer,
        "final_answer": final_answer
    }
    
    # 将结果字典添加到结果列表中
    results.append(result_entry)

# 将结果列表写入 JSON 文件
output_file_path="D:LLMdata/test_acc/Pubmed_new.json"
with open(output_file_path, "w") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)