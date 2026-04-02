"""
Week 6：Reranking 实验脚手架

目标：
1. 固定候选池，避免把召回和排序混在一起
2. 对已有候选结果重新打分排序
3. 比较重排序前后的 Top-K 变化

规则：
- 不要直接复制完整实现
- 优先复用 W5 的检索结果
- 先建立“排序是独立问题”的直觉，再考虑模型和框架
"""


def load_demo_document() -> str:
    """读取实验文档。"""
    raise NotImplementedError


def build_chunks(text: str) -> list[str]:
    """构建文本块。"""
    raise NotImplementedError


def retrieve_candidates(query: str, chunks: list[str], top_n: int = 10):
    """先用已有检索方法拿到候选池。"""
    raise NotImplementedError


def score_candidate(query: str, chunk: str) -> float:
    """对单个候选块打重排序分。"""
    raise NotImplementedError


def rerank_candidates(query: str, candidates):
    """对候选结果重新排序。"""
    raise NotImplementedError


def compare_rankings(query: str, before, after) -> None:
    """打印排序前后对比结果。"""
    raise NotImplementedError


def evaluate_queries() -> None:
    """对一组问题评估 reranking 收益。"""
    raise NotImplementedError


if __name__ == "__main__":
    print("请在这里完成 W6 reranking 实验。")
