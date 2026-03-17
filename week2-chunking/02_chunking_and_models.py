"""
Week 2 实验：文本分块（Chunking）—— 理解"怎么切"对检索质量的影响

目标：
1. 实现 3 种分块策略：固定长度、按段落、滑动窗口
2. 对同一篇文档，对比不同策略的分块效果
3. 观察：不同切法如何影响语义完整性？

⚠️ 规则：自己理解每一行代码，不要让 AI 帮你写逻辑
"""

from common.embedding import get_embeddings as shared_get_embeddings
from common.search import search_chunks as shared_search_chunks
from common.similarity import cosine_similarity as shared_cosine_similarity
from common.text_splitters import chunk_by_fixed_length as shared_chunk_by_fixed_length
from common.text_splitters import chunk_by_paragraph as shared_chunk_by_paragraph
from common.text_splitters import chunk_by_sliding_window as shared_chunk_by_sliding_window

# ============================
# 测试文档：一篇关于 RAG 的中文文章
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


# ============================
# 第一步：实现三种分块策略
# ============================


def chunk_by_fixed_length(text: str, chunk_size: int = 200) -> list[str]:
    """
    固定长度分块：每 chunk_size 个字符切一块

    TODO：自己实现
    提示：
    - 从头开始，每隔 chunk_size 个字符切一刀
    - 最后不足 chunk_size 的部分也要保留
    - 注意：这里用字符数，不是 token 数（简化处理）
    """
    return shared_chunk_by_fixed_length(text, chunk_size)



def chunk_by_paragraph(text: str) -> list[str]:
    """
    按段落分块：以空行（两个换行符）为分隔符

    TODO：自己实现
    提示：
    - 用 text.split() 按空行分割
    - 过滤掉空字符串
    - 每个段落 strip() 去掉首尾空白
    """
    return shared_chunk_by_paragraph(text)



def chunk_by_sliding_window(
    text: str, window_size: int = 200, overlap: int = 50
) -> list[str]:
    """
    滑动窗口分块：窗口大小 window_size，重叠 overlap 个字符

    TODO：自己实现
    提示：
    - 起始位置从 0 开始，每次前进 (window_size - overlap) 个字符
    - 每次取 [start : start + window_size] 的内容
    - 直到 start >= len(text) 时停止
    """
    return shared_chunk_by_sliding_window(text, window_size, overlap)


# ============================
# 第二步：对比分块结果
# ============================


def show_chunks(chunks: list[str], strategy_name: str):
    """展示分块结果"""
    print(f"\n{'=' * 60}")
    print(f"📦 策略：{strategy_name}（共 {len(chunks)} 块）")
    print(f"{'=' * 60}")
    for i, chunk in enumerate(chunks):
        print(f"\n--- 块 {i} （{len(chunk)} 字符）---")
        # 只显示前 80 个字符 + 后 30 个字符
        if len(chunk) > 120:
            print(f"  {chunk[:80]}...{chunk[-30:]}")
        else:
            print(f"  {chunk}")


# ============================
# 第三步：用 Embedding 检索测试分块质量
# ============================


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    调用 Embedding API（复用 W1 的实现）

    TODO：把你 W1 写好的代码复制过来
    """
    return shared_get_embeddings(texts)



def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    余弦相似度（复用 W1 的实现）

    TODO：把你 W1 写好的代码复制过来
    """
    return shared_cosine_similarity(vec_a, vec_b)



def search_chunks(
    query: str, chunks: list[str], embeddings: list[list[float]], top_k: int = 3
) -> list[tuple[int, float, str]]:
    """
    给定一个查询，从分块中找到最相关的 top_k 个块

    TODO：自己实现
    提示：
    1. 先获取 query 的 embedding
    2. 计算 query 和每个 chunk 的余弦相似度
    3. 按相似度降序排列，返回 top_k 个
    4. 返回格式：[(chunk_index, similarity, chunk_text), ...]
    """



    return shared_search_chunks(query, chunks, embeddings, top_k)


# ============================
# 第四步：对比不同策略的检索效果
# ============================


def compare_strategies(query: str):
    """对同一个查询，对比三种分块策略的检索结果"""
    print(f"\n🔍 查询：「{query}」")
    print(f"{'=' * 60}")

    strategies = {
        "固定长度（200字符）": chunk_by_fixed_length(document, chunk_size=200),
        "按段落": chunk_by_paragraph(document),
        "滑动窗口（200字符，50重叠）": chunk_by_sliding_window(
            document, window_size=200, overlap=50
        ),
    }

    for name, chunks in strategies.items():
        print(f"\n📦 策略：{name}（{len(chunks)} 块）")
        print("-" * 40)

        # 获取所有块的 embedding
        embeddings = get_embeddings(chunks)

        # 检索最相关的块
        results = search_chunks(query, chunks, embeddings, top_k=10)

        for rank, (idx, sim, text) in enumerate(results, 1):
            preview = text[:60].replace("\n", " ")
            print(f"  Top-{rank}: 块[{idx}] (相似度={sim:.4f})")
            print(f"         「{preview}...」")


# ============================
# 第五步：思考题
# ============================
"""
🤔 完成实验后，回答以下问题（直接在这里写注释）：

Q1: 三种策略分别产生了多少个块？哪种最多，为什么？
A1: 
    固定长度：4 按段落：7 滑动窗口：5 
    按段落最多，因为按段落策略分割的结果取决于原始文本的段落结构

Q2: 固定长度分块有什么明显的问题？举一个被切断的例子。
A2: 
    固定长度分块的问题是会把连续的语义进行分割，

Q3: 对于查询"分块大小怎么选"，哪种策略检索效果最好？为什么？
A3: 按段落检索效果最好，因为原始文档是段落结构的，分块后具有天然的语义连续性

Q4: 滑动窗口的 overlap 有什么作用？如果 overlap=0，和固定长度有什么区别？
A4: overlap的作用是决定块与块之间的重叠程度，overlap为0，那么和固定长度没有区别

Q5: 如果文档是代码（而不是自然语言），你会怎么分块？
A5: 按照滑动窗口分块，因为具有强烈的上下文关联性

Q6: 在实际 RAG 系统中，你会选哪种策略？为什么？
A6: 取决于RAG系统的应用场景，聊天记录 滑动窗口 知识库 段落  
"""


# ============================
# 主程序
# ============================
if __name__ == "__main__":
    print("🧪 Week 2 实验：文本分块（Chunking）")
    print("=" * 60)

    # 展示原始文档
    print(f"\n📄 原始文档长度：{len(document)} 字符")

    # 第一步：展示三种分块结果
    chunks_fixed = chunk_by_fixed_length(document, chunk_size=200)
    show_chunks(chunks_fixed, "固定长度（200字符）")

    chunks_paragraph = chunk_by_paragraph(document)
    show_chunks(chunks_paragraph, "按段落")

    chunks_sliding = chunk_by_sliding_window(document, window_size=200, overlap=50)
    show_chunks(chunks_sliding, "滑动窗口（200字符，50重叠）")

    # 第二步：检索对比
    print("\n\n" + "=" * 60)
    print("🔬 检索效果对比")
    print("=" * 60)

    test_queries = [
        "分块大小怎么选择？",
        "RAG 系统有哪些组件？",
        "滑动窗口有什么优缺点？",
    ]

    for query in test_queries:
        compare_strategies(query)

    print("\n💡 完成后请回到文件底部回答思考题！")

