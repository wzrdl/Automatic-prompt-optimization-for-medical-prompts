import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate


class AnsPromptGenerator:
    def __init__(self,temp):
        self.template = temp

    def generate_prompt(self, text):
        cat_prompt = PromptTemplate.from_template(self.template)
        prompt_template = cat_prompt.format(text=text)
        return prompt_template

"""
text=""
new_prompt=""
prompt_generator = AnsPromptGenerator(new_prompt)
prompt = prompt_generator.generate_prompt(text)
print("Generated Prompt:", prompt)

# Now you can use this prompt to get completion as you were doing before
response = get_completion(prompt)
print("Result type:", type(response))
print("Result:", response)
"""




