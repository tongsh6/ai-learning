"""
Week 1 实验 1：Embedding 基础 —— 理解文本如何变成向量

目标：
1. 把 10 段中文文本转成 Embedding 向量
2. 手动计算余弦相似度
3. 观察：哪些文本语义相近？结果符合直觉吗？

⚠️ 规则：自己理解每一行代码，不要让 AI 帮你写逻辑
"""

from common.embedding import get_embeddings as shared_get_embeddings
from common.similarity import cosine_similarity as shared_cosine_similarity

# ============================
# 第一步：准备测试文本
# ============================
# 10 段中文文本，涵盖不同主题和相似度
texts = [
    # 技术相关（预期：1-2-3 相似度高）
    "Spring Boot 是一个 Java 微服务框架，简化了应用开发",              # 0
    "Java 后端开发常用 Spring Cloud 搭建微服务架构",                    # 1
    "Vue 3 是一个前端框架，使用组合式 API 提升开发体验",               # 2

    # 户外运动（预期：3-4-5 相似度高）
    "始祖鸟是一个高端户外运动品牌，产品线包括冲锋衣和登山装备",       # 3
    "周末去莫干山徒步，天气很好，走了 15 公里",                        # 4
    "攀岩是一项需要力量和技巧的极限运动",                              # 5

    # AI 相关（预期：6-7-8 相似度高）
    "RAG 系统通过检索外部知识来增强大语言模型的回答质量",              # 6
    "Embedding 将文本转换为高维向量，用于语义相似度计算",              # 7
    "大语言模型通过 Transformer 架构实现了文本的理解和生成",           # 8

    # 完全不相关
    "今天中午吃了一碗牛肉面，味道还不错",                              # 9
]

# ============================
# 第二步：调用 API 获取 Embedding
# ============================
def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    调用 Embedding API，返回每段文本的向量

    TODO：自己实现这个函数
    提示：
    - 发 POST 请求到 EMBEDDING_URL
    - Header 需要 Authorization: Bearer <API_KEY>
    - Body: {"input": texts, "model": "模型名"}
    - 返回的 data[i].embedding 就是向量
    """
    return shared_get_embeddings(texts, debug_response=False)


# ============================
# 第三步：计算余弦相似度
# ============================
def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    计算两个向量的余弦相似度

    公式：cos(θ) = (A · B) / (|A| × |B|)

    TODO：自己实现，不要用 sklearn
    提示：
    - A · B = sum(a_i * b_i)  点积
    - |A| = sqrt(sum(a_i^2))  向量模长
    """
    return shared_cosine_similarity(vec_a, vec_b)


# ============================
# 第四步：构建相似度矩阵并分析
# ============================
def analyze_similarities(texts: list[str], embeddings: list[list[float]]):
    """
    计算所有文本对之间的相似度，找出最相似和最不相似的组合
    """
    n = len(texts)

    # 计算所有两两相似度
    print("\n📊 相似度矩阵（越接近 1 越相似）：")
    print("-" * 80)

    similarities = []
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            similarities.append((i, j, sim))

    # 按相似度排序
    similarities.sort(key=lambda x: x[2], reverse=True)
    # 打印
    print("  " + "  ".join(f"[{i}]" for i in range(n)))
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append("  -  ")
            elif i < j:
                sim = next(sim for x, y, sim in similarities if (x, y) == (i, j))
                row.append(f"{sim:.2f}")
            else:
                sim = next(sim for x, y, sim in similarities if (x, y) == (j, i))
                row.append(f"{sim:.2f}")
        print(f"[{i}] " + "  ".join(row))

    # Top 5 最相似
    print("\n🔥 Top 5 最相似的文本对：")
    for i, j, sim in similarities[:5]:
        print(f"  [{i}] vs [{j}] = {sim:.4f}")
        print(f"    「{texts[i][:30]}...」")
        print(f"    「{texts[j][:30]}...」")
        print()

    # Top 5 最不相似
    print("\n❄️ Top 5 最不相似的文本对：")
    for i, j, sim in similarities[-5:]:
        print(f"  [{i}] vs [{j}] = {sim:.4f}")
        print(f"    「{texts[i][:30]}...」")
        print(f"    「{texts[j][:30]}...」")
        print()


# ============================
# 第五步：思考题（不写代码，写注释回答）
# ============================
"""
🤔 完成实验后，回答以下问题（直接在这里写注释）：

Q1: 同一主题（如技术/户外/AI）内的文本相似度大概在什么范围？
A1: 大概在 0.7-0.9 之间，具体数值取决于文本的具体内容和模型的理解能力。

Q2: 不同主题之间的相似度大概在什么范围？
A2: 大概在 0.53-0.55 之间，说明模型能够区分不同主题的文本。

Q3: "牛肉面"那句和其他所有文本的相似度如何？为什么？
A3: 相似度较低，因为"牛肉面"属于美食主题，与其他技术或户外主题的文本语义差异较大。

Q4: 如果你要搜索"微服务架构怎么设计"，Embedding 检索能找到正确的文本吗？
A4: 不能，会有很多干扰项，因为 Embedding 只能捕捉英文本的语义相似度，无法理解用户的具体需求和上下文。

Q5: 你觉得这个 Embedding 模型对中文的理解够好吗？有什么局限？
A5: 不够好，对于表达习惯和方式的理解有限，可能会误判一些文本的相似度，尤其是结构相同但语义不同的文本。

Q6: 向量维度是多少？维度越高一定越好吗？
A6: 768维，维度高不一定好，可能会有稀疏性和计算效率问题。
"""


# ============================
# 主程序
# ============================
if __name__ == "__main__":
    print("🧪 Week 1 实验：Embedding 基础")
    print("=" * 60)

    # 打印所有测试文本
    print("\n📝 测试文本：")
    for i, text in enumerate(texts):
        print(f"  [{i}] {text}")

    # 获取 Embedding
    print("\n⏳ 正在获取 Embedding...")
    embeddings = get_embeddings(texts)
    print(f"✅ 获取完成！每个向量维度：{len(embeddings[0])}")

    # 分析相似度
    analyze_similarities(texts, embeddings)

    print("\n💡 完成后请回到文件底部回答思考题！")

