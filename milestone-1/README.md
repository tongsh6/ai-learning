# 第一阶段里程碑验证：PDF 端到端 RAG 问答

## 验证目标

用中文友好模型 + 自己写的代码，对一份真实 PDF 文档进行端到端问答。
串联 W1-W4 所有能力：PDF 读取 → 分块 → Embedding → Chroma 存储 → 检索 → Prompt → LLM。

## 使用的 PDF 文档

<!-- 替换为你选的 PDF 信息 -->
- 文档名称：
- 来源：
- 页数：
- 简介：

## 运行方式

1. 将 PDF 文件放入 `data/` 目录
2. 修改 `milestone_rag_pdf.py` 中的 `PDF_PATH` 文件名
3. 先实现 `common/pdf_reader.py` 中的两个 TODO 函数
4. 再实现 `milestone_rag_pdf.py` 中的 TODO 函数
5. 运行验证：

```bash
# 从项目根目录运行
python milestone-1/milestone_rag_pdf.py
```

## 实现顺序

1. `common/pdf_reader.py` — `read_pdf()` 和 `read_pdf_pages()`
2. 运行测试验证：`pytest tests/test_pdf_reader.py -v`
3. `milestone_rag_pdf.py` — `load_and_chunk()`
4. `milestone_rag_pdf.py` — `build_knowledge_base()`
5. `milestone_rag_pdf.py` — `rag_retrieve()` + `build_rag_prompt()` + `rag_query()`
6. 填写 `EVAL_QUESTIONS` 中的预设问题和参考答案
7. 运行完整验证，填写下方评估结论

## 评估结论

<!-- 跑完后手动填写 -->

### 检索质量判断

### 生成质量判断

### 发现的问题和改进方向
