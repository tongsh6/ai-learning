"""
Week 3 实验：向量数据库（Chroma）—— 高效存储和检索 Embedding 向量

目标：
1. 用 Chroma 替代 W2 的暴力搜索，理解向量数据库解决什么问题
2. 掌握 Chroma 的基本操作：创建、存储、检索、过滤
3. 对比 Chroma 检索和 W2 手写检索的结果

⚠️ 规则：自己理解每一行代码，不要让 AI 帮你写逻辑
"""

import chromadb

from common.embedding import get_embeddings
from common.text_splitters import chunk_by_paragraph
from common.search import search_chunks
# ============================
# 测试文档（复用 W2 的 RAG 说明文）
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
# 第一步：创建 Chroma 客户端和 Collection
# ============================
def create_collection():
    """
    创建一个内存模式的 Chroma 客户端，并创建一个 Collection

    TODO：自己实现
    提示：
    - chromadb.Client() 创建内存模式客户端
    - client.create_collection(name="xxx") 创建 Collection
    - 返回 (client, collection) 元组
    """
    # 你的代码写在这里
    doc_client = chromadb.Client()
    doc_collection = doc_client.create_collection(name="doc")
    return doc_client, doc_collection


# ============================
# 第二步：手动传入 Embedding 存储文档
# ============================
def add_chunks_manual(collection, chunks: list[str]):
    """
    先用我们自己的 Embedding API 计算向量，再存入 Chroma

    TODO：自己实现
    提示：
    - 用 get_embeddings(chunks) 获取所有块的向量
    - collection.add() 需要传入：
      - ids: 每条数据的唯一 ID（如 "chunk_0", "chunk_1", ...）
      - documents: 原始文本列表
      - embeddings: 向量列表
      - metadatas: 元数据列表（如 {"chunk_index": 0, "char_count": 120}）
    - 注意：ids 必须是字符串列表
    """
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"chunk_index": i, "char_count": len(chunk)} for i, chunk in enumerate(chunks)]
    chunks_embeddings = get_embeddings(chunks)
    # 打印向量
    print("\n📊 文本块的 Embedding 向量（前5维）:")
    for i, embedding in enumerate(chunks_embeddings):
        print(f"  [{i}] {embedding[:5]}... (长度: {len(embedding)})")

    collection.add(ids=ids, documents=chunks, embeddings=chunks_embeddings, metadatas=metadatas)


# ============================
# 第三步：用 Chroma 做语义检索
# ============================
def semantic_search(collection, query: str, top_k: int = 3):
    """
    用 Chroma 的 query API 做语义检索

    TODO：自己实现
    提示：
    - 先用 get_embeddings([query]) 获取查询向量
    - collection.query() 参数：
      - query_embeddings: 查询向量（注意是列表套列表）
      - n_results: 返回数量
    - 返回值是一个字典，包含 ids、documents、distances、metadatas
    - 打印出 Top-K 结果：排名、文本预览、距离
    """
    # 你的代码写在这里
    query_embeddings = get_embeddings([query])[0]
    results = collection.query(query_embeddings=[query_embeddings], n_results=top_k)
# 打印出 Top-K 结果
    print(f"\n🔍 查询：「{query}」")
    for i in range(len(results["ids"][0])):
        doc_id = results["ids"][0][i]
        doc_text = results["documents"][0][i]
        distance = results["distances"][0][i]
        print(f"  [{i}] (id: {doc_id}, distance: {distance:.4f}) {doc_text[:50]}...")
    return results

# ============================
# 第四步：Metadata 过滤
# ============================
def search_with_metadata(collection, query: str, min_length: int = 80):
    """
    在语义检索基础上，用 metadata 过滤短文本块

    TODO：自己实现
    提示：
    - collection.query() 可以加 where 参数做 metadata 过滤
    - where={"char_count": {"$gte": min_length}} 表示只返回字符数 >= min_length 的块
    - 对比有无过滤的检索结果差异
    """
    # 你的代码写在这里
    query_embeddings = get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embeddings],
        n_results=3,
        where={"char_count": {"$gte": min_length}},
    )
    print(f"\n🔍 查询：「{query}」 (过滤条件: char_count >= {min_length})")
    for i in range(len(results["ids"][0])):
        doc_id = results["ids"][0][i]
        doc_text = results["documents"][0][i]
        distance = results["distances"][0][i]
        print(f"  [{i}] (id: {doc_id}, distance: {distance:.4f}) {doc_text[:50]}...")

    return results


# ============================
# 第五步：持久化存储
# ============================
def persistent_storage(chunks: list[str]):
    """
    将数据持久化到磁盘，验证重启后数据仍在

    TODO：自己实现
    提示：
    - chromadb.PersistentClient(path="./chroma_data") 创建持久化客户端
    - 用 get_or_create_collection() 代替 create_collection()（避免重复创建报错）
    - 存入数据后，创建一个新的 PersistentClient 指向同一路径
    - 验证新客户端能读到之前存入的数据
    """
    # 你的代码写在这里
    persistent_client = chromadb.PersistentClient(path="./chroma_data")
    doc_collection = persistent_client.get_or_create_collection(name="doc")
    add_chunks_manual(doc_collection, chunks)
    print(f"✅ 数据已持久化，当前 Collection 共有 {doc_collection.count()} 条数据")


