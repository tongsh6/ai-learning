# 第一阶段里程碑验证：PDF 端到端 RAG 问答

## 验证目标

用中文友好模型 + 自己写的代码，对一份真实 PDF 文档进行端到端问答。
串联 W1-W4 所有能力：PDF 读取 → 分块 → Embedding → Chroma 存储 → 检索 → Prompt → LLM。

## 使用的 PDF 文档

- 文档名称：`rag_intro_zh.pdf`
- 来源：基于 `milestone-1/data/rag_intro_zh.txt` 生成的中文 RAG 综述资料
- 页数：4 页
- 简介：围绕 RAG 的定义、技术演进、Indexing、Retrieval、Generation、评估体系和前沿方向展开，适合作为第一阶段 PDF 问答验证材料

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


### 检索质量判断
- 事实型问题整体表现较稳定，能够从 `Prompt Engineering`、`Reranking`、`RAGas` 等章节中召回相关块
- 与 W4 的硬编码短文本相比，真实 PDF 材料噪声更多，检索结果更依赖分块质量和问题措辞
- 对需要跨段整合的信息，当前 `top_k=3` 的纯向量检索能提供部分支撑，但稳定性仍有限

### 生成质量判断
- 当检索块与问题强相关时，回答基本能够忠实于资料内容，幻觉明显少于“直接问 LLM”
- 对综合型问题，回答可以覆盖主要结论，但组织性和归纳深度仍有提升空间
- 对文档中未出现的问题，系统能够明确拒答，说明 RAG Prompt 的约束是有效的

### 发现的问题和改进方向
1. **真实文档噪声处理**：PDF 提取后的文本仍存在一定格式噪声，真实文档场景比 W4 的演示文本更考验预处理质量。
2. **分块策略优化**：当前仍以段落/滑窗为主，后续可尝试标题感知分块或更细粒度的结构化清洗。
3. **检索策略升级**：纯向量检索对精确关键词、术语匹配不够稳，这正是 W5 引入 BM25 + 向量混合检索的动机。
4. **回答质量提升**：后续可尝试 reranking、上下文压缩或更严格的引用约束，提高综合题表现。
