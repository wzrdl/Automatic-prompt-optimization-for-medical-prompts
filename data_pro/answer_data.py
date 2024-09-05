import json

class CaseAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze_case(self, target_id):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                
            for item in json_data:
                if item.get('id') == target_id:
                    case = self._parse_case(item)
                    return case
            print(f"ID {target_id} not found.")
            return None
        except FileNotFoundError:
            print("File not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return None

    def _parse_case(self, data):
        case_id = data["id"]
        question = data["问题"]
        true_answer = data["答案"]
        text=data["文本信息"]
        prompt = data["生成的提示"]
        answer=data["完成结果"]
        return CaseAnalysis(case_id, question, true_answer, prompt,answer,text)
    
class CaseAnalysis:
    def __init__(self, case_id, question, true_answer, prompt,answer,text):
        self.id = case_id
        self.question = question
        self.true_answer = true_answer
        self.prompt = prompt
        self.answer=answer
        self.text=text
    def get_question(self):
        return self.question
    def get_true_answer(self):
        return self.true_answer
    def get_prompt(self):
        return self.prompt
    def get_answer(self):
        return self.answer
    def get_text(self):
        return self.text



'''
# 使用示例
file_path = 'D:/LLMdata/CMB/CMB-Clin/answer.json' # 替换为你的文件路径
analyzer = CaseAnalyzer(file_path)
target_id = 1  # 替换为你要提取的 ID
case = analyzer.analyze_case(target_id)
print(type(case))
print(case.get_question())

print(case.get_true_answer())

print(case.get_answer())

print(case.get_prompt())
'''