# ============================
# 第六步：对比 Chroma 和 W2 手写检索
# ============================
def compare_with_manual_search(collection, chunks: list[str], query: str):
    """
    对同一个查询，对比 Chroma 检索和 W2 手写 search_chunks() 的结果

    TODO：自己实现
    提示：
    - Chroma 检索：用 semantic_search()
    - 手写检索：导入 common.search.search_chunks，用同样的 query 和 chunks
    - 对比两者的 Top-3 结果是否一致
    - 思考：如果不一致，可能是什么原因？
    """
    # 你的代码写在这里
    print("\n🔍 Chroma 检索结果：")
    chroma_result= semantic_search(collection, query)

    chroma_result = [
        (chroma_result["ids"][0][i], chroma_result["distances"][0][i], chroma_result["documents"][0][i])
        for i in range(len(chroma_result["ids"][0]))
    ]

    print("\n🔍 手写检索结果：")
    manual_results = search_chunks(query, chunks)

    # 对比结果
    print("\n🔍 对比结果：")
    for i in range(3):
        chroma_doc = chroma_result[i] if i < len(chroma_result) else None
        manual_doc = manual_results[i] if i < len(manual_results) else None
        print(f"  Rank {i}:")
        print(f"    Chroma: {chroma_doc[2][:50]}..." if chroma_doc else "    Chroma: None")
        print(f"    Manual: {manual_doc[2][:50]}..." if manual_doc else "    Manual: None")
    print("\n💡 如果结果不一致，可能原因包括：")
    print("- Chroma 使用了 ANN 索引，可能有近似误差")
    print("- Embedding 计算可能有微小差异")
    print("- Metadata 过滤可能导致结果不同")




# ============================
# 第七步：思考题（不写代码，写注释回答）
# ============================
"""
🤔 完成实验后，回答以下问题（直接在这里写注释）：

Q1: Chroma 的 query 返回的 distances 和我们 W1 手写的余弦相似度有什么关系？
    （提示：观察 distances 的值域，和余弦相似度的 0~1 范围对比）
A1: 相似度= 1- distances, distances越小相似度越高 distances越大相似度越低

Q2: 为什么 Chroma 用 get_or_create_collection() 而不是 create_collection()？
    什么场景下用哪个更合适？
A2: get_or_create_collection 就不用重复创建collection了，适合有持久化存储需求的场景

Q3: Metadata 过滤是在向量检索之前还是之后执行的？这对性能有什么影响？
    （提示：想想 "先过滤再搜索" vs "先搜索再过滤" 的区别）
A3: 先过滤再搜索可以减少需要计算相似度的文本块数量，提高性能；先搜索再过滤可能会计算更多无关文本块的相似度，降低效率。

Q4: 如果你有 100 万个文档块，内存模式还合适吗？你会怎么选择存储方式？
A4: 需要磁盘存储，可以使用 Chroma 的 PersistentClient 来存储数据到磁盘，并且在需要时加载到内存中进行检索。

Q5: Chroma 默认使用 HNSW 索引。回忆我们讨论的"问路找餐厅"类比，
    ANN 检索可能会漏掉真正最相似的结果。在 RAG 场景中，这个精度损失可以接受吗？为什么？
A5: 可以接受，查询的结果是多条，用户可以从中选择最相关的结果，或者调整查询文本，因ANN检索的速度优势可以显著提升用户体验，尤其是在大规模数据集上。

Q6: 如果你的文档会不断更新（比如知识库每天新增文章），
    你觉得向量数据库需要支持哪些额外操作？
A6: 定时计算新文档的 Embedding 并添加到数据库中；支持删除过时文档；支持更新文档内容和对应的 Embedding；提供高效的增量索引更新机制，以保持检索性能。
"""


# ============================
# 主程序
# ============================
if __name__ == "__main__":
    print("🧪 Week 3 实验：向量数据库（Chroma）")
    print("=" * 60)

    # 准备分块数据（复用 W2 的按段落分块）
    chunks = chunk_by_paragraph(document)
    print(f"\n📄 原始文档长度：{len(document)} 字符")
    print(f"📦 按段落分块：{len(chunks)} 块")
    for i, chunk in enumerate(chunks):
        print(f"  [{i}] ({len(chunk)}字符) {chunk[:50]}...")

    # === 第一步：创建 Collection ===
    print("\n\n📌 第一步：创建 Chroma Collection")
    print("-" * 40)
    client, collection = create_collection()
    print(f"✅ Collection 创建成功：{collection}")

    # === 第二步：存入数据 ===
    print("\n\n📌 第二步：手动传入 Embedding 存储")
    print("-" * 40)
    add_chunks_manual(collection, chunks)
    print(f"✅ 存入 {collection.count()} 条数据")

    # === 第三步：语义检索 ===
    print("\n\n📌 第三步：语义检索")
    print("-" * 40)
    test_queries = [
        "分块大小怎么选择？",
        "RAG 系统有哪些组件？",
        "滑动窗口有什么优缺点？",
    ]
    for query in test_queries:
        print(f"\n🔍 查询：「{query}」")
        semantic_search(collection, query)

    # === 第四步：Metadata 过滤 ===
    print("\n\n📌 第四步：Metadata 过滤（只返回 >= 80 字符的块）")
    print("-" * 40)
    search_with_metadata(collection, "RAG 系统的组件", min_length=80)

    # === 第五步：持久化存储 ===
    print("\n\n📌 第五步：持久化存储")
    print("-" * 40)
    persistent_storage(chunks)

    # === 第六步：对比检索结果 ===
    print("\n\n📌 第六步：对比 Chroma 和手写检索")
    print("-" * 40)
    compare_with_manual_search(collection, chunks, "分块策略的优缺点")

    print("\n\n💡 完成后请回到文件底部回答思考题！")
