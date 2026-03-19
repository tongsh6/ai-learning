# Milestone 1: PDF 端到端 RAG 问答验证 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建里程碑验证课件——PDF 读取模块 + 端到端 RAG 问答脚本（TODO 脚手架），供学习者自己填写核心实现。

**Architecture:** 新增 `common/pdf_reader.py` 公共模块（TODO stub），创建 `milestone-1/milestone_rag_pdf.py` 主脚本（TODO 脚手架 + 打印格式），配套测试和 README。学习者负责填写所有 TODO 函数体。

**Tech Stack:** Python 3.11+, PyMuPDF (fitz), chromadb, 现有 common/ 模块

**Spec:** `docs/superpowers/specs/2026-03-19-milestone-1-rag-pdf-design.md`

---

## 文件清单

| 操作 | 文件 | 职责 |
|------|------|------|
| Modify | `requirements.txt` | 添加 PyMuPDF + chromadb |
| Modify | `pyproject.toml` | 同步添加依赖 |
| Modify | `.gitignore` | 添加 PDF 排除规则 |
| Create | `common/pdf_reader.py` | PDF 文本提取（TODO stub） |
| Create | `tests/test_pdf_reader.py` | pdf_reader 单元测试 |
| Create | `milestone-1/data/.gitkeep` | 保留空目录 |
| Create | `milestone-1/milestone_rag_pdf.py` | 里程碑验证主脚本（TODO 脚手架） |
| Create | `milestone-1/README.md` | 验证说明和结论记录模板 |

---

### Task 1: 依赖和基础设施

**Files:**
- Modify: `requirements.txt`
- Modify: `pyproject.toml`
- Modify: `.gitignore`
- Create: `milestone-1/data/.gitkeep`

- [ ] **Step 1: 替换 requirements.txt 为以下完整内容**

```
numpy
requests
pytest
ruff
PyMuPDF
chromadb
```

- [ ] **Step 2: 更新 pyproject.toml**

更新 `[project] dependencies`：

```toml
dependencies = [
    "numpy",
    "requests",
    "PyMuPDF",
    "chromadb",
]
```

