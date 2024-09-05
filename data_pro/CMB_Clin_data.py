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
        title = data["title"]
        description = data["description"]
        qa_pairs = data["QA_pairs"]
        return CaseAnalysis(case_id, title, description, qa_pairs)

class CaseAnalysis:
    def __init__(self, case_id, title, description, qa_pairs):
        self.id = case_id
        self.title = title
        self.description = description
        self.qa_pairs = qa_pairs

    def get_patient_history(self):
        return self.description

    def get_question_answers(self):
        return [(qa["question"], qa["answer"]) for qa in self.qa_pairs]


"""
# 示例用法
file_path = "D:/LLMdata/CMB/CMB-Clin/CMB-Clin-qa.json"
analyzer = CaseAnalyzer(file_path)
target_id = '1'  # 替换为你要提取的 ID
case = analyzer.analyze_case(target_id)
print(type(case))

if case:
    # 获取病人病史
    patient_history = case.get_patient_history()
    print("病人病史：", patient_history)

    # 获取问题及答案
    question_answers = case.get_question_answers()
    for question, answer in question_answers:
        print("问题:", question)
        print("答案:", answer)
"""



