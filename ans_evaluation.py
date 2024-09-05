from bert_score import score


sentence="根据提供的文本内容，病人的精索静脉曲张属于一度曲张。"
sentence1 = "  应该属于临床Ⅱ度曲张，即外观看不到曲张静脉，但触诊较明显，摒气动作（valsava）时更加明显。平卧后曲张静脉消失，考虑为原发性精索静脉曲张。"
sentence2 = "Based on the provided information, the patient is a 22-year-old male who has been experiencing left scrotal discomfort and swelling for over a year. The symptoms worsen after prolonged standing or physical activity but improve with rest in a supine position. The semen analysis indicates oligoasthenozoospermia (low sperm count and poor sperm motility). \n\nDuring physical examination, there is no abnormality observed in the appearance of the left scrotum. However, upon palpation, a worm-like structure can be felt above the left testicle in the spermatic cord. The symptoms are exacerbated with the Valsalva maneuver but disappear when lying down. The left testicle is of normal size but has a softer texture. No abnormalities are detected in the left epididymis. Abdominal examination is unremarkable, with no tenderness or rebound tenderness.\n\nThe laboratory findings from at least two semen analyses show a semen volume of 3ml, a sperm density of 38 million/ml, with 4.6% A-grade sperm, 20.5% B-grade sperm, 10.3% C-grade sperm, and 64.6% D-grade sperm. The semen liquefaction time is normal.\n\nDoppler ultrasound examination reveals that the left spermatic vein has an inner diameter of 0.36cm. The Valsalva maneuver shows reflux, and there is widening of a tubular structure. No abnormalities are observed in the right spermatic vein.\n\nBased on the provided information, the patient's left spermatic vein varicocele can be classified as grade 2 varicocele. This is determined by the presence of a worm-like structure above the left testicle, the exacerbation of symptoms with the Valsalva maneuver, and the widening of the tubular structure observed on Doppler ultrasound."

# data
cands = [sentence]
refs = [sentence1]

P, R, F1 = score(cands, refs, lang="zn", verbose=True)

print(f"System level F1 score: {F1.mean():.3f}") 

cands = [sentence2]
refs = [sentence1]

P, R, F1 = score(cands, refs, lang="others", verbose=True)

print(f"System level F1 score: {F1.mean():.3f}") 


import matplotlib.pyplot as plt

font = {'family': 'SimHei', 'size':'10'}
plt.rc('font', **font)
plt.show()

from bert_score import plot_example

cand = sentence
ref = sentence1
plot_example(cand, ref, lang="zh")
