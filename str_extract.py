import re

class StringExtractor:
    def __init__(self, input_string):
        self.input_string = input_string

    def extract_between_tags(self):
        pattern = r'<START>(.*?)<END>'
        match = re.search(pattern, self.input_string,re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None


"""
# 示例用法
input_string = "'<START>\nThe false examples provided in the prompt have several common mistakes:\n1. They provide incorrect answers to the questions asked. In all of the examples, the given answers do not match the correct answers.\n2. The explanations provided for the incorrect answers are not accurate or logical. They do not properly analyze the information provided in the text or consider the relevant medical knowledge.\n3. The examples do not follow a consistent format or structure. Some examples provide a detailed analysis of the information, while others only give a brief explanation.\n\nTo improve the prompt, here are some suggestions:\n1. Clearly state the question being asked in each example. This will help the reader understand what they need to analyze and answer.\n2. Provide accurate and logical explanations for the correct answers. Make sure to consider all the relevant information and medical knowledge when analyzing the text.\n3. Use a consistent format and structure for each example. This will make it easier for the reader to follow and understand the analysis process.\n\n<END>'"
extractor = StringExtractor(input_string)
result = extractor.extract_between_tags()
print("提取的部分是:", result)

"""



