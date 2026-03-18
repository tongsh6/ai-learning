"""
Week 4 实验：Prompt 基础 + RAG 管道

目标：
1. 理解 Prompt 工程基础：System Prompt、Few-shot、Context Window
2. 串联 W1-W3 组装完整的端到端 RAG 问答系统
3. 对比有无 RAG 的回答质量

⚠️ 规则：自己理解每一行代码，不要让 AI 帮你写逻辑
"""

import chromadb

from common.embedding import get_embeddings
from common.llm import chat
from common.text_splitters import chunk_by_paragraph

# ============================
# 测试文档（复用 W2/W3 的 RAG 说明文）
# ============================
document = """
检索增强生成（RAG）是一种结合信息检索与文本生成的技术架构。它的核心思想是：在大语言模型生成回答之前，先从外部知识库中检索相关信息，将检索结果作为上下文提供给模型，从而提高回答的准确性和可靠性。

RAG 系统通常由三个核心组件构成：文档处理管道、检索引擎和生成模型。文档处理管道负责将原始文档转换为可检索的格式，包括文本提取、清洗、分块和向量化。检索引擎负责根据用户查询找到最相关的文档片段。生成模型则基于检索到的上下文生成最终回答。

文本分块是 RAG 系统中最关键的预处理步骤之一。分块策略直接影响检索质量：块太大，信息被稀释，检索不精确；块太小，上下文被切断，语义不完整。常见的分块策略包括固定长度分块、按段落分块和滑动窗口分块。

固定长度分块是最简单的方法，按照固定的字符数或 token 数切分文本。优点是实现简单、块大小均匀；缺点是可能在句子中间切断，破坏语义完整性。

按段落分块以自然段落为单位切分，保持了段落内的语义完整性。优点是语义边界清晰；缺点是段落长度不均，有的段落可能太长或太短。

滑动窗口分块使用固定窗口大小，但相邻块之间有重叠（overlap）。优点是不会遗漏边界信息；缺点是产生冗余数据，增加存储和计算成本。

在实际工程中，分块大小的选择需要根据具体场景进行权衡。对于问答系统，通常推荐 256-512 个 token 的块大小。对于摘要任务，可能需要更大的块来保持完整上下文。最佳实践是通过实验对比不同策略的检索效果，选择最适合当前数据和任务的方案。
""".strip()


# ============================================================
# Part 1：Prompt 工程基础
# ============================================================


# ============================
# 第一步：最基本的 LLM 调用
# ============================
def simple_chat(user_message: str) -> str:
    """
    用最简单的方式调用 LLM：只传一条 user 消息

    TODO：自己实现
    提示：
    - 构造 messages 列表，只包含一条 {"role": "user", "content": user_message}
    - 调用 chat(messages) 获取回复
    - 打印并返回回复内容
    """
    # 你的代码写在这里
    messages = [{"role": "user", "content": user_message}]
    content = chat(messages)
    # 打印
    print(f"用户消息: {user_message}")
    print(f"模型回复: {content}")
    return content


# ============================
# 第二步：System Prompt 的作用
# ============================
def chat_with_system_prompt(system_prompt: str, user_message: str) -> str:
    """
    使用 System Prompt 设定 LLM 的角色和行为

    TODO：自己实现
    提示：
    - messages 列表包含两条消息：
      1. {"role": "system", "content": system_prompt}
      2. {"role": "user", "content": user_message}
    - 调用 chat(messages) 获取回复
    - 打印并返回回复内容
    """
    # 你的代码写在这里
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    content = chat(messages)
    # 打印
    print(f"System Prompt: {system_prompt}")
    print(f"用户消息: {user_message}")
    print(f"模型回复: {content}")
    return content


def experiment_system_prompts():
    """
    对比不同 System Prompt 对同一问题的回答差异

    TODO：自己实现
    提示：
    - 准备 2-3 个不同的 System Prompt，例如：
      1. "你是一位严谨的技术专家，回答要精确简洁。"
      2. "你是一位耐心的老师，回答要通俗易懂，多用比喻。"
      3. "你是一位段子手，回答要幽默风趣。"
    - 用同一个问题（如 "什么是向量数据库？"）分别调用
    - 对比三次回答的风格差异
    """
    # 你的代码写在这里
    system_prompts = [
        "你是一位严谨的技术专家，回答要精确简洁。",
        "你是一位耐心的老师，回答要通俗易懂，多用比喻。",
        "你是一位段子手，回答要幽默风趣。",
    ]
    user_message = "什么是向量数据库？"
    for sp in system_prompts:
        print(f"\n{'─' * 50}")
        chat_with_system_prompt(sp, user_message)


