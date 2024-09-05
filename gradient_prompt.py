import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from data_pro.answer_data import CaseAnalyzer, CaseAnalysis
from str_extract import StringExtractor
from optimizer import PromptGenerator
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
gradient_template = """
        Your task is to point out the problems with the current prompt based on the wrong
        examples. The current prompt is: {current} But this prompt gets the following examples
        wrong.You should analyze the differences between wrong predictions and ground truth
        answers, and carefully consider why this prompt led to incorrect predictions. Below are
        the task examples with Queston, Wrong prediction, and Ground truth answer. {error}
        {analyze}

        """


current_template = """你现在是一名医生，具备丰富的医学知识和临床经验。你擅长诊断和治疗各种疾病，能为病人提供专业
    的医疗建议。在你思考这个问题的时候，首先要梳理提供的文本内容分析提供的信息，并且根据提出的问题对应到相关的领域，
    如果是选择题，先根据之前整理出来的信息，对于每一个选项逐步思考能否选择该选项及其理由。最后告诉我答案。
    如果不是选择题，那么需要你根据整理出来的信息逐步分析, 最后回答问题。"""
error_template = """here are some examples, {false_sentence}."""
analyze_template = """
        First find whether the false example give answers, Give reasons why the prompt could have
        gotten these examples have wrong answer, do not analyze each example in detail, just
        give common mistakes these examples have made.
        Wrap the mistakes with <START> and <END>.
        """



# Start iteration
file_path = 'D:/LLMdata/CMB/CMB-Clin/'  # 替换为你的文件路径
output_directory = 'D:/LLMdata/CMB/CMB-Clin/'  # 替换为你的输出目录路径
count = 1
iteration_time=1
for k in range(5):  # 循环5次
    error_generate = []
    file_path_now=os.path.join(file_path, f"else{k}.json")
    analyzer = CaseAnalyzer(file_path_now)
    prompt_template=" "
    for i in range(15,20):
        case = analyzer.analyze_case(i)
        error_answer = "error answer" + " " + case.get_answer()
        true_answer = "true answer" + " " + case.get_true_answer()
        prompt_template=case.get_prompt()
        count_string = "example: {}".format(count)
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
    #第一次get
    response = get_completion(messages)




    extractor = StringExtractor(response)
    result = extractor.extract_between_tags()
    print(result)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    prompt_generator = PromptGenerator()
    previous_problem = result
    if k==0:
        old_prompt=current_template
    else:
        old_prompt = prompt_template
    step = "400"
    prompt = prompt_generator.generate_prompt(previous_problem, old_prompt, step)

    response = get_completion(prompt)

    extractor = StringExtractor(response)
    result = extractor.extract_between_tags()
    print(result)

    generated_content = []
    file_path_now=os.path.join(file_path, f"else{k}.json")
    analyzer = CaseAnalyzer(file_path_now)
    for i in range(15,20):
        case = analyzer.analyze_case(i)
        question = case.get_question()
        answer = case.get_true_answer()
        patient_text = case.get_text()
        new_prompt = result + "" + "文本: {text}" + " " + question
        prompt_generator = AnsPromptGenerator(new_prompt)
        prompt = prompt_generator.generate_prompt(patient_text)
        response = get_completion(prompt)
        content = {
            "id": i,  # 假设问题有编号
            "问题": question,
            "答案": answer,
            "文本信息": patient_text,
            "生成的提示": result,
            "完成结果": response
        }
        generated_content.append(content)

    filename = f"else{iteration_time}.json"
    output_file_path = os.path.join(output_directory, filename)
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(generated_content, output_file, ensure_ascii=False, indent=4)
    iteration_time+=1
    print("数据处理完成，并已写入到文件:", output_file_path)
