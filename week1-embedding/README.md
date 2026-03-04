# Week 1：Embedding 基础

## 目标
理解 Embedding 的本质——文本如何变成向量，向量如何衡量语义相似性。

## 实验列表

### 实验 1：`01_embedding_basics.py`
- 把 10 段中文文本转成 Embedding
- 手动实现余弦相似度计算（不用 sklearn）
- 分析相似度矩阵，回答思考题

### 实验 2（自己扩展）：
- 换一个 Embedding 模型（如 OpenAI text-embedding-3-small），对比结果
- 同一段话翻译成英文后，Embedding 相似度是多少？

## 运行方式

```bash
# 先安装依赖
pip install numpy requests

# 运行实验
python 01_embedding_basics.py
```

## ⛔ 规则
- `get_embeddings()` 和 `cosine_similarity()` 必须自己写
- 可以查 API 文档，但不要让 AI 生成完整实现
- 写完后回答文件底部的思考题

## 学习资源
- [OpenAI Embedding 文档](https://platform.openai.com/docs/guides/embeddings)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [余弦相似度 - Wikipedia](https://zh.wikipedia.org/wiki/余弦相似性)