# ============================
# 第三步：Few-shot Prompting
# ============================
def few_shot_experiment():
    """
    用 Few-shot 示例引导 LLM 按特定格式回答

    TODO：自己实现
    提示：
    - 场景：让 LLM 对技术概念给出"一句话定义 + 一个比喻"格式的回答
    - Zero-shot：直接问 "用一句话定义 + 一个比喻解释：什么是 Embedding？"
    - Few-shot：在 user 消息中先给 1-2 个示例，再问目标问题
      示例格式：
        Q: 什么是数据库？
        A: 定义：数据库是结构化存储和管理数据的系统。比喻：就像一个有索引的图书馆，你可以快速找到任何一本书。

        Q: 什么是 API？
        A: 定义：API 是程序之间通信的标准接口。比喻：就像餐厅的菜单，你不需要知道厨房怎么做菜，只需要看菜单点菜。

        Q: 什么是 Embedding？
        A:
    - 对比两次回答的格式和质量
    """
    # 你的代码写在这里
    # Zero-shot
    print("\nZero-shot:")
    zero_shot_query = "用一句话定义 + 一个比喻解释：什么是 Embedding？"
    simple_chat(zero_shot_query)

    # prompt with few-shot examples
    print("\nFew-shot:")
    few_shot_query = """Q: 什么是数据库？
A: 定义：数据库是结构化存储和管理数据的系统。比喻：就像一个有索引的图书馆，你可以快速找到任何一本书。

Q: 什么是 API？
A: 定义：API 是程序之间通信的标准接口。比喻：就像餐厅的菜单，你不需要知道厨房怎么做菜，只需要看菜单点菜。

Q: 什么是 Embedding？
A: 
"""
    simple_chat(few_shot_query)


# ============================
# 第四步：理解 Context Window
# ============================
def context_window_demo():
    """
    演示 Context Window 的限制

    TODO：自己实现
    提示：
    - 打印出 document 的字符数和估算的 token 数
      （中文粗略估算：1 个汉字 ≈ 1.5-2 个 token）
    - 假设 context window = 32K tokens，计算这篇文档占了多少比例
    - 思考：如果文档有 100 页（约 5 万字），直接塞进去会怎样？
    - 这就是为什么需要 RAG：先检索相关片段，只把需要的部分送入 LLM
    """
    # 你的代码写在这里
    char_count = len(document)
    token_estimate = int(char_count * 1.75)  # 粗略估算
    context_window = 32000
    proportion = token_estimate / context_window * 100
    print(f"文档字符数: {char_count}")
    print(f"文档估算 token 数: {token_estimate}")
    print(f"占 Context Window 的比例: {proportion:.2f}%")
    print("如果文档有 100 页（约 5 万字），直接塞进去会超出 Context Window，LLM 可能只能看到部分内容，导致回答不完整或错误。这就是 RAG 的价值：先检索相关片段，只把需要的部分送入 LLM。")


# ============================================================
# Part 2：组装 RAG 管道
# ============================================================


# ============================
# 第五步：构建向量知识库
# ============================
def build_knowledge_base(doc: str):
    """
    将文档分块、向量化、存入 Chroma（复用 W2-W3 的能力）

    TODO：自己实现
    提示：
    - 用 chunk_by_paragraph(doc) 分块
    - 用 get_embeddings(chunks) 获取向量
    - 创建 Chroma 内存客户端和 Collection
    - 将 chunks + embeddings 存入 Collection
    - 返回 collection（后续检索用）
    """
    # 你的代码写在这里
    # 分块
    chunks = chunk_by_paragraph(doc)
    # 向量
    doc_embeddings = get_embeddings(chunks)
    # chroma 客户端和 Collection
    client = chromadb.Client()
    doc_collection = client.create_collection(name="doc")
    # 存入 Collection
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"chunk_index": i, "char_count": len(chunk)} for i, chunk in enumerate(chunks)]

    doc_collection.add(
        ids=ids,
        documents=chunks,
        embeddings=doc_embeddings,
        metadatas=metadatas,
    )
    return doc_collection


