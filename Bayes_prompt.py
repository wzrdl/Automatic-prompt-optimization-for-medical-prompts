'''


{"question": "男，67岁。反复咳嗽、咳痰30年，加重1周。\
    查体：双肺可闻及干湿性啰音。动脉血气分析示：pH 7.21，PaCO2 75mmHg，PaO2 50mmHg，HCO3－ 19.6mmol/L。\
        酸碱平衡失调的类型是（　　）。", \
            "options": ["代谢性碱中毒", "代谢性酸中毒", "呼吸性酸中毒合并代谢性酸中毒", "呼吸性酸中毒", "呼吸性酸中毒合并代谢性碱中毒"]

{"question": "患者男性，16岁。踢足球时致右大腿轻度碰伤，未在意。第2天出\
现局部明显肿胀，剧痛，活动明显受限，高热。最有诊断意义的检查\
是（　　）。", "options": ["拍X线片", "B型超声", "检查局部", "分层穿刺", "血尿常规"]\

 "question": "患者，男性，76岁，慢性肺源性心脏病10年，近日受凉后咳黏脓痰，查体：体温37.6℃，端坐位，口唇发绀，双下肢水肿，两肺散在干、湿啰音，叩诊心界不大，心率92次/分，律齐, 肝肋下2cm。下列措施中最关键的是",
            "A": "持续低流量吸氧",
            "B": "静脉点滴广谱抗生素",
            "C": "使用快速洋地黄制剂",
            "D": "使用利尿药控制心力衰竭",
            "E": "静脉补液以稀释痰液"
从文本中提取患者的信息作为条件，形如条件1,2,3,4，条件1是患者的主诉，剩下的为其他条件，并列出问题以\
及选项，不要给出正确答案\

第一步，你现在只有条件1，2,3，不允许考虑其他任何条件，给出一个0到0.5之间的数字，表示只在条件1的\
信息下选择每个选项的概率，对每个选项都解释给出该数字的理由，如果概率很小就给一个比较接近0的数，不要给0，如果概\
率比较大就给一个比较接近0.5的数。\

记住要把严重的疾病优先考虑\
第二步，结合你拥有的知识，以一个专业医生的视角，告诉我每一个条件可能的原因，不要漏掉任何一个条件以及数据。\
给出一个0到1之间数字，表示在患者的所有条件下选择每个选项的概率，对每个选项都解释给出该数\
字的理由，尽可能的详细分析每一个条件，如果概率很小就给一个比较接近0的数，不要给0，如果概\
    率很大就给一个比较接近1的数\

最后将每个选项得到的这两个概率相乘，并选出概率最大的选项。


'''


你作为一个prompt engineer，对我的prompt进行修改，使得输出效果更好，只进行语义上的修改不要修改其他内容，下面“”内的是我的prompt

"questions": "心慌，恶心，逆时针旋转", "answers": "你好，根据你说的情况，初步分析有可能是胃肠型感冒或者是休息不好，劳累，供血不足等因素引起的，要注意多休息，清淡饮食，保持充足睡眠。建议先吃点藿香正气胶囊治疗试试，如果病情严重，要及时就医检查治疗，祝早日恢复健康"}

Question = """\
{"question": "男，67岁。反复咳嗽、咳痰30年，加重1周。\
    查体：双肺可闻及干湿性啰音。动脉血气分析示：pH 7.21，PaCO2 75mmHg，PaO2 50mmHg，HCO3－ 19.6mmol/L。\
        酸碱平衡失调的类型是（　　）。", \
            "options": ["代谢性碱中毒", "代谢性酸中毒", "呼吸性酸中毒合并代谢性酸中毒", "呼吸性酸中毒", "呼吸性酸中毒合并代谢性碱中毒"]
"""

gradient_prompt_template="""Your task is to point out the problems with the\
current prompt based on the wrong examples.\
The current prompt is: {current} But this prompt gets the following exampleswrong.You should analyze the differences between wrong\
predictions and ground truth answers, and carefully\
consider why this prompt led to incorrect predictions.\
Below are the task examples with Queston,\
Wrong prediction, and Ground truth answer. {error_demonstrations}

{analyze}
"""


Your task is to point out the problems with the
current prompt based on the wrong examples.
The current prompt is:"从文本中提取患者的信息作为条件，并用数字依次顺序标出，形如条件1,2,3,4，条件1是患者的主诉，剩下的为其他条件，不要给出正确答案."But this prompt gets the following exampleswrong.You should analyze the differences between wrong\
predictions and ground truth answers, and carefully
consider why this prompt led to incorrect predictions.
Below are the task examples with Queston,
Wrong prediction, and Ground truth answer. 

错误输出：

条件1: 患者的主诉是反复咳嗽、咳痰30年，加重1周。

条件2: 患者的性别是男性，年龄为67岁。

条件3: 查体结果显示双肺可闻及干湿性啰音。

条件4: 动脉血气分析结果为pH 7.21，PaCO2 75mmHg，PaO2 50mmHg，HCO3－ 19.6mmol/L。
正确输出：
条件1: 患者是男性，67岁，主诉是反复咳嗽、咳痰30年，加重1周。

条件2: 查体结果显示双肺可闻及干湿性啰音。

条件3: 动脉血气分析结果为pH 7.21，PaCO2 75mmHg，PaO2 50mmHg，HCO3－ 19.6mmol/L。

Give a reason why the prompt could have
gotten these examples wrong.
Wrap the reason with <START> and <END>.