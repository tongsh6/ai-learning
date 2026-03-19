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