# ============================
# 第六步：RAG 检索 + Prompt 构造
# ============================
def rag_retrieve(doc_collection, query: str, top_k: int = 3) -> list[str]:
    """
    从向量知识库中检索与 query 最相关的文档块

    TODO：自己实现
    提示：
    - 用 get_embeddings([query]) 获取查询向量
    - 用 collection.query() 检索 Top-K
    - 返回检索到的文档块列表（纯文本）
    - 打印检索结果供观察
    """
    # 你的代码写在这里
    query_embedding = get_embeddings([query])[0]
    results = doc_collection.query(query_embeddings=[query_embedding], n_results=top_k)
    retrieved_chunks = results["documents"][0]  # 因为 query_embeddings 是列表
    print("\n🔍 RAG 检索到的相关文档块:")
    for i, chunk in enumerate(retrieved_chunks):
        print(f"  [{i}] {chunk[:100]}...")  # 打印前100字符预览
    return retrieved_chunks

def build_rag_prompt(query: str, context_chunks: list[str]) -> list[dict[str, str]]:
    """
    将检索到的文档块组装成 RAG prompt

    TODO：自己实现
    提示：
    - System Prompt 要告诉 LLM：
      1. 你是一个问答助手
      2. 请基于以下提供的上下文信息回答问题
      3. 如果上下文中没有相关信息，请明确说"根据提供的资料，我无法回答这个问题"
      4. 不要编造信息
    - User Prompt 结构：
      "上下文信息：\n{context}\n\n问题：{query}"
    - context 是将 context_chunks 用换行符连接起来的文本
    - 返回完整的 messages 列表
    """
    # 你的代码写在这里
    system_prompt = (
        "你是一个问答助手。请基于以下提供的上下文信息回答问题。如果上下文中没有相关信息，请明确说'根据提供的资料，我无法回答这个问题'。不要编造信息。"
    )
    context = "\n".join(context_chunks)
    user_prompt = f"上下文信息：\n{context}\n\n问题：{query}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return messages


# ============================
# 第七步：端到端 RAG 问答
# ============================
def rag_query(doc_collection, query: str) -> str:
    """
    完整的 RAG 问答流程：检索 → 构造 Prompt → LLM 生成

    TODO：自己实现
    提示：
    - 调用 rag_retrieve() 获取相关文档块
    - 调用 build_rag_prompt() 构造 prompt
    - 调用 chat() 获取 LLM 回复
    - 打印并返回回复
    """
    # 你的代码写在这里
    retrieved_chunks = rag_retrieve(doc_collection, query)
    query_messages = build_rag_prompt(query,retrieved_chunks)
    content = chat(query_messages)
    # 打印
    print(f"用户消息: {query_messages}")
    print(f"模型回复: {content}")




# ============================
# 第八步：对比实验 —— 有无 RAG 的差异
# ============================
def compare_with_and_without_rag(collection):
    """
    对比直接问 LLM 和 RAG 增强后的回答质量

    TODO：自己实现
    提示：
    - 准备 2-3 个关于文档内容的问题，例如：
      1. "RAG 系统由哪些核心组件构成？"
      2. "文本分块策略有哪些？各有什么优缺点？"
      3. "分块大小应该怎么选择？"
    - 对每个问题：
      1. 直接问 LLM（无 RAG）：simple_chat(query)
      2. RAG 增强后问：rag_query(collection, query)
    - 对比两者的回答：准确性、具体性、是否有幻觉
    """
    # 你的代码写在这里
    user_queries = [
        "RAG 系统由哪些核心组件构成？",
        "文本分块策略有哪些？各有什么优缺点？",
        "分块大小应该怎么选择？",
    ]
    for q in user_queries:
        print(f"\n{'─' * 50}")
        print(f"问题: {q}")
        print("\n直接问 LLM（无 RAG）:")
        simple_chat(q)
        print("\nRAG 增强后问:")
        rag_query(collection, q)