同时移除 `[tool.pytest.ini_options] addopts` 中的 `"-p", "no:tmpdir"`（新增测试需要 `tmp_path` fixture）：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-p",
    "no:cacheprovider",
]
```

- [ ] **Step 3: 在 .gitignore 末尾添加 PDF 排除规则**

```gitignore
# PDF data files
milestone-1/data/*.pdf
```

- [ ] **Step 4: 创建 milestone-1/data/ 目录**

```bash
mkdir -p milestone-1/data
touch milestone-1/data/.gitkeep
```

- [ ] **Step 5: 安装新依赖**

Run: `pip install -e .[dev]`
Expected: PyMuPDF 和 chromadb 安装成功

- [ ] **Step 6: 验证安装**

Run: `python -c "import fitz; import chromadb; print('OK')"`
Expected: 输出 `OK`

- [ ] **Step 7: Commit**

```bash
git add requirements.txt pyproject.toml .gitignore milestone-1/data/.gitkeep
git commit -m "chore: add PyMuPDF and chromadb dependencies, gitignore PDF files"
```

---

### Task 2: common/pdf_reader.py（TODO stub + 测试）

**Files:**
- Create: `common/pdf_reader.py`
- Create: `tests/test_pdf_reader.py`

- [ ] **Step 1: 创建 tests/test_pdf_reader.py**

```python
"""common/pdf_reader.py 单元测试。"""

from __future__ import annotations

import fitz

from common.pdf_reader import read_pdf, read_pdf_pages


def _create_test_pdf(tmp_path, pages: list[str]) -> str:
    """辅助函数：创建包含指定页面文本的测试 PDF。"""
    pdf_path = str(tmp_path / "test.pdf")
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text, fontsize=12)
    doc.save(pdf_path)
    doc.close()
    return pdf_path


class TestReadPdf:
    """read_pdf() 测试。"""

    def test_single_page(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Hello World"])
        result = read_pdf(pdf_path)
        assert "Hello World" in result

    def test_multi_page_separated_by_double_newline(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Page one", "Page two"])
        result = read_pdf(pdf_path)
        assert "Page one" in result
        assert "Page two" in result
        # 页间应有双换行分隔
        assert "\n\n" in result

    def test_excessive_blank_lines_collapsed(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Line A\n\n\n\n\nLine B"])
        result = read_pdf(pdf_path)
        # 连续 3+ 空行应合并为 2 个换行
        assert "\n\n\n" not in result

    def test_file_not_found_raises(self):
        import pytest
        with pytest.raises(FileNotFoundError):
            read_pdf("/nonexistent/path.pdf")

    def test_returns_string(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Test"])
        result = read_pdf(pdf_path)
        assert isinstance(result, str)


class TestReadPdfPages:
    """read_pdf_pages() 测试。"""

    def test_returns_list_of_dicts(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Page 1", "Page 2"])
        result = read_pdf_pages(pdf_path)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_dict_has_page_and_text(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Content"])
        result = read_pdf_pages(pdf_path)
        assert result[0]["page"] == 1
        assert "Content" in result[0]["text"]

    def test_page_numbers_are_sequential(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["A", "B", "C"])
        result = read_pdf_pages(pdf_path)
        pages = [r["page"] for r in result]
        assert pages == [1, 2, 3]
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_pdf_reader.py -v`
Expected: FAIL（`common.pdf_reader` 不存在）

- [ ] **Step 3: 创建 common/pdf_reader.py（TODO stub）**

```python
"""PDF 文本提取公共模块。"""

from __future__ import annotations

import re
from pathlib import Path

import fitz


def read_pdf(file_path: str) -> str:
    """读取 PDF 文件，返回全文纯文本。

    - 逐页提取文本（使用 page.get_text("blocks") 按文本块提取）
    - 同一页内的文本块之间用双换行分隔
    - 不同页之间用双换行分隔
    - 清理多余空行（连续 3+ 空行合并为 2 个换行）
    - 不做分块（分块交给 text_splitters）

    Parameters
    ----------
    file_path : str
        PDF 文件路径

    Returns
    -------
    str
        提取的全文纯文本

    Raises
    ------
    FileNotFoundError
        文件不存在时抛出
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {file_path}")

    # TODO：自己实现
    # 提示：
    # 1. 用 fitz.open(file_path) 打开 PDF
    # 2. 遍历每一页，用 page.get_text("blocks") 获取文本块列表
    #    - 每个 block 是一个元组，block[4] 是文本内容，block[6] 是类型（0=文本）
    #    - 只取 block[6] == 0 的文本块
    # 3. 同一页内的文本块用双换行 "\n\n" 连接
    # 4. 不同页的文本用双换行 "\n\n" 连接
    # 5. 用 _clean_text() 清理多余空行
    # 6. 返回清理后的文本
    raise NotImplementedError("请在这里实现 read_pdf")


def read_pdf_pages(file_path: str) -> list[dict]:
    """逐页读取 PDF，返回带页码的文本列表。

    Parameters
    ----------
    file_path : str
        PDF 文件路径

    Returns
    -------
    list[dict]
        [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}, ...]

    Raises
    ------
    FileNotFoundError
        文件不存在时抛出
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {file_path}")

    # TODO：自己实现
    # 提示：
    # 1. 用 fitz.open(file_path) 打开 PDF
    # 2. 遍历每一页（enumerate 从 1 开始计数）
    # 3. 用 page.get_text("blocks") 获取文本块，过滤 block[6] == 0
    # 4. 将文本块用双换行连接，再用 _clean_text() 清理
    # 5. 构造 {"page": 页码, "text": 清理后文本} 字典
    # 6. 返回字典列表
    raise NotImplementedError("请在这里实现 read_pdf_pages")


def _clean_text(text: str) -> str:
    """清理提取的文本：将连续 3+ 个换行合并为 2 个。

    Parameters
    ----------
    text : str
        待清理的文本

    Returns
    -------
    str
        清理后的文本
    """
    return re.sub(r"\n{3,}", "\n\n", text).strip()
```

- [ ] **Step 4: 运行测试确认 NotImplementedError**

Run: `pytest tests/test_pdf_reader.py -v`
Expected: FAIL（`NotImplementedError: 请在这里实现 read_pdf`）

- [ ] **Step 5: 运行 ruff 检查代码风格**

Run: `ruff check common/pdf_reader.py tests/test_pdf_reader.py`
Expected: 无 lint 错误

- [ ] **Step 6: Commit**

```bash
git add common/pdf_reader.py tests/test_pdf_reader.py
git commit -m "feat: add pdf_reader module (TODO stubs) with tests"
```

---

### Task 3: milestone-1/milestone_rag_pdf.py（主脚本脚手架）

**Files:**
- Create: `milestone-1/milestone_rag_pdf.py`

- [ ] **Step 1: 创建主脚本**

```python
"""
Milestone 1 验证：PDF 端到端 RAG 问答

目标：
1. 读取一份真实 PDF 文档
2. 串联 W1-W4 全部能力：分块 → Embedding → Chroma 存储 → 检索 → Prompt → LLM
3. 通过交互式问答和预设评估，验证 RAG 管道的完整性和质量

⚠️ 规则：自己理解每一行代码，不要让 AI 帮你写逻辑
"""

from pathlib import Path

import chromadb

from common.embedding import get_embeddings
from common.llm import chat
from common.pdf_reader import read_pdf
from common.text_splitters import chunk_by_paragraph, chunk_by_sliding_window

# ============================
# 配置
# ============================
PDF_PATH = Path(__file__).parent / "data" / "xxx.pdf"  # TODO：替换为你选的 PDF 文件名


# ============================================================
# Part 1：PDF 读取 + 分块
# ============================================================

def load_and_chunk(pdf_path: str) -> list[str]:
    """
    读取 PDF 并分块

    TODO：自己实现
    提示：
    - 用 read_pdf(pdf_path) 获取全文文本
    - 打印文档总字数
    - 用 chunk_by_paragraph() 分块
    - 打印分块数量
    - 打印每块的前 50 字作为预览
    - 检查：如果分块数 < 3 或任意块超过 1000 字，打印警告并改用 chunk_by_sliding_window(text, 500, 100)
    - 返回分块列表
    """
    # 你的代码写在这里
    raise NotImplementedError("请在这里实现 load_and_chunk")


# ============================================================
# Part 2：构建向量知识库
# ============================================================

def build_knowledge_base(chunks: list[str]):
    """
    将分块向量化并存入 Chroma

    TODO：自己实现
    提示：
    - 用 get_embeddings(chunks) 获取向量
    - 创建 Chroma 内存客户端：chromadb.Client()
    - 创建 Collection：client.create_collection(name="milestone1")
    - 构造 ids 列表：["chunk_0", "chunk_1", ...]
    - 构造 metadatas 列表：[{"chunk_index": i, "char_count": len(chunk)}, ...]
    - 用 collection.add() 存入 ids, documents, embeddings, metadatas
    - 打印 collection 中的文档数量确认
    - 返回 collection
    """
    # 你的代码写在这里
    raise NotImplementedError("请在这里实现 build_knowledge_base")


# ============================================================
# Part 3：交互式问答
# ============================================================

def rag_retrieve(collection, query: str, top_k: int = 3) -> list[str]:
    """
    从向量知识库中检索与 query 最相关的文档块

    TODO：自己实现（可参考 W4 的 rag_retrieve）
    提示：
    - 用 get_embeddings([query]) 获取查询向量
    - 用 collection.query() 检索 Top-K
    - 打印检索到的文档块（前 80 字预览）
    - 返回文档块列表
    """
    # 你的代码写在这里
    raise NotImplementedError("请在这里实现 rag_retrieve")


def build_rag_prompt(query: str, context_chunks: list[str]) -> list[dict]:
    """
    将检索到的文档块组装成 RAG prompt

    TODO：自己实现（可参考 W4 的 build_rag_prompt）
    提示：
    - System Prompt：你是一个基于文档的问答助手，请基于提供的上下文回答问题，
      如果上下文中没有相关信息，请明确说"根据提供的资料，我无法回答这个问题"，不要编造信息
    - User Prompt："上下文信息：\n{context}\n\n问题：{query}"
    - 返回 messages 列表
    """
    # 你的代码写在这里
    raise NotImplementedError("请在这里实现 build_rag_prompt")


def rag_query(collection, query: str) -> str:
    """
    完整的 RAG 问答：检索 → Prompt → LLM

    TODO：自己实现
    提示：
    - 调用 rag_retrieve() 获取相关文档块
    - 调用 build_rag_prompt() 构造 prompt
    - 调用 chat() 获取 LLM 回复
    - 打印回复
    - 返回回复文本
    """
    # 你的代码写在这里
    raise NotImplementedError("请在这里实现 rag_query")


def interactive_qa(collection):
    """
    交互式问答循环

    已实现，不需要修改。
    """
    print("\n进入交互式问答（输入 quit 退出）")
    print("─" * 50)
    while True:
        query = input("\n你的问题: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            print("退出交互式问答。")
            break
        if not query:
            continue
        rag_query(collection, query)


# ============================================================
# Part 4：预设问题评估
# ============================================================

# TODO：选定 PDF 后，替换为基于文档内容的问题和参考答案
EVAL_QUESTIONS = [
    {
        "question": "（替换为基于你 PDF 内容的问题 1）",
        "reference": "（从文档中摘出的参考答案）",
        "aspect": "事实准确性",
    },
    {
        "question": "（替换为问题 2）",
        "reference": "（参考答案）",
        "aspect": "事实准确性",
    },
    {
        "question": "（替换为问题 3）",
        "reference": "（参考答案）",
        "aspect": "事实准确性",
    },
    {
        "question": "（替换为问题 4：需要跨多段整合信息）",
        "reference": "（参考答案）",
        "aspect": "综合性",
    },
    {
        "question": "（替换为问题 5：需要跨多段整合信息）",
        "reference": "（参考答案）",
        "aspect": "综合性",
    },
    {
        "question": "（替换为问题 6：文档中没有的信息，期望 LLM 拒绝回答）",
        "reference": "文档中未提及此内容",
        "aspect": "忠实度",
    },
]


def chat_without_rag(query: str) -> str:
    """直接问 LLM（无 RAG），用于对比评估。"""
    messages = [{"role": "user", "content": query}]
    return chat(messages)


def run_evaluation(collection):
    """
    预设问题评估：对比 RAG 回答、无 RAG 回答、参考答案

    已实现，不需要修改。
    """
    print("\n预设问题评估")
    print("=" * 60)

    for i, item in enumerate(EVAL_QUESTIONS, 1):
        question = item["question"]
        reference = item["reference"]
        aspect = item["aspect"]

        print(f"\n{'━' * 60}")
        print(f"问题 {i}（{aspect}）: {question}")
        print(f"{'━' * 60}")

        # RAG 回答
        print("\n📗 RAG 回答:")
        print("─" * 40)
        rag_answer = rag_query(collection, question)

        # 无 RAG 回答
        print("\n📕 无 RAG 回答（直接问 LLM）:")
        print("─" * 40)
        no_rag_answer = chat_without_rag(question)
        print(no_rag_answer)

        # 参考答案
        print("\n📘 参考答案:")
        print("─" * 40)
        print(reference)

        print()


# ============================================================
# 思考题（完成验证后回答）
# ============================================================
"""
🤔 完成里程碑验证后，回答以下问题：

Q1: 对比 PDF 文档和 W4 硬编码文本，RAG 效果有什么差异？你觉得主要原因是什么？
A1:

Q2: 在预设评估中，哪类问题 RAG 回答得最好？哪类最差？说明了什么？
A2:

Q3: 检索到的文档块和你预期的一样吗？如果不一样，你觉得瓶颈在哪里（分块？Embedding？检索？）？
A3:

Q4: 如果要把这个系统的回答质量从"能用"提升到"好用"，你会优先改进哪个环节？为什么？
A4:
"""


# ============================
# 主程序
# ============================
if __name__ == "__main__":
    print("🏁 Milestone 1：PDF 端到端 RAG 问答验证")
    print("=" * 60)

    # --- Part 1：PDF 读取 + 分块 ---
    print("\n📌 Part 1：PDF 读取 + 分块")
    print("-" * 40)
    chunks = load_and_chunk(str(PDF_PATH))

    # --- Part 2：构建知识库 ---
    print("\n📌 Part 2：构建向量知识库")
    print("-" * 40)
    collection = build_knowledge_base(chunks)

    # --- 选择模式 ---
    print("\n\n请选择验证模式：")
    print("  1 - 交互式问答")
    print("  2 - 预设问题评估")
    print("  3 - 两者都跑（先评估，再交互）")
    choice = input("请输入 (1/2/3): ").strip()

    if choice == "1":
        interactive_qa(collection)
    elif choice == "2":
        run_evaluation(collection)
    elif choice == "3":
        run_evaluation(collection)
        interactive_qa(collection)
    else:
        print("无效选择，默认运行预设问题评估。")
        run_evaluation(collection)

    print("\n\n💡 验证完成后请回答文件底部的思考题！")
```

- [ ] **Step 2: 运行 ruff 检查代码风格**

Run: `ruff check milestone-1/milestone_rag_pdf.py`
Expected: 无 lint 错误

- [ ] **Step 3: 验证 import 可解析**

Run: `python -c "import ast; ast.parse(open('milestone-1/milestone_rag_pdf.py').read()); print('syntax OK')"`
Expected: 输出 `syntax OK`

- [ ] **Step 4: Commit**

```bash
git add milestone-1/milestone_rag_pdf.py
git commit -m "feat: add milestone 1 RAG PDF validation script (TODO scaffolding)"
```

---

### Task 4: milestone-1/README.md

**Files:**
- Create: `milestone-1/README.md`

- [ ] **Step 1: 创建 README**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add milestone-1/README.md
git commit -m "docs: add milestone 1 README with validation instructions"
```

---

### Task 5: 最终验证

- [ ] **Step 1: 运行全量 lint**

Run: `ruff check .`
Expected: 无错误

- [ ] **Step 2: 运行现有测试确认无回归**

Run: `pytest -v --ignore=tests/test_pdf_reader.py`
Expected: 已有测试全部 PASS

- [ ] **Step 3: 确认 pdf_reader 测试的预期状态**

Run: `pytest tests/test_pdf_reader.py -v`
Expected: 全部 FAILED（`NotImplementedError: 请在这里实现 read_pdf`）——这是预期行为，学习者实现后会变为 PASS

- [ ] **Step 4: 确认文件结构**

Run: `find milestone-1 common/pdf_reader.py tests/test_pdf_reader.py -type f | sort`
Expected:
```
common/pdf_reader.py
milestone-1/README.md
milestone-1/data/.gitkeep
milestone-1/milestone_rag_pdf.py
tests/test_pdf_reader.py
```

- [ ] **Step 5: Commit（如有修复）**

仅在前面步骤发现问题并修复后才需要此步骤。
