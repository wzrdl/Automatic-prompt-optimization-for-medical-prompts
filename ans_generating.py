import _init_
import json
from langchain.prompts import ChatPromptTemplate
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from data_pro.CMB_Clin_data import CaseAnalyzer,CaseAnalysis
import os

class PromptProcessor:
    def __init__(self, templates):
        self.templates = templates

    def process_prompt(self, question, text):
        # 根据问题或文本内容选择不同的模板
        if "诊断" in question:
            template = self.templates["template1"]
        elif "治疗原则" in question:
            template = self.templates["template2"]
        elif "检查" in question:
            template = self.templates["template3"]   
        else:
            template = self.templates["default_template"]

        prompt_template = ChatPromptTemplate.from_template(template)
        messages = prompt_template.format(text=text)
        return messages

# Example usage

review_templates = {
    "template1": """\
    \nAs a doctor with extensive medical knowledge and clinical experience, your task is to carefully analyze the provided information and provide a thorough and evidence-based analysis and diagnosis. In order to improve the prompt, it is important to address the problems and advices that arose from the previous prompts.\n\nThe false examples provided in the previous prompts had several common mistakes that need to be avoided:\n\n1. Incorrect diagnosis: Ensure that your diagnosis reflects your expertise and understanding of the symptoms. Consider all possible diagnoses and avoid jumping to conclusions without thorough analysis.\n\n2. Lack of thorough analysis: Take the time to thoroughly analyze the provided information, considering all relevant factors and conducting further tests or examinations if necessary. Demonstrate critical thinking and problem-solving skills in your analysis.\n\n3. Failure to consider differential diagnoses: Include a comprehensive list of potential conditions based on the given information. Consider multiple possible diagnoses and explain your reasoning for each.\n\n4. Lack of evidence-based reasoning: Support your analysis and diagnoses with specific evidence from the text. Reference symptoms, test results, or medical literature to provide a strong rationale for your conclusions.\n\nTo improve the prompt, consider the following modifications:\n\n1. Clarify the expectations: Clearly state that your analysis should be based on evidence from the provided text and should consider all relevant factors, including symptoms, medical history, and test results.\n\n2. Emphasize the importance of differential diagnoses: Highlight the need to consider multiple possible diagnoses and provide a comprehensive list of potential conditions based on the given information.\n\n3. Encourage evidence-based reasoning: Prompt you to provide specific evidence or reasoning to support your analysis and diagnoses. Reference specific symptoms, test results, or medical literature to strengthen your conclusions.\n\n4. Provide guidance on critical thinking: Include prompts or questions that encourage critical thinking and problem-solving skills. This will help you analyze the information more thoroughly and consider all possible factors before reaching a conclusion.\n\nWith these improvements in mind, carefully analyze the provided information and provide a thorough and evidence-based analysis and diagnosis. Remember to consider all relevant factors, provide a comprehensive list of potential diagnoses, and support your conclusions with specific evidence and reasoning. 文本: {text}
    """,
    "template2": """\
    \nAs a highly skilled and experienced doctor, you possess a wealth of medical knowledge and clinical expertise. Your proficiency lies in diagnosing and treating various diseases, enabling you to provide professional medical advice to patients. When approaching a problem, it is crucial to carefully analyze the information provided in the text and correlate it with the relevant field based on the questions posed.\n\nTo ensure clarity and accuracy in your responses, it is important to address the following issues that have been identified in previous prompts:\n\n1. Clearly state the task or question that needs to be answered. Specify the objective of the analysis and the specific questions that require a response. This will provide a clear direction for your evaluation and prevent confusion or incorrect answers.\n\n2. Provide sufficient context and information for the examples. Include relevant details about the patient's medical history, physical examination findings, and any diagnostic tests or results. This additional information will enable you to make accurate diagnoses and formulate appropriate treatment plans.\n\n3. Specify the format of the expected answers. Clearly indicate whether the responses should be in the form of multiple-choice options or written explanations. Provide guidelines on the necessary components to include in the answers, such as relevant symptoms, diagnostic criteria, and treatment options.\n\nBy addressing these concerns, you can enhance the prompt and provide clearer instructions and context for the model. This will result in more accurate and informative answers, enabling you to effectively utilize your medical expertise and provide valuable insights to patients.\n\nNow, with these improvements in mind, carefully analyze the provided text and answer the questions accordingly. Remember to consider the relevant information, evaluate each option (if applicable), and provide a well-reasoned response. 文本: {text}
    """,
    "template3": """\
    \nAs a highly skilled and experienced doctor, you possess a wealth of medical knowledge and clinical expertise. Your proficiency lies in diagnosing and treating various diseases, and providing professional medical advice to patients. In order to effectively address the given problem, it is crucial to carefully analyze the provided text and extract relevant information. Additionally, it is important to correlate the presented questions with the appropriate medical field. If the question is a multiple-choice format, utilize the organized information to systematically evaluate each option and determine its suitability, providing supporting reasons. Finally, provide a definitive answer. If the question is not in a multiple-choice format, systematically analyze the compiled information and provide a comprehensive response to the question at hand.\n\nTo enhance the clarity and effectiveness of the prompt, it is essential to provide specific context and background information about the patients and their conditions. This will enable the model to accurately analyze the given text and provide appropriate answers. Furthermore, the prompt should clearly state the task or question that needs to be answered, ensuring that the model understands the objective. \n\nFor instance, the revised prompt could be: \"Based on the provided text, carefully analyze the symptoms, medical history, and test results of the patient to accurately diagnose their condition. Provide a detailed explanation of your diagnosis, including any further tests or treatments that may be necessary. Finally, offer professional medical advice to the patient.\"\n\nBy incorporating these improvements, the prompt will provide the necessary context, clarity, and guidance for the model to effectively analyze the text and generate accurate responses.\n文本: {text}
    """,
    "default_template": """\
    \nAs a doctor with extensive medical knowledge and clinical experience, your task is to analyze the provided information and provide professional medical advice to patients. In order to effectively approach this task, it is important to follow these steps:\n\n1. Analyze the information: Carefully review the text and identify the relevant details and key points. Take note of any symptoms, medical history, or other pertinent information that may be important for diagnosis or treatment.\n\n2. Understand the context: To better understand the relevance of the information provided, it is essential to have some background context. Familiarize yourself with the scenarios or patients involved, including their age, gender, lifestyle, and any other relevant factors that may impact their health.\n\n3. Determine the specific questions: Clearly identify the specific questions that need to be answered or the type of analysis that needs to be conducted. This will help guide your thinking and ensure that you address all the necessary aspects.\n\n4. Conduct a thorough analysis: When answering questions or providing medical advice, consider all the available information and apply your medical knowledge and clinical experience. Evaluate the options or potential treatment plans based on their feasibility, effectiveness, and potential risks or side effects. Consider any contraindications or specific considerations for the patient's condition.\n\n5. Provide clear explanations: When presenting your analysis or advice, ensure that you provide clear explanations for your conclusions. Justify your choices or recommendations by referencing the relevant information and medical principles. This will help the patient understand the reasoning behind your advice and make informed decisions about their health.\n\nBy following these guidelines, you will be able to effectively analyze the information provided and provide accurate and professional medical advice. Remember to always prioritize the well-being and best interests of the patients in your responses.\n\n文本: {text}
    """
}

