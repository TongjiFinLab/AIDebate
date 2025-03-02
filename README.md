# AIDebate

本项目旨在深入探索人工智能大语言模型在辩论场景中的表现。我们期望通过展示这些模型在辩论中的能力，为研究大语言模型的推理能力、论证方式以及建模方式提供素材和借鉴。

本项目后续将持续更新，纳入更多不同模型在多个领域和多样辩题上的辩论过程，全面呈现各个模型在辩论赛中的能力与表现，为广大研究者和从业者提供的参考。欢迎开发者参与贡献本项目。

## 项目结构

    ├── videos/ # 大模型辩论赛的视频展示
    ├── src/ # 大模型辩论赛的组织代码
    ├── log/ # 大模型辩论赛的完整日志记录
    ├── results/ # 大模型辩论赛的结果展示
    ├── README.md
    └── LICENSE

## 辩论规则设置

### 第一阶段：开篇陈词和质询（共10分钟）
- 由正方一辩进行立论，时间为3分钟；由反方四辩对正方一辩进行质询，时间为2分钟。
- 由反方一辩进行立论，时间为3分钟；由正方四辩对反方一辩进行质询，时间为2分钟。

### 第二阶段：驳论和质询（共8分钟）
- 由正方二辩进行驳论，时间为2分钟；由反方三辩对正方二辩进行质询，时间为2分钟。
- 由反方二辩进行驳论，时间为2分钟；由正方三辩对反方二辩进行质询，时间为2分钟。

### 第三阶段：质询小结（共4分钟）
- 由反方三辩对刚刚的两场质询进行小结，时间为2分钟。
- 由正方三辩对刚刚的两场质询进行小结，时间为2分钟。

### 第四阶段：自由辩论（共8分钟）
- 本阶段双方各计时4分钟，由正反方交替发言，正方先发言。
为辩论过程的流畅性考虑，此阶段双方均可发言三轮。

### 第五阶段：总结陈词（共8分钟）
- 由反方四辩对整场辩论进行总结陈词，时间为4分钟。
- 由正方四辩对整场辩论进行总结陈词，时间为4分钟。

## 辩论赛示例

以金融决策场景为例，我们围绕 “智能投顾是否会取代人类理财顾问？” 这一核心议题，呈现了 Deepseek-R1 和 OpenAI o3-mini-high 两个典型大模型的辩论结果。
### 辩论赛题
#### 智能投顾是否会取代人类理财顾问？
- 正方（Deepseek-R1） VS  反方 OpenAI o3-mini-high  [[阅读文字版](results/智能投顾是否会取代人类理财顾问(正方-deepseek-r1-反方-o3-mini-high).md )][[观看视频]()]

### 视频展示

<div align="center">
  <video src="videos/example.mp4" controls="controls" width="500" height="300"></video> 
  <br />
  <br />
</div>

### 辩手介绍

|                | Deepseek-R1 | OpenAI o3-mini-high | 
| ---------------| ----        | -------             |
| 发布时间        | 2025年1月20日| 2025年1月29日| 
| 开源状况        | 开源| 闭源| 
| 模型类型        | 带有Chain-of-Thought的推理模型| 带有Chain-of-Thought的推理模型| 
| 推理模式        | 一档| 低/中/高三档| 
| API价格（输入） | 1¥/million tokens| 1.1\$/million tokens| 
| API价格（输出） | 16¥/million tokens| 4.4\$/million tokens| 
| 支持长度        | 128K tokens（约213K汉字）| 200K tokens（约100K汉字）| 
| 模型参数        | 671B 激活 37B（671A37）| 未知| 

### 表现对比
|            | Deepseek-R1 | OpenAI o3-mini-high | 
| -----------| ----        | -------             |
| AIME 2024  | 79.8        | **87.3**            | 
| MATH-500   | 97.3        | **97.9**            | 
| Codeforces | 2029        | **2130**            | 
| SWE-Bench  | 49.2        | **49.3**            | 
| MMLU       | **90.8**    | 86.9                | 
| SimpleQA   | **30.1**    | 13.8                | 


## 更多辩论赛内容
#### 1. 智能投顾是否会取代人类理财顾问？
- 正方（Deepseek-R1） VS 反方 （OpenAI o3-mini-high） [[文字版阅读](results/智能投顾是否会取代人类理财顾问(正方-deepseek-r1-反方-o3-mini-high).md)]
- 正方（OpenAI o3-mini-high） VS 反方 （Deepseek-R1） [[文字版阅读](results/智能投顾是否会取代人类理财顾问(正方-o3-mini-high-反方-deepseek-r1).md)]
- 正方（Deepseek-R1） VS 反方 （Deepseek-R1） [[文字版阅读](results/tba.md)]
- 正方（OpenAI o3-mini-high） VS 反方 （OpenAI o3-mini-high） [[文字版阅读](results/tba.md)]

#### 2. 人工智能能否取代人类投资经理？
- 正方（Deepseek-R1） VS 反方 （OpenAI o3-mini-high） [[文字版阅读](results/tba.md)]
- 正方（OpenAI o3-mini-high） VS 反方 （Deepseek-R1） [[文字版阅读](results/tba.md)]
- 正方（Deepseek-R1） VS 反方 （Deepseek-R1） [[文字版阅读](results/tba.md)]
- 正方（OpenAI o3-mini-high） VS 反方 （OpenAI o3-mini-high） [[文字版阅读](results/tba.md)]


## 许可证
AIDebate是一项仅用于非商业使用的研究预览，受OpenAI和DeepSeek生成数据的使用条款约束。如果您发现任何潜在的风险行为，请与我们联系。该代码发布在Apache License 2.0下。

## 感谢我们的贡献者 ：
<a href="https://github.com/TongjiFinLab/AIDebate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TongjiFinLab/AIDebate" />
</a>
