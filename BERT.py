from bert_score import score as bert_score
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
import csv

class BertScoreEvaluator:
    def __init__(self):
        pass

    def score_sentences(self, candidate, reference, lang="others", verbose=False):
        """
        Score a single candidate sentence against a single reference sentence.
        
        Args:
            candidate (str): The candidate sentence.
            reference (str): The reference sentence.
            lang (str): Language of the sentences. Defaults to "en" (English).
            verbose (bool): Whether to print verbose output. Defaults to False.
        
        Returns:
            tuple: Precision, Recall, and F1 score.
        """
        P, R, F1 = bert_score([candidate], [reference], lang=lang, verbose=verbose)
        return P.item(), R.item(), F1.item()

    def score_system(self, candidates, references, lang="others", verbose=False):
        """
        Score a list of candidate sentences against a list of reference sentences.

        Args:
            candidates (list): List of candidate sentences.
            references (list): List of reference sentences.
            lang (str): Language of the sentences. Defaults to "en" (English).
            verbose (bool): Whether to print verbose output. Defaults to False.

        Returns:
            float: System-level F1 score.
        """
        P, R, F1 = bert_score(candidates, references, lang=lang, verbose=verbose)
        return F1.mean().item()
    

# 创建一个CSV文件并写入数据
def save_variables_to_csv(filename, headers, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # 写入标签
        writer.writerows(data)   # 写入数据

# Example usage
if __name__ == "__main__":
    evaluator = BertScoreEvaluator()

    # 初始化一个空列表来收集数据
    all_data = []
    
    file_path_old = 'D:/LLMdata/CMB/CMB-Clin/diagnose.json'  # 替换为你的文件路径
    analyzer_old = CaseAnalyzer(file_path_old)
    file_path_new = 'D:/LLMdata/CMB/CMB-Clin/diagnosenew.json'  # 替换为你的文件路径
    analyzer_new= CaseAnalyzer(file_path_new)
    for i in range(47):
        case = analyzer_old.analyze_case(i)
        error_answer_old = case.get_answer()
        true_answer = case.get_true_answer()

        case2 = analyzer_old.analyze_case(i)
        error_answer_new = case2.get_answer()
        
        """
        sentence = "根据提供的文本内容，病人的精索静脉曲张属于一度曲张。"
        sentence1 = "应该属于临床Ⅱ度曲张，即外观看不到曲张静脉，但触诊较明显，摒气动作（valsava）时更加明显。平卧后曲张静脉消失，考虑为原发性精索静脉曲张。"
        sentence2 = "Based on the provided information, the patient is a 22-year-old male who has been experiencing left scrotal discomfort and swelling for over a year. The symptoms worsen after prolonged standing or physical activity but improve with rest in a supine position. The semen analysis indicates oligoasthenozoospermia (low sperm count and poor sperm motility). \n\nDuring physical examination, there is no abnormality observed in the appearance of the left scrotum. However, upon palpation, a worm-like structure can be felt above the left testicle in the spermatic cord. The symptoms are exacerbated with the Valsalva maneuver but disappear when lying down. The left testicle is of normal size but has a softer texture. No abnormalities are detected in the left epididymis. Abdominal examination is unremarkable, with no tenderness or rebound tenderness.\n\nThe laboratory findings from at least two semen analyses show a semen volume of 3ml, a sperm density of 38 million/ml, with 4.6% A-grade sperm, 20.5% B-grade sperm, 10.3% C-grade sperm, and 64.6% D-grade sperm. The semen liquefaction time is normal.\n\nDoppler ultrasound examination reveals that the left spermatic vein has an inner diameter of 0.36cm. The Valsalva maneuver shows reflux, and there is widening of a tubular structure. No abnormalities are observed in the right spermatic vein.\n\nBased on the provided information, the patient's left spermatic vein varicocele can be classified as grade 2 varicocele. This is determined by the presence of a worm-like structure above the left testicle, the exacerbation of symptoms with the Valsalva maneuver, and the widening of the tubular structure observed on Doppler ultrasound."

        """
        sentence1=true_answer
        sentence=error_answer_old
        sentence2=error_answer_new

        # Score individual sentences
        P, R, F1 = evaluator.score_sentences(sentence, sentence1, lang="zh", verbose=True)
        P_others, R_others, F1_others = evaluator.score_sentences(sentence2, sentence1, lang="others", verbose=True)

        # Score system-level sentences
        F1_system = evaluator.score_system([sentence], [sentence1], lang="zh", verbose=True)
        F1_system_en = evaluator.score_system([sentence2], [sentence1], lang="en", verbose=True)

        # 标签行
        headers = ['Precision', 'Recall', 'F1', 'System F1 score', 'Precision (others)', 'Recall (others)', 'F1 (others)', 'System F1 score (en)']

        # 数据行
        data = [
            [P, R, F1, F1_system, P_others, R_others, F1_others, F1_system_en]
        ]
                
        # 收集当前迭代的数据
        iteration_data = [P, R, F1, F1_system, P_others, R_others, F1_others, F1_system_en]

        # 将当前迭代的数据添加到全部数据列表中
        all_data.append(iteration_data)

    # 标签行
    headers = ['Precision', 'Recall', 'F1', 'System F1 score', 'Precision (others)', 'Recall (others)', 'F1 (others)', 'System F1 score (en)']

    # 保存到CSV文件
    save_variables_to_csv('D:LLMdata/test_acc/diagnoseF1.csv', headers, all_data)