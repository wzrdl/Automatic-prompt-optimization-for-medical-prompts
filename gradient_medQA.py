import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from str_extract import StringExtractor
from optimizer import PromptGenerator
from data_pro.MedQA_test  import JSONDataExtractor
import json
import os
from for_ans import AnsPromptGenerator

class GDprompt:
    def __init__(self):
        self.gradient_prompt = None
        self.current_prompt = None
        self.error_prompt = None
        self.analyze_prompt = None
        self.pipeline_prompt = None

    def set_gradient_prompt(self, gradient_prompt_template):
        self.gradient_prompt = PromptTemplate.from_template(gradient_prompt_template)

    def set_current_prompt(self, current_prompt_template):
        self.current_prompt = PromptTemplate.from_template(current_prompt_template)

    def set_error_prompt(self, error_prompt_template):
        self.error_prompt = PromptTemplate.from_template(error_prompt_template)

    def set_analyze_prompt(self, analyze_prompt_template):
        self.analyze_prompt = PromptTemplate.from_template(analyze_prompt_template)

    def initialize_pipeline_prompt(self):
        if all([self.gradient_prompt, self.current_prompt, self.error_prompt, self.analyze_prompt]):
            input_prompts = [
                ("current", self.current_prompt),
                ("error", self.error_prompt),
                ("analyze", self.analyze_prompt)
            ]
            self.pipeline_prompt = PipelinePromptTemplate(final_prompt=self.gradient_prompt, pipeline_prompts=input_prompts)
        else:
            raise ValueError("All prompt templates must be set before initializing the pipeline.")

    def generate_messages(self, false_sentence):
        if not self.pipeline_prompt:
            raise ValueError("Pipeline prompt must be initialized before generasting messages.")
        return self.pipeline_prompt.format(false_sentence=false_sentence)

# Example usage
gradient_template = """Your task is to point out the problems with the
        current prompt based on the wrong examples.
        The current prompt is: {current} But this prompt gets the following examples wrong. 
        you should You should analyze why there are discrepancies between these outputs 
        and the actual answers {error}
        
        {analyze}
        """


current_template = """从文本中提取患者的信息作为条件，形如条件1,2,3,4，然后看信息之间的关联性，关联性强的就合并，并重新编号

第一步，你现在只有条件1，2,3，不允许考虑其他任何条件，给出一个0到0.5之间的数字，表示只在条件1的\
信息下选择每个选项的概率，对每个选项都解释给出该数字的理由，如果概率很小就给一个比较接近0的数，不要给0，如果概\
率比较大就给一个比较接近0.5的数。\

记住要把严重的疾病优先考虑\
第二步，结合你拥有的知识，以一个专业医生的视角，告诉我每一个条件可能的原因，不要漏掉任何一个条件以及数据。\
给出一个0到1之间数字，表示在患者的所有条件下选择每个选项的概率，对每个选项都解释给出该数\
字的理由，尽可能的详细分析每一个条件，如果概率很小就给一个比较接近0的数，不要给0，如果概\
    率很大就给一个比较接近1的数\

最后将每个选项得到的这两个概率相乘，并选出概率最大的选项。"""

error_template = """here are some examples, {false_sentence}."""
analyze_template = """
        First find whether the false example give answers, Give reasons why the prompt could have
        gotten these examples have wrong answer, do not analyze each example in detail, just
        give common mistakes these examples have made, and advices to modify my current prompt .
        Wrap the reason and advices with <START> and <END>.
        """



# Start iteration

output_directory = 'D:/LLMdata/test_acc'  # 替换为你的输出目录路径
count = 1
iteration_time=1
file_path = 'D:/LLMdata/test_acc/'  # 替换为你的文件路径


for k in range(5):  # 循环5次
    error_generate = []
    file_path_new=os.path.join(file_path, f"medQA_old{k}.json")
    data_extractor = JSONDataExtractor(file_path_new)
    random_jsonl_data = data_extractor.get_random_jsonl_data(8)
    prompt_template=" "
    for data in random_jsonl_data:
        question=data_extractor.get_question(data)
        error_answer = "error answer" + " " + data_extractor.get_error_answer(data)
        true_answer = "true answer" + " " + data_extractor.get_answer(data)
        options = data_extractor.get_options(data)
        count_string = "example: {}".format(count)
        prompt_template=data_extractor.get_prompt(data)
        error_generate.append(count_string + " " + error_answer + " " + true_answer)
        count += 1

    gd_prompt = GDprompt()
    gd_prompt.set_gradient_prompt(gradient_template)
    if k==0:
        gd_prompt.set_current_prompt(current_template)
    else:
        gd_prompt.set_current_prompt(prompt_template)
    gd_prompt.set_error_prompt(error_template)
    gd_prompt.set_analyze_prompt(analyze_template)
    gd_prompt.initialize_pipeline_prompt()
    messages = gd_prompt.generate_messages(false_sentence=error_generate)
    response = get_completion(messages)

    extractor = StringExtractor(response)
    result = extractor.extract_between_tags()
    print(result)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    prompt_generator = PromptGenerator()
    previous_problem = result
    if k==0:
        old_prompt=current_template
    else:
        old_prompt=prompt_template
    step = "10000"
    prompt = prompt_generator.generate_prompt(previous_problem, old_prompt, step)

    response = get_completion(prompt)

    extractor = StringExtractor(response)
    result = extractor.extract_between_tags()
    print(result)


    generated_content = []
    file_path = 'D:/LLMdata/test_acc/'  # 替换为你的文件路径
    file_path_new=os.path.join(file_path, f"medQA_old{k}.json")
    data_extractor = JSONDataExtractor(file_path_new)
    random_jsonl_data = data_extractor.get_random_jsonl_data(8)
    for data in random_jsonl_data:
        #
        question = data_extractor.get_question(data)
        answer = data_extractor.get_answer(data)
        options = data_extractor.get_options(data)
        meta_info = data_extractor.get_meta_info(data)
        answer_idx = data_extractor.get_answer_idx(data)
        text = question+ " " + options
        prompt_generator = AnsPromptGenerator(result + " " + "文本, {text}" )
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
            "prompt" : result
        }
        generated_content.append(result_entry)

    filename = f"medQA_old{iteration_time}.json"
    output_file_path = os.path.join(output_directory, filename)
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(generated_content, output_file, ensure_ascii=False, indent=4)
    iteration_time+=1
    print("数据处理完成，并已写入到文件:", output_file_path)
