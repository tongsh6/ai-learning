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
PDF_PATH = Path(__file__).parent / "data" / "rag_intro_zh.pdf"  # TODO：替换为你选的 PDF 文件名


# ============================================================
# Part 1：PDF 读取 + 分块
# ============================================================

def load_and_chunk(pdf_path: str) -> list[str]:
    """
    读取 PDF 并分块

    TODO：自己实现
    提示：
    - 用 read_pdf(pdf_path) 获取全文文本
    - 打印文档总字数。
    - 用 chunk_by_paragraph() 分块
    - 打印分块数量
    - 打印每块的前 50 字作为预览
    - 检查：如果分块数 < 3 或任意块超过 1000 字，打印警告并改用 chunk_by_sliding_window(text, 500, 100)
    - 返回分块列表
    """
    # 你的代码写在这里
    # raise NotImplementedError("请在这里实现 load_and_chunk")
    full_text = read_pdf(pdf_path)
    print(f"文档总字数: {len(full_text)}")
    chunks = chunk_by_paragraph(full_text)
    print(f"分块数量: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"块 {i} 预览: {chunk[:50]}")
    if len(chunks) < 3 or any(len(chunk) > 1000 for chunk in chunks):
        print("⚠️ 分块数过少或存在过长块，改用滑动窗口分块")
        chunks = chunk_by_sliding_window(full_text, 500, 100)
        print(f"滑动窗口分块数量: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"块 {i} 预览: {chunk[:50]}")
    return chunks



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
    # raise NotImplementedError("请在这里实现 build_knowledge_base")
    embeddings = get_embeddings(chunks)
    client = chromadb.Client()
    collection = client.create_collection(name="milestone1")
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"chunk_index": i, "char_count": len(chunk)} for i, chunk in enumerate(chunks)]
    collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
    print(f"知识库中存储的文档数量: {len(collection.get()['documents'])}")
    return collection

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
    # raise NotImplementedError("请在这里实现 rag_retrieve")
    query_embedding = get_embeddings([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    retrieved_chunks = results["documents"][0]
    for i, chunk in enumerate(retrieved_chunks):
        print(f"检索到的块 {i} 预览: {chunk[:80]}")
    return retrieved_chunks

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
    # raise NotImplementedError("请在这里实现 build_rag_prompt")
    system_prompt = "你是一个基于文档的问答助手，请基于提供的上下文回答问题，如果上下文中没有相关信息，请明确说'根据提供的资料，我无法回答这个问题'，不要编造信息。"
    user_prompt = f"上下文信息：\n{''.join(context_chunks)}\n\n问题：{query}"
    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]

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
    # raise NotImplementedError("请在这里实现 rag_query")
    retrieved_chunks = rag_retrieve(collection, query)
    prompt = build_rag_prompt(query, retrieved_chunks)
    answer = chat(prompt)
    print(f"RAG 回答: {answer}")
    return answer



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
        "question": "提示词工程（Prompt Engineering）在 RAG 中的应用",
        "reference": "一个好的 RAG Prompt 应该包含：* **角色设定**：如“你是一个严谨的文档分析专家”。* **约束条件**：如“仅基于提供的资料回答”、“如果没有请说不知道”。* **推理引导**：引导模型在回答前先列出引用来源。",
        "aspect": "事实准确性",
    },
    {
        "question": "检索的最后防线",
        "reference": "重排序（Reranking）：检索的最后防线初筛阶段为了速度通常使用向量检索（Bi-Encoder），但其精度有限。Reranking使用交叉编码器（Cross-Encoder）对 Top-K个结果进行深度语义比对，虽然速度慢，但能极大地过滤掉无关噪声，是提升 RAG质量的“银弹”。",
        "aspect": "事实准确性",
    },
    {
        "question": "如何提升回答质量",
        "reference": "通过 LLM 或信息熵方法剔除冗余句子，只保留核心证据，能显著提升回答质量",
        "aspect": "事实准确性",
    },
    {
        "question": "如何量化“好用”",
        "reference": "（参考答案）",
        "aspect": "综合性",
    },
    {
        "question": "RAG 系统中，哪些因素会导致回答质量不稳定？",
        "reference": "（参考答案）",
        "aspect": "综合性",
    },
    {
        "question": "Claude code interpreter 模式的核心能力是什么？",
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
A1: W4 的硬编码文本通常是精心挑选和优化过的，内容简洁且高度相关，适合直接被 LLM 理解和利用。而 PDF 文档则可能包含大量冗余、格式杂乱、语言不规范的文本，这些都会干扰 RAG 的检索和理解过程，导致回答质量下降。主要原因是 PDF 文档的噪声和非结构化特性，使得分块、Embedding 和检索环节都面临更大的挑战。
    

Q2: 在预设评估中，哪类问题 RAG 回答得最好？哪类最差？说明了什么？
A2: 通常来说，事实性强、直接从文档中可以找到答案的问题（如 Q1、Q2）RAG 回答得较好，因为它们依赖于检索到的相关信息。而需要综合推理、归纳总结或者文档中没有明确提及的问题（如 Q4、Q5、Q6）RAG 回答得较差，因为它们不仅需要准确检索，还需要更高层次的理解和推理能力。这说明 RAG 在处理明确的事实查询时表现较好，但在需要深度理解和推理的综合性问题上仍有提升空间。

Q3: 检索到的文档块和你预期的一样吗？如果不一样，你觉得瓶颈在哪里（分块？Embedding？检索？）？
A3: 检索到的文档块可能与预期不完全一致，尤其是在分块质量不高或者文档内容过于冗杂的情况下。瓶颈可能出现在分块环节，如果分块过大或过小，都会影响后续的 Embedding 和检索效果；也可能在 Embedding 环节，如果向量表示不能很好地捕捉文本语义，就会导致检索结果不相关；最后也可能是检索算法本身的限制，无法有效区分相关和不相关的块。需要具体分析每个环节的输出才能定位瓶颈。

Q4: 如果要把这个系统的回答质量从"能用"提升到"好用"，你会优先改进哪个环节？为什么？
A4: 1.原始文本的结构化处理 2.然后改进分块环节，因为分块的质量直接影响到后续的 Embedding 和检索效果。一个好的分块策略能够确保每个块都包含完整的语义单元，既不过于冗长也不过于碎片化，这样才能让 Embedding 
更准确地捕捉文本含义，检索时也更容易找到真正相关的块。相比之下，Embedding 和检索算法虽然重要，但如果输入的文本块质量不高，再先进的算法也难以弥补这个问题。因此，优化分块是提升整体回答质量的关键一步。
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
