# Week 3：向量数据库（Chroma）

## 目标
理解向量数据库解决什么问题——如何高效存储和检索 Embedding 向量，替代 W2 的暴力搜索。

## 核心概念
- **为什么需要向量数据库**：预计算 + 持久化 + 索引加速
- **Chroma 基本操作**：Client → Collection → Add → Query
- **ANN（近似最近邻）**：用少量精度损失换取大幅速度提升
- **Metadata 过滤**：在语义检索基础上叠加结构化筛选
- **持久化存储**：内存模式 vs 磁盘模式

## 实验列表

### 实验 1：`03_vector_search.py`（必做）
- 创建 Chroma 客户端和 Collection
- 将 W2 的文档分块存入 Chroma（手动传 embedding + 自动 embedding 两种方式）
- 用 Chroma 做语义检索，对比 W2 手写 `search_chunks()` 的结果
- 体验 metadata 过滤：按分块策略、块长度等条件筛选
- 持久化：将数据存到磁盘，重启后仍可检索
- 回答思考题

### 实验 2（选做扩展）：
- 用 W1 的 10 段文本存入 Chroma，对比 Chroma 内置 embedding 模型和 Ollama nomic-embed-text 的检索效果
- 尝试存入更大的文档（1000+ 块），感受检索速度的差异

## 运行方式

```bash
# 确保已安装 chromadb
pip install chromadb

# 运行实验
python week3-vector-db/03_vector_search.py
```

## 需要实现的函数

| 函数 | 难度 | 说明 |
|------|------|------|
| `create_collection()` | ⭐ | 创建 Chroma 客户端和 Collection |
| `add_chunks_manual()` | ⭐⭐ | 手动计算 embedding 后存入 Chroma |
| `add_chunks_auto()` | ⭐ | 让 Chroma 自动计算 embedding |
| `semantic_search()` | ⭐⭐ | 用 Chroma 的 query API 做语义检索 |
| `search_with_metadata()` | ⭐⭐ | 在检索基础上叠加 metadata 过滤 |
| `persistent_storage()` | ⭐ | 持久化存储到磁盘 |

## ⛔ 规则
- 每个函数自己写，理解每一行 Chroma API 调用
- 可以查 Chroma 官方文档
- W2 的分块函数可以直接从 `common/` 导入
- 写完后回答文件底部的思考题

## 补充阅读
- [Chroma 官方文档](https://docs.trychroma.com/)
- [像光速一样搜索——HNSW算法介绍](https://luxiangdong.com/2023/11/06/hnsw/) — HNSW 原理 + FAISS 代码示例
- [向量数据库核心索引技术 FLAT、HNSW、IVF 深度解析](https://blog.csdn.net/weixin_43156294/article/details/147401155) — 三种索引对比 + 选型指南

## 本周总结（完成后填写）
- 学到了什么：向量数据库的使用和原理，Chroma 的基本 API，ANN 索引的概念和优势，metadata 过滤的实战应用，持久化存储的配置方法。
- 踩了什么坑：Chroma查询结果返回的数据结构和W2手写函数不同
- 下周关注什么：没有特别要关注的 就是HNSW等核心原理和技术还未深入理解，后续会继续补充相关内容。
