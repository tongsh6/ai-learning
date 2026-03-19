# Milestone 1: PDF 端到端 RAG 问答验证

## 概述

第一阶段（W1-W4）里程碑验证：用中文友好模型 + 自己写的代码，对一份公开中文技术 PDF 文档进行端到端问答，并通过预设问题评估回答质量。

## 目标

1. 验证 W1-W4 所学能力可以串联成完整的 RAG 管道
2. 新增 PDF 读取能力，从硬编码文本升级到真实文档
3. 通过交互式问答和预设评估，建立对 RAG 质量的直觉基线

## 项目结构

```
ai-learning/
├── common/
│   ├── pdf_reader.py          # 新增：PDF 文本提取
│   └── ...（现有模块不变）
├── milestone-1/
│   ├── milestone_rag_pdf.py   # 里程碑验证主脚本
│   ├── data/                  # 存放测试 PDF
│   │   └── (用户自选的公开中文技术文档.pdf)
│   └── README.md              # 验证结论记录
├── requirements.txt           # 新增 PyMuPDF 依赖
└── pyproject.toml             # 同步更新依赖
```

**关键决策**：
- `milestone-1/` 独立于 `weekN-xxx/` 目录，体现阶段性验证的定位
- PDF 文件放 `milestone-1/data/`，不污染其他目录
- `common/pdf_reader.py` 是唯一新增的公共模块
- `.gitignore` 需添加 `milestone-1/data/*.pdf`，避免将 PDF 文件提交到 git

## 模块设计

### `common/pdf_reader.py`

依赖：`PyMuPDF`（import 名为 `fitz`）

```python
def read_pdf(file_path: str) -> str:
    """
    读取 PDF 文件，返回全文纯文本。

    - 逐页提取文本，页间用双换行分隔
    - 清理多余空行（连续 3+ 空行合并为 2 个）
    - 不做分块（分块交给 text_splitters）
    """

def read_pdf_pages(file_path: str) -> list[dict]:
    """
    逐页读取 PDF，返回 [{"page": 1, "text": "..."}, ...]

    - 保留页码信息，后续可用于 metadata 过滤
    - 每页文本独立清理
    """
```

**TODO 模式**：两个函数都是 TODO stub——给出 docstring + 实现提示，学习者自己填写实现。

设计原则：
- 职责单一：只负责 "PDF -> 纯文本"，不涉及分块和 Embedding
- `read_pdf` 用于简单场景（里程碑验证直接用）
- `read_pdf_pages` 保留页码元数据，后续 Chroma metadata 过滤时可用
- 清理逻辑最小化：只合并多余空行，不做激进的格式处理
- 无需环境变量配置，只依赖 PyMuPDF 库

**已知风险：PDF 文本的分块兼容性**

PyMuPDF 提取的文本不一定以双换行分隔段落（可能是单换行或无换行拼接），导致 `chunk_by_paragraph()` 可能失效（整页变成一个巨大的 chunk）。应对策略：
- `read_pdf` 在提取时需对页内文本做段落检测：利用 PyMuPDF 的 `page.get_text("blocks")` 按文本块提取，块间用双换行分隔，确保输出文本与 `chunk_by_paragraph` 兼容
- Part 1 打印分块预览时，学习者应检查分块数量和大小是否合理。如果分块过少/过大，可切换到 `chunk_by_sliding_window` 作为 fallback

### `milestone-1/milestone_rag_pdf.py`

脚本分 4 个 Part：

#### Part 1: PDF 读取 + 分块

```python
# 使用 Path(__file__).parent 构造绝对路径，避免运行目录依赖
PDF_PATH = Path(__file__).parent / "data" / "xxx.pdf"

# read_pdf() -> 全文文本
# chunk_by_paragraph() 分块
# 打印：文档总字数、分块数量、每块前50字预览
# 检查：如果分块过少或单块过大（>1000字），提示切换到 chunk_by_sliding_window
```

#### Part 2: 构建向量知识库

```python
# get_embeddings() 向量化
# Chroma 内存客户端，存入 chunks + embeddings
# metadata 包含 chunk_index 和 char_count
# 打印：collection 中文档数量确认
```

#### Part 3: 交互式问答

```python
# while True 循环，用户输入问题
# 输入 "quit" 退出
# 每次：检索 Top-3 -> 构造 RAG Prompt -> LLM 生成 -> 打印回答
# 同时打印检索到的文档块（方便判断检索质量）
```

#### Part 4: 预设问题评估

```python
# 5-6 组 {"question": "...", "reference": "...", "aspect": "..."}
# aspect 标注考察维度：事实准确性 / 综合性 / 忠实度
# 对每个问题：
#   1. RAG 回答
#   2. 无 RAG 直接问 LLM 的回答
#   3. 参考答案
# 逐列输出（先 RAG 回答，再无 RAG 回答，最后参考答案），用分隔线区分，人工判断
```

脚本执行流程：先跑 Part 1-2 构建知识库，然后用户选择进入 Part 3（交互式）或 Part 4（预设评估），或两者都跑。

TODO 模式：核心函数给 TODO + 提示，由学习者自己填实现。脚手架和打印格式由课件提供。

## PDF 选择

要求：
- 公开的中文技术文档
- 中文为主，内容有一定信息密度
- 5-15 页为宜
- 学习者有一定了解（方便判断回答质量）

由学习者自行选取，放入 `milestone-1/data/`。

## 评估问题设计原则

等 PDF 选定后，根据文档内容设计 5-6 个问题，覆盖 3 个考察维度：

| 维度 | 说明 | 问题数 |
|------|------|--------|
| 事实准确性 | 答案在文档中有明确出处 | 2-3 个 |
| 综合性 | 需要跨多个段落/页面整合信息 | 1-2 个 |
| 忠实度 | 文档中没有的信息，LLM 应拒绝回答 | 1 个 |

每个问题附参考答案（从文档中摘出关键句）。

## `milestone-1/README.md` 结构

```markdown
# 第一阶段里程碑验证

## 验证目标
## 使用的 PDF 文档
## 运行方式
## 评估结论（跑完后手动填写）
- 检索质量判断
- 生成质量判断
- 发现的问题和改进方向
```

## 依赖变更

- 新增 `PyMuPDF` 到 `requirements.txt` 和 `pyproject.toml`
- 补充 `chromadb` 到 `requirements.txt` 和 `pyproject.toml`（W3 起已在使用但未声明）

## 复用的现有模块

| 模块 | 用途 |
|------|------|
| `common/text_splitters.py` | `chunk_by_paragraph()` 分块 |
| `common/embedding.py` | `get_embeddings()` 向量化 |
| `common/llm.py` | `chat()` LLM 调用 |

不新增 Chroma 封装，直接在脚本中使用 `chromadb` API（与 W3/W4 保持一致）。

## 不在范围内

- 命令行参数（方案 B 的 argparse）
- Ingest/Query 分离（方案 C 的架构拆分）
- 量化评估指标（W8-W9 的内容）
- PDF 表格/图片提取（只处理文本）