# ============================
# 思考题（不写代码，写注释回答）
# ============================
"""
🤔 完成实验后，回答以下问题（直接在这里写注释）：

Q1: System Prompt 和 User Prompt 的区别是什么？如果冲突了，LLM 会听谁的？
A1: System Prompt是给模型设定的规则，通常是一些角色定义、范围、风格等；User Prompt是用户的具体指令或者问题；我推断如果冲突了，应该是System Prompt优先，一般来说，在计算机世界中，系统指令会高于用户指令

Q2: 为什么 RAG 的 System Prompt 要强调"如果上下文中没有相关信息，请说不知道"？
A2: RAG检索系统中，要求的是对搜索结果的精准性，不需要模型进行额外的发挥，对已有信息检索后返回即可

Q3: Context Window 有限，但检索回来的文档块可能很多。你会怎么决定送入多少块？
A3: 在判断窗口的大小后，先计算每块的token数量，按照相关性排序，优先送入相关性高的块，直到达到窗口限制为止

Q4: Few-shot 示例放在 System Prompt 里好，还是放在 User Prompt 里好？为什么？
A4: 放在User Prompt里好，因为Few-shot示例是用户提供的具体指导，放在User Prompt里更符合语义和逻辑结构；System Prompt更适合放置模型的角色设定和行为规范

Q5: 如果 RAG 检索到了错误的文档块，LLM 会怎么表现？这说明了什么？
A5: 检索到错误的文档块，那么LLM也会返回错误的结果，这说明RAG的质量影响LLM返回的结果，同样也能知道LLM的prompt设计的好坏，会影响LLM的输出结果，差的prompt设计让LLM产生幻觉的概率更高
"""
"""
学到了什么：0 对模型chat接口的使用过 1 System prompt和User prompt的使用 2 RAG检索与LLM联动进行问答 3 指令的好坏影响LLM的输出 
踩了什么坑：模型接口超时时间设置过短，导致LLM生成较长回答时经常超时失败，后来调整了环境变量LLM_TIMEOUT_SECONDS=600才稳定下来
下周关注什么：第一阶段结束，需要进行里程碑验证 第二阶段要开始了
"""

# ============================
# 主程序
# ============================
if __name__ == "__main__":
    print("🧪 Week 4 实验：Prompt 基础 + RAG 管道")
    print("=" * 60)

    # === Part 1：Prompt 工程基础 ===
    print("\n\n🔹 Part 1：Prompt 工程基础")
    print("=" * 60)

    # --- 第一步：基本 LLM 调用 ---
    print("\n📌 第一步：最基本的 LLM 调用")
    print("-" * 40)
    # simple_chat("你好，请用一句话介绍你自己。")

    # --- 第二步：System Prompt ---
    print("\n\n📌 第二步：System Prompt 的作用")
    print("-" * 40)
    # experiment_system_prompts()

    # --- 第三步：Few-shot ---
    print("\n\n📌 第三步：Few-shot Prompting")
    print("-" * 40)
    # few_shot_experiment()

    # --- 第四步：Context Window ---
    print("\n\n📌 第四步：Context Window 限制")
    print("-" * 40)
    # context_window_demo()

    # === Part 2：组装 RAG 管道 ===
    print("\n\n🔹 Part 2：组装 RAG 管道")
    print("=" * 60)

    # --- 第五步：构建知识库 ---
    print("\n📌 第五步：构建向量知识库")
    print("-" * 40)
    collection = build_knowledge_base(document)

    # --- 第六步 & 第七步：RAG 问答 ---
    print("\n\n📌 第六步 & 第七步：RAG 问答测试")
    print("-" * 40)
    test_queries = [
        "RAG 系统由哪些核心组件构成？",
        "文本分块策略有哪些？各有什么优缺点？",
        "分块大小应该怎么选择？",
    ]
    # for q in test_queries:
    #     print(f"\n{'─' * 50}")
    #     rag_query(collection, q)

    # --- 第八步：对比实验 ---
    print("\n\n📌 第八步：对比有无 RAG 的回答质量")
    print("-" * 40)
    compare_with_and_without_rag(collection)

    print("\n\n💡 完成后请回到文件底部回答思考题！")
