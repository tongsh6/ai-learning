"""
Week 5 实验：混合检索（Hybrid Retrieval）

目标：
1. 理解为什么纯向量检索对精确术语类查询不够稳定
2. 手写最小 BM25 检索器
3. 对比 vector only / BM25 only / hybrid 三种方案

⚠️ 规则：
- 不要引入新框架，先用纯 Python 把原理跑通
- BM25 和融合排序先留在本周脚本，不要急着抽到 common/
- 先观察现象，再总结原因
"""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

from common.search import search_chunks
from common.text_splitters import chunk_by_paragraph

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "milestone-1" / "data" / "rag_intro_zh.txt"

EVAL_QUERIES = [
    {
        "label": "term",
        "query": "RAGas 是什么？",
        "expected_keyword": "RAGas",
    },
    {
        "label": "term",
        "query": "Prompt Engineering 是什么？",
        "expected_keyword": "Prompt Engineering",
    },
    {
        "label": "term",
        "query": "Reranking 的作用是什么？",
        "expected_keyword": "Reranking",
    },
    {
        "label": "term",
        "query": "Indexing 阶段会做什么？",
        "expected_keyword": "Indexing",
    },
    {
        "label": "semantic",
        "query": "为什么分块策略会影响检索质量？",
        "expected_keyword": "分块",
    },
    {
        "label": "semantic",
        "query": "为什么真实资料里的检索比演示文本更难？",
        "expected_keyword": "噪声",
    },
    {
        "label": "semantic",
        "query": "为什么不能把所有文档直接塞进模型上下文？",
        "expected_keyword": "上下文",
    },
    {
        "label": "semantic",
        "query": "为什么需要评估体系来判断 RAG 效果？",
        "expected_keyword": "评估",
    },
]


def load_demo_document() -> str:
    """
    读取本周实验文档。

    TODO：
    最小提示：
    - 复用里程碑里已经准备好的文本版资料
    - 直接从 DATA_PATH 读取 UTF-8 文本

    再提示：
    - 可以先判断 DATA_PATH.exists()
    - 文件存在时返回 read_text() 的结果，并顺手 strip() 一下首尾空白

    仍卡住时检查：
    - 返回值必须是 str，不要返回 Path
    - 如果文件不存在，报错信息里最好带上 DATA_PATH，方便定位
    """
    raise NotImplementedError("TODO: 实现 load_demo_document()")


def build_chunks(document: str) -> list[str]:
    """
    先复用最稳定的段落分块，降低本周变量数量。

    TODO：
    最小提示：
    - 调用 chunk_by_paragraph(document)
    - 返回分块后的列表

    再提示：
    - 可以在返回前打印：
      - 原文长度
      - chunk 数量
      - 每个 chunk 的前 40~60 个字符预览

    仍卡住时检查：
    - 空文档时 chunk 列表应为空
    - 本周先不要改 chunking 策略，避免实验变量混乱
    """
    raise NotImplementedError("TODO: 实现 build_chunks()")


def tokenize(text: str) -> list[str]:
    """
    一个“够用就好”的最小 tokenizer。

    目标不是做完美中文分词，而是先让这些信号可用：
    - 英文术语
    - 数字
    - 连续中文词片段

    TODO：
    最小提示：
    - 先统一转小写，减少英文大小写影响
    - 目标不是“最优分词”，而是“query 和 chunk 能产生可重叠 token”

    再提示：
    - 一种够用的做法：
      1. 用正则提取英文/数字 token，比如 `ragas`、`bm25`、`top`
      2. 用正则提取连续中文串
      3. 对每段中文串再做 2-gram / 3-gram 滑窗，补一点粗粒度中文 token
    - 例如“检索质量”可以切出：
      - 检索
      - 索质
      - 质量
      - 检索质
      - 索质量

    仍卡住时检查：
    - token 列表可以重复，后面 BM25 需要 TF
    - 不要在这里去重，否则词频信息会丢
    - 如果 query 是 “Prompt Engineering 是什么”，至少要能保留 `prompt`、`engineering`
    """
    raise NotImplementedError("TODO: 实现 tokenize()")


