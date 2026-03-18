# Week 4：Prompt 基础 + RAG 管道

> **目标**：理解 Prompt 工程基础，然后串联 W1-W3 组装完整的端到端 RAG 问答系统
> **交付物**：`04_basic_rag.py`

---

## 本周地图

| 阶段 | 内容 | 关键概念 |
|------|------|----------|
| 上半段 | Prompt 工程基础 | System Prompt、Few-shot、Context Window |
| 下半段 | 串联 RAG 管道 | 文档→分块→向量化→检索→Prompt→LLM→回答 |

---

## 前置准备

确保 Ollama 已安装并拉取模型：

```bash
# 确认 Ollama 服务在运行
curl http://localhost:11434/v1/models

# 拉取 LLM 模型（如果还没有）
ollama pull qwen3:8b

# 确认 Embedding 模型也在（W1-W3 用过）
ollama pull bge-m3
```

---

## 实验步骤

### Part 1：Prompt 工程基础

**第一步：调用 LLM API**
- Ollama 兼容 OpenAI 的 `/v1/chat/completions` 接口
- 理解 messages 结构：`role`（system/user/assistant）和 `content`
- 实现一个最基本的 LLM 调用函数

**第二步：System Prompt 的作用**
- 对同一个问题，用不同的 System Prompt 观察回答风格变化
- 理解 System Prompt 如何"设定角色"和"约束行为"

**第三步：Few-shot Prompting**
- 在 prompt 中给出几个示例，引导 LLM 按特定格式回答
- 对比 zero-shot vs few-shot 的回答质量

**第四步：Context Window 限制**
- 了解模型的上下文窗口大小（qwen3:8b 约 32K tokens）
- 理解为什么 RAG 需要"检索再送入"而不是"把所有文档塞进去"

### Part 2：组装 RAG 管道

**第五步：构建 RAG Prompt**
- 将检索到的文档块组装成 context
- 设计 RAG 专用的 System Prompt（要求基于上下文回答，不知道就说不知道）

**第六步：端到端 RAG 管道**
- 串联完整流程：分块 → 向量化 → Chroma 存储 → 语义检索 → 构造 Prompt → LLM 生成
- 复用 W2 的分块、W3 的 Chroma 存储

**第七步：对比实验**
- 同一个问题，对比"直接问 LLM"vs"RAG 增强后问 LLM"的回答
- 观察 RAG 如何减少幻觉、提高准确性

---

## 思考题（完成实验后回答）

1. System Prompt 和 User Prompt 的区别是什么？如果冲突了，LLM 会听谁的？
2. 为什么 RAG 的 System Prompt 要强调"如果上下文中没有相关信息，请说不知道"？
3. Context Window 有限，但检索回来的文档块可能很多。你会怎么决定送入多少块？
4. Few-shot 示例放在 System Prompt 里好，还是放在 User Prompt 里好？为什么？
5. 如果 RAG 检索到了错误的文档块，LLM 会怎么表现？这说明了什么？

---

## 第一阶段里程碑检查

完成 W4 后，你应该能：
- [ ] 对一份中文文档进行问答（端到端 RAG）
- [ ] 解释 RAG 管道中每个组件的作用
- [ ] 说出 Prompt 工程的三个基本技巧
- [ ] 对比有无 RAG 的回答质量差异
