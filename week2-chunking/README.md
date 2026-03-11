# Week 2：文本分块（Chunking）+ 模型选型

## 目标
理解"怎么切文本"对检索质量的影响——同一篇文档，不同切法，检索结果完全不同。

## 实验列表

### 实验 1：`02_chunking_and_models.py`（必做）
- 实现 3 种分块策略：固定长度、按段落、滑动窗口
- 对同一篇文档分块，观察每种策略的切分结果
- 用 W1 写好的 Embedding + 余弦相似度做检索，对比三种策略的检索效果
- 回答思考题

### 实验 2（选做扩展）：
- 拉 `bge-m3` 模型：`ollama pull bge-m3`
- 用 W1 的 10 段文本，分别用 `nomic-embed-text` 和 `bge-m3` 计算相似度矩阵
- 对比：`bge-m3` 是否解决了 W1 发现的"结构相似但语义不同"的问题？

## 运行方式

```bash
# 建议先在项目根目录准备依赖和环境变量
pip install -e .[dev]
python scripts/dev.py init-env

# 运行实验
python week2-chunking/02_chunking_and_models.py
```

如果你已经在 `week2-chunking/` 目录里，也可以直接执行：

```bash
python 02_chunking_and_models.py
```

## 需要实现的函数

| 函数 | 难度 | 说明 |
|------|------|------|
| `chunk_by_fixed_length()` | ⭐ | 最简单，一个循环搞定 |
| `chunk_by_paragraph()` | ⭐ | split + 过滤，两行代码 |
| `chunk_by_sliding_window()` | ⭐⭐ | 需要想清楚步长和终止条件 |
| `get_embeddings()` | — | 复制 W1 的实现 |
| `cosine_similarity()` | — | 复制 W1 的实现 |
| `search_chunks()` | ⭐⭐ | 核心函数，串联 embedding + 相似度 + 排序 |

## ⛔ 规则
- 三种分块函数必须自己写
- `search_chunks()` 必须自己写
- W1 的函数可以直接复制过来
- 写完后回答文件底部的思考题

## 本周总结（完成后填写）
- 学到了什么：
- 踩了什么坑：
- 下周关注什么：