def build_bm25_index(chunks: list[str]) -> dict:
    """
    构建最小 BM25 所需索引。

    你至少需要这些信息：
    - tokenized_chunks
    - document_frequencies
    - document_lengths
    - average_document_length
    - total_documents

    TODO：
    最小提示：
    - 先对每个 chunk 调一次 tokenize()
    - BM25 的 index 本质上就是“预处理统计结果”

    再提示：
    - 推荐先得到：
      - tokenized_chunks: `list[list[str]]`
      - document_lengths: 每个 chunk 的 token 数
      - total_documents: `len(chunks)`
      - average_document_length: 所有长度平均值
    - DF 的统计方式：
      - 对每个 chunk 的 token 先转成 `set(...)`
      - 再累计每个 token 出现于多少个 chunk

    仍卡住时检查：
    - DF 统计的是“出现于多少篇文档”，不是“总共出现多少次”
    - `average_document_length` 不要按字符数算，要按 token 数算
    - 返回 dict 时，key 名尽量和上面列的一致，后面更好读
    """
    raise NotImplementedError("TODO: 实现 build_bm25_index()")


def bm25_score(
    query_tokens: list[str],
    chunk_tokens: list[str],
    document_frequencies: dict[str, int],
    total_documents: int,
    average_document_length: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """
    计算单个 chunk 的 BM25 分数。

    TODO：
    最小提示：
    - 你需要先知道当前 chunk 里每个 query token 的词频
    - 一个 chunk 的总分 = query 中每个 token 的贡献之和

    再提示：
    - 可以先写成下面这个思路：
      1. `chunk_tf = Counter(chunk_tokens)`
      2. 遍历 `query_tokens`
      3. 如果 token 不在当前 chunk 中，跳过
      4. 计算该 token 的 IDF
      5. 计算该 token 的 BM25 分项并累加
    - 常见 BM25 形式：
      - `idf = log(1 + (N - df + 0.5) / (df + 0.5))`
      - `score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))`

    仍卡住时检查：
    - `dl` 是当前 chunk 的 token 长度，不是字符长度
    - `avgdl` 可能为 0，最好先处理空数据边界
    - 同一个 query token 重复出现时，先允许重复累加，后续再观察是否要去重
    """
    raise NotImplementedError("TODO: 实现 bm25_score()")


def bm25_search(query: str, bm25_index: dict, chunks: list[str], top_k: int = 3):
    """
    用 BM25 对 chunks 排序。

    返回格式尽量对齐 common.search.search_chunks：
    - [(chunk_index, score, chunk_text), ...]

    TODO：
    最小提示：
    - 先把 query 变成 query_tokens
    - 再对每个 chunk 算一遍 bm25_score()

    再提示：
    - 可直接遍历 `enumerate(bm25_index["tokenized_chunks"])`
    - 每项结果组装成：
      - `(chunk_index, score, chunks[chunk_index])`
    - 最后按 score 从大到小排序，切片取前 `top_k`

    仍卡住时检查：
    - 返回格式要和 `search_chunks()` 尽量一致，这样后面的融合和打印更简单
    - `top_k <= 0` 时最好主动报错，和 `common.search` 保持一致
    - 如果 query_tokens 为空，结果应该是空列表或全 0 分，你自己选一种并保持一致
    """
    raise NotImplementedError("TODO: 实现 bm25_search()")


def vector_search(query: str, chunks: list[str], top_k: int = 3):
    """
    向量检索 baseline。

    TODO：
    最小提示：
    - 直接复用 common.search.search_chunks()

    再提示：
    - 这个函数基本只是“换一个更贴近本周语义的名字”
    - 目标是让主流程里能并排写：
      - `vector_results = vector_search(...)`
      - `bm25_results = bm25_search(...)`

    仍卡住时检查：
    - 不要在这里重复写 embedding 和 cosine 逻辑
    - 保持返回格式和 `search_chunks()` 完全一致
    """
    raise NotImplementedError("TODO: 实现 vector_search()")


def fuse_rankings(
    vector_results: list[tuple[int, float, str]],
    bm25_results: list[tuple[int, float, str]],
    top_k: int = 3,
) -> list[tuple[int, float, str]]:
    """
    合并两路检索结果。

    建议先做最简单的 rank-based fusion：
    - 第 1 名给更高分
    - 第 2 名给次高分
    - 同一 chunk 如果两路都出现，就累计得分

    TODO：
    最小提示：
    - 先不要管原始分数的量纲差异，直接按“名次”给分
    - 你的核心目标是：两路都出现的 chunk 得分更高

    再提示：
    - 一个简单方案：
      - 第 1 名加 `1 / 1`
      - 第 2 名加 `1 / 2`
      - 第 3 名加 `1 / 3`
    - 实现时可以维护：
      - `fused_scores: dict[int, float]`
      - `chunk_texts: dict[int, str]`
    - 分别遍历 `vector_results` 和 `bm25_results`，按名次累加

    仍卡住时检查：
    - 排序时要按融合后的分数降序
    - 返回仍然是 `(chunk_index, fused_score, chunk_text)` 的列表
    - 先别把原始 BM25 分和 cosine score 直接相加，它们量纲不同，不利于建立直觉
    """
    raise NotImplementedError("TODO: 实现 fuse_rankings()")


def print_results(title: str, results: list[tuple[int, float, str]]) -> None:
    """打印 Top-K 结果，方便观察。"""
    print(f"\n{title}")
    print("-" * len(title))
    for rank, (chunk_index, score, chunk_text) in enumerate(results, start=1):
        preview = re.sub(r"\s+", " ", chunk_text).strip()
        print(f"[{rank}] chunk={chunk_index} score={score:.4f} text={preview[:80]}...")


def evaluate_queries(chunks: list[str], bm25_index: dict, top_k: int = 3) -> None:
    """
    对比三种检索方案的表现。

    这里故意不做复杂指标，先做最小可观察评估：
    - 只检查 expected_keyword 是否出现在 Top-K 任一 chunk 中
    - 先建立“召回是否发生”的直觉

    TODO：
    最小提示：
    - 对每个 query 分别跑三种方案
    - 每种方案都打印 Top-K 和是否 hit

    再提示：
    - 判断 hit 的方式可以很简单：
      - 把 Top-K chunk 文本拼起来
      - 看 `expected_keyword` 是否出现在拼接后的文本里
    - 建议同时维护一个统计结构，例如：
      - `stats[scheme][label] = {"hit": 0, "total": 0}`
    - 三种 scheme：
      - `vector`
      - `bm25`
      - `hybrid`

    仍卡住时检查：
    - 先做“是否命中”的最小评估，不要一开始设计复杂指标
    - `term` 和 `semantic` 最后要分开看，否则看不出 hybrid 在哪类问题上更有价值
    - 每个 query 最好打印：
      - query 文本
      - query 类型
      - 三种方案的命中结果
    """
    raise NotImplementedError("TODO: 实现 evaluate_queries()")


def main() -> None:
    print("🧪 Week 5 实验：混合检索（Hybrid Retrieval）")
    print("=" * 60)
    print("本周唯一主问题：为什么纯向量检索不够稳，而 hybrid 更稳？")

    try:
        document = load_demo_document()
        chunks = build_chunks(document)
        bm25_index = build_bm25_index(chunks)
        evaluate_queries(chunks, bm25_index)
    except NotImplementedError as error:
        print(f"\n当前脚手架尚未完成：{error}")
        print("建议实现顺序：")
        print("1. load_demo_document()")
        print("2. build_chunks()")
        print("3. tokenize()")
        print("4. build_bm25_index()")
        print("5. bm25_score() + bm25_search()")
        print("6. vector_search() + fuse_rankings()")
        print("7. evaluate_queries()")


if __name__ == "__main__":
    main()
