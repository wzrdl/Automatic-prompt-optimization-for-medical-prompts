# -*- coding: utf-8 -*-
import re
from nltk.translate.bleu_score import sentence_bleu
def calculate_overlap_ratio(sentence1, sentence2,sentence):

    sentence1 = re.sub(r'[^\w\s]', '', sentence1.lower())
    sentence2 = re.sub(r'[^\w\s]', '', sentence2.lower())
    sentence =  re.sub(r'[^\w\s]', '', sentence.lower())
    # 将句子转换为小写，去除空格
    sentence1 = sentence1.lower().split()
    #print(sentence1)
    sentence2 = sentence2.lower().split()
    #print(sentence2)
    sentence = sentence.lower().split()

    

    reference = [sentence1]
    candidate = sentence2

    bleu_score = sentence_bleu(reference, candidate)
    print("BLEU Score:", bleu_score)

    candidate = sentence

    bleu_score = sentence_bleu(reference, candidate)
    print("BLEU Score:", bleu_score)

    # 初始化一个计数器，用于记录第二个句子中包含了第一个句子中多少内容的字符数量
    overlap_count = 0
    
    # 遍历第一个句子中的每个字符
    for char in sentence1:
        # 如果第二个句子中的字符也在第一个句子中出现，则计数器加一
        if char in sentence2:
            overlap_count += 1
            continue
    print(overlap_count)
    # 计算重叠比例
    overlap_ratio = overlap_count / len(sentence1)
    
    return overlap_ratio

# 示例用法
sentence="\nYou are now a doctor with extensive medical knowledge and clinical experience. You excel in diagnosing and treating various diseases and can provide professional medical advice to patients. As you approach this problem, your first step is to analyze the information provided in the text and relate it to the relevant field based on the questions asked. If it is a multiple-choice question, use the information you have gathered to consider each option and determine if it is a viable choice, providing your reasoning for each option. Finally, provide your answer.\n\nTo ensure a more effective assessment of your abilities, we have made the following modifications to address the previous problems and advice:\n\n1. Clearly state the objective: The objective of this task is to analyze the given information and provide a reasoned answer or solution. You should demonstrate your thought process and reasoning behind your answer.\n\n2. Provide accurate and complete information: The prompt will provide accurate and complete information to ensure you have all the necessary details to make an informed analysis.\n\n3. Encourage critical thinking: The prompt will encourage you to think critically and analyze the information provided. Specific questions or prompts will guide your analysis process.\n\nBy addressing these issues, we aim to improve the prompt and better assess your ability to analyze medical information and provide accurate answers or solutions. Your task is to carefully analyze the information provided, think critically, and provide your well-reasoned answer or solution. Good luck!\n"
sentence1 = " nYou are now a doctor with extensive medical knowledge and clinical experience. You excel in diagnosing and treating various diseases and can provide professional medical advice to patients. As you approach this problem, your first step is to analyze the information provided in the text and relate it to the relevant field based on the questions asked. If it is a multiple-choice question, use the information you have gathered to consider each option and determine if it is a viable choice, providing your reasoning for each option. Finally, provide your answer.\n\nTo ensure a more effective assessment of your abilities, we have made the following modifications to address the previous problems and advice:\n\n1. Clearly state the objective: The objective of this task is to analyze the given information and provide a reasoned answer or solution. You should demonstrate your thought process and reasoning behind your answer.\n\n2. Provide accurate and complete information: The prompt will provide accurate and complete information to ensure you have all the necessary details to make an informed analysis. This includes relevant medical history, physical examination findings, and diagnostic test results.\n\n3. Encourage critical thinking: The prompt will encourage you to think critically and analyze the information provided. Specific questions or prompts will guide your analysis process and require you to consider different possibilities and explanations.\n\nBy addressing these issues, we aim to improve the prompt and better assess your ability to analyze medical information and provide accurate answers or solutions. Your task is to carefully analyze the information provided, think critically, and provide your well-reasoned answer or solution. Good luck!\n"
sentence2="\nYou are now a doctor with extensive medical knowledge and clinical experience. You excel in diagnosing and treating various diseases and can provide professional medical advice to patients. As you approach this problem, your first step is to analyze the information provided in the text and relate it to the relevant field based on the questions asked. If it is a multiple-choice question, use the information you have gathered to consider each option and determine if it is a viable choice, providing your reasoning for each option. Finally, provide your answer.\n\nTo ensure a more effective assessment of your abilities, we have made the following modifications to address the previous problems and advice:\n\n1. Clearly state the objective: The objective of this task is to analyze the given information and provide a reasoned answer or solution. You should demonstrate your thought process and reasoning behind your answer.\n\n2. Provide accurate and complete information: The prompt will provide accurate and complete information to ensure you have all the necessary details to make an informed analysis. This includes relevant medical history, physical examination findings, and diagnostic test results.\n\n3. Encourage critical thinking: The prompt will encourage you to think critically and analyze the information provided. Specific questions or prompts will guide your analysis process and require you to consider different possibilities and explanations.\n\nBy addressing these issues, we aim to improve the prompt and better assess your ability to analyze medical information and provide accurate answers or solutions. Your task is to carefully analyze the information provided, think critically, and provide your well-reasoned answer or solution. Good luck!\n"
overlap_ratio = calculate_overlap_ratio(sentence1, sentence2, sentence)
print("第二个句子中包含了第一个句子中 {:.2%} 的内容。".format(overlap_ratio))

from rouge import Rouge

reference = sentence1
candidate = sentence2

rouge = Rouge()
scores = rouge.get_scores(candidate, reference)
print("ROUGE Scores:", scores)

reference = sentence1
candidate = sentence

rouge = Rouge()
scores = rouge.get_scores(candidate, reference)
print("ROUGE Scores:", scores)

