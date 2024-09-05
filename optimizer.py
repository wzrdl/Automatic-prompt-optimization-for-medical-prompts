import _init_
from _init_ import get_completion
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate


class PromptGenerator:
    def __init__(self):
        self.template =  """Your task is to integrate the problems in the previous
            prompt and the current prompt, to make the current prompt better perform.
            Below are the problems that arose from the
            previous prompts. {previous_problem}
            according to previous problem, write a new version of {old_prompt}
            You are allowed to change up to {step} words in the "old prompt" and replace the old prompt 
            with the "new prompt".
            Wrap the "new prompt" with <START> and <END>.
            """

    def generate_prompt(self, previous_problem, old_prompt, step):
        cat_prompt = PromptTemplate.from_template(self.template)
        prompt_template = cat_prompt.format(previous_problem=previous_problem, old_prompt=old_prompt, step=step)
        return prompt_template

"""
prompt_generator = PromptGenerator()
previous_problem = "提示语可能会弄错这些示例的一个原因是，它没有为给定文本提供足够的背景信息或语境。背景信息或语境。提示假定读者事先已经了解和理解医学领域的知识以及与主题相关的具体细节。但是，如果没有足够的背景信息，就很难准确分析给定文本并提供正确答案。此外，提示 多选题中的选项没有具体的评估标准或指导原则，导致预期答案与实际答案不一致。"
old_prompt = "作为一名拥有丰富医学知识和临床经验的医生，您善于诊断和治疗各种疾病，并为患者提供专业的医疗建议。然而，要准确分析给定文本并提供正确答案，就必须了解提示中指出的医学领域或专业的具体信息。此外，有关问题主题的背景信息和相关细节也是全面分析的关键。仔细分析前面的提示，结合相关领域考虑所提供的文本，如果是多选题，则对每个选项进行评估，以做出有理有据的答案。最后，通过分析收集到的信息并做出适当的结论来给出答案。"
step = "1000"
prompt = prompt_generator.generate_prompt(previous_problem, old_prompt, step)
print("Generated Prompt:", prompt)

# Now you can use this prompt to get completion as you were doing before
response = get_completion(prompt)
print("Result type:", type(response))
print("Result:", response)
"""




