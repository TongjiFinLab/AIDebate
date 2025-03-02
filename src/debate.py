import os
from openai import OpenAI
import json
from datetime import datetime
import logging

API_SECRET_KEY = ""
BASE_URL = ""


class DebateCompetition:
    def __init__(self, topic, positive_model="o3-mini-2025-01-31", negative_model="deepseek-reasoner", logger=None):
        self.client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
        self.topic = topic
        self.debate_history = []
        self.positive_model = positive_model
        self.negative_model = negative_model
        self.logger = logger
        
    def get_completion(self, role_prompt, context="", side="正方"):
        
        messages = [
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": f"辩论主题：{self.topic}\n\n当前辩论历史：\n{context}\n\n你的责任：\n{role_prompt}"}
        ]

        # 根据正反方选择对应的模型
        model = self.positive_model if side == "正方" else self.negative_model

        self.logger.info(f"Model: {model}")
        self.logger.info(f"Messages: {messages}")
        
        if model == "deepseek-reasoner":
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000, #指的是模型生成的最大token数，2000表示2000个token，一个token大约4个字符
                temperature=0.7,#大小代表随机性，越大随机性越大，越小越确定
                presence_penalty=0.6  # 降低重复内容的可能性
            )
            self.logger.info(f"Response: {response}")
            reasoning_and_context = '> Reasoning '+response.choices[0].message.reasoning_content.replace('\n\n', ' ') +"\n\n" + response.choices[0].message.content
            return reasoning_and_context
        
        elif model == "o3-mini-2025-01-31":
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000, #指的是模型生成的最大token数，2000表示2000个token，一个token大约4个字符
                temperature=0.7,#大小代表随机性，越大随机性越大，越小越确定
            )
            self.logger.info(f"Response: {response}")
            return response.choices[0].message.content
        else: #deepseek-chat
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000, #指的是模型生成的最大token数，2000表示2000个token，一个token大约4个字符
                temperature=0.7,#大小代表随机性，越大随机性越大，越小越确定
            )
            self.logger.info(f"Response: {response}")
            return "> Reasoning " +"None \n\n" + response.choices[0].message.content
    
    def format_debate_history(self):
        return "\n\n".join([f"{entry['side']} {entry['speaker']}: {entry['content']}" 
                           for entry in self.debate_history]) #将辩论历史转换为字符串
    
    def add_to_history(self, side, speaker, stage, content):
        # 处理 o3-mini 模型的输出,为了统一，实现的时候将deepseek的输出格式也处理为了o3-mini
        try:
            # 找到第一个双换行符的位置
            split_index = content.index('\n\n', content.index('> Reasoning'))
            reasoning = content[:split_index].strip()  # 推理部分
            content = content[split_index:].strip()    # 实际内容
        except ValueError:
            # 如果找不到双换行符，使用默认的分割方式
            reasoning = content
            content = content
        
        # 添加分隔符
        print("\n" + "=" * 50)
        print(f"{side} {speaker} ({stage}):")
        print(content)
        print("=" * 50, flush=True)
        
        # 添加到历史记录
        self.debate_history.append({
            "side": side,
            "speaker": speaker,
            "stage": stage,
            "content": content,
            "reasoning": reasoning
        })

    @property
    def prompts(self):
        return {
            'first_speaker': """
            你是一位标准辩论赛的一号辩手。作为{side}方一辩，你代表{stance}的立场。你的任务是：
            1. 清晰定义辩题中的关键概念
            2. 阐明{side}方立场
            3. 建立论述框架，提出2-3个核心论点
            4. 详细展开论点
            请用专业、严谨的语言完成立论陈词。
            """,
            
            'questioning': """
            你是{side}方辩手，你代表{stance}的立场。现在是质询环节：
            1. 请针对对方最近的发言提出3-4个尖锐的问题
            2. 质询要简短有力，直指对方论证的关键漏洞
            3. 注意问题的连贯性和逻辑性
            """,
            
            'rebuttal': """
            你是{side}方二辩，代表{stance}的立场。你的任务是：
            1. 针对对方论点进行有力驳斥
            2. 强化{side}方论证
            3. 提出新的论据支持己方观点
            请保持逻辑性和攻击性。
            """,
            
            'summary': """
            你是{side}方三辩，代表{stance}的立场。请完成质询小结：
            1. 总结之前的质询环节要点
            2. 强化{side}方优势论点
            3. 指出对方论证中的关键漏洞
            4. 为后续辩论奠定基础
            """,
            
            'free_debate': """
            这是自由辩论环节。作为{side}方辩手，你坚定代表{stance}的立场。：
            1. 抓住对方论证漏洞进行反击
            2. 深化{side}方论点
            3. 回应对方质疑
            4. 提出新的论据或视角
            请保持言简意赅，突出重点。
            """,
            
            'final_speaker': """
            你是{side}方四辩，代表{stance}的立场。请完成总结陈词：
            1. 梳理整场辩论的关键分歧点
            2. 总结{side}方优势论点
            3. 指出对方论证中的致命缺陷
            4. 有力地重申{side}方立场
            请全面而有力地总结，为己方赢得辩论。
            """
        }

    def run_debate(self):
        # 第一阶段：开篇陈词和质询
        print("\n=== 第一阶段：开篇陈词和质询 ===\n")
        support_stance = f"支持「{self.topic}」"
        oppose_stance = f"反对「{self.topic}」"
        
        # 正方一辩立论
        print("【正方一辩立论】")
        content = self.get_completion(self.prompts['first_speaker'].format(side="正",stance=support_stance), side="正方")
        self.add_to_history("正方", "一辩", "立论", content)
        
        # 反方四辩质询正方一辩
        print("\n【反方四辩质询】")
        questioning = self.get_completion(
            self.prompts['questioning'].format(side="反",stance=oppose_stance)
            ,context=self.format_debate_history()
            ,side="反方"
        )
        self.add_to_history("反方", "四辩", "质询", questioning)
        
        # 反方一辩立论
        print("\n【反方一辩立论】")
        content = self.get_completion(self.prompts['first_speaker'].format(side="反",stance=oppose_stance),context=self.format_debate_history(), side="反方")
        self.add_to_history("反方", "一辩", "立论", content)
        
        # 正方四辩质询反方一辩
        print("\n【正方四辩质询】")
        questioning = self.get_completion(
            self.prompts['questioning'].format(
                side="正"
                ,stance=support_stance
            ),
            context=self.format_debate_history(),
            side="正方"
        )
        self.add_to_history("正方", "四辩", "质询", questioning)
        
        # 第二阶段：驳论和质询
        print("\n=== 第二阶段：驳论和质询 ===\n")
        
        # 正方二辩驳论
        print("【正方二辩驳论】")
        content = self.get_completion(self.prompts['rebuttal'].format(side="正",stance=support_stance),context=self.format_debate_history(), side="正方")
        self.add_to_history("正方", "二辩", "驳论", content)
        
        # 反方三辩质询
        print("\n【反方三辩质询】")
        questioning = self.get_completion(
            self.prompts['questioning'].format(
                side="反",
                stance=oppose_stance
            ),
            context=self.format_debate_history(),
            side="反方"
        )
        self.add_to_history("反方", "三辩", "质询", questioning)
        
        # 反方二辩驳论
        print("\n【反方二辩驳论】")
        content = self.get_completion(self.prompts['rebuttal'].format(side="反",stance=oppose_stance),context=self.format_debate_history() ,side="反方")
        self.add_to_history("反方", "二辩", "驳论", content)
        
        # 正方三辩质询
        print("\n【正方三辩质询】")
        questioning = self.get_completion(
            self.prompts['questioning'].format(
                side="正",
                stance=support_stance
            ),
            context=self.format_debate_history(),
            side="正方"
        )
        self.add_to_history("正方", "三辩", "质询", questioning)
        
        # 第三阶段：质询小结
        print("\n=== 第三阶段：质询小结 ===\n")
        
        # 反方三辩小结
        print("【反方三辩小结】")
        content = self.get_completion(self.prompts['summary'].format(side="反",stance=oppose_stance),context=self.format_debate_history(), side="反方")
        self.add_to_history("反方", "三辩", "小结", content)
        
        # 正方三辩小结
        print("\n【正方三辩小结】")
        content = self.get_completion(self.prompts['summary'].format(side="正",stance =support_stance), context=self.format_debate_history(), side="正方")
        self.add_to_history("正方", "三辩", "小结", content)
        
        # 第四阶段：自由辩论
        print("\n=== 第四阶段：自由辩论 ===\n")
        
        # 模拟4轮自由辩论
        for i in range(3):
            print(f"\n【第{i+1}轮自由辩论】")
            # 正方发言
            content = self.get_completion(self.prompts['free_debate'].format(side="正",stance=support_stance)
                                          ,context=self.format_debate_history()
                                          ,side="正方")
            self.add_to_history("正方", f"自由辩论{i+1}", "自由辩论", content)
            
            # 反方发言
            content = self.get_completion(self.prompts['free_debate'].format(side="反",stance=oppose_stance)
                                          ,context=self.format_debate_history()
                                          ,side="反方")
            self.add_to_history("反方", f"自由辩论{i+1}", "自由辩论", content)
        
        # 第五阶段：总结陈词
        print("\n=== 第五阶段：总结陈词 ===\n")
        
        # 反方四辩总结
        print("【反方四辩总结】")
        content = self.get_completion(self.prompts['final_speaker'].format(side="反",stance=oppose_stance)
                                          ,context=self.format_debate_history()
                                          ,side="反方")
        self.add_to_history("反方", "四辩", "总结", content)
        
        # 正方四辩总结
        print("\n【正方四辩总结】")
        content = self.get_completion(self.prompts['final_speaker'].format(side="正",stance=support_stance)
                                          ,context=self.format_debate_history()
                                          ,side="正方")
        self.add_to_history("正方", "四辩", "总结", content)
        
        return self.debate_history
    
def get_logger(filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(filename.replace('.json', '.log'))
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def run_debate_competition(
    topic, 
    positive_model="o3-mini-2025-01-31",
    negative_model="deepseek-reasoner"
):
    current_time = datetime.now().strftime("%m%d_%H%M")
    safe_topic = "".join(char for char in topic if char.isalnum() or char in (' ', '_'))
    filename = f'debate_{current_time}_{safe_topic}_pos_{positive_model}_neg_{negative_model}.json'
    
    logger = get_logger(filename)

    debate = DebateCompetition(
        topic=topic,
        positive_model=positive_model,
        negative_model=negative_model,
        logger = logger
    )
    results = debate.run_debate()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n辩论结果已保存至: {filename}")

if __name__ == '__main__':
    topic = "人工智能是否能够取代人类理财顾问？"
    run_debate_competition(
        topic=topic,
        positive_model="o3-mini-2025-01-31-high",  # deepseek-reasoner o3-mini-2025-01-31
        negative_model="deepseek-reasoner"     # deepseek-reasoner o3-mini-2025-01-31
    )