file_path = "D:/LLMdata/CMB/CMB-Clin/CMB-Clin-qa.json"
# Initialize a dictionary to store processed data for different categories
processed_data = {
    "diagnose": [],
    "cure": [],
    "check": [],
    "else": []
}
analyzer = CaseAnalyzer(file_path)

for i in range(0,50):
    target_id = str(i)  # 替换为你要提取的 ID
    case = analyzer.analyze_case(target_id)
    
    patient_history = case.get_patient_history()

    question_answers = case.get_question_answers()
    for question, answer in question_answers:
        #print("问题:", question)
        #print("答案:", answer)

        # 使用 PromptProcessor 处理提示
        processor = PromptProcessor(review_templates)
        patient_history=patient_history+""+question
        messages = processor.process_prompt(question, patient_history)
        #print("Generated Prompt:", messages)

        # 现在可以使用这个提示来获取完成
        response = get_completion(messages)
        print("Result type:", type(response))
        print("Result:", response)
        # 将原始数据、生成的提示和结果添加到processed_data列表中
        if "诊断" in question:
            category = "diagnose"
        elif "治疗原则" in question:
            category = "cure"
        elif "检查" in question:
            category = "check"
        else:
            category = "else"

        processed_data[category].append({
            "id": len(processed_data[category]),
            "问题": question,
            "答案": answer,
            "文本信息": patient_history,
            "生成的提示": messages,
            "完成结果": response
        })


# Store processed data into separate JSON files based on categories
for category, data in processed_data.items():
    filename = f"{category}new.json"
    output_file_path = os.path.join("D:/LLMdata/CMB/CMB-Clin/", filename)
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

print("数据处理完成，并已写入到文件:", output_file_path)