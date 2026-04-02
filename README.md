# AI 工程学习路线（13 周）

> **目标**：全栈开发者 → 能独立设计、实现、优化 RAG + Agent 系统的 AI 工程师
> **节奏**：每周 5-10 小时，每周 1-2 个动手实验 + 思考题
> **方式**：苏格拉底式引导，代码自己写

## 路线设计原则

- 先打牢 RAG 基础，再进入 Agent；不跳过检索、评估、失败分析这些基本功
- 每周只围绕一个主问题展开，重点建立“现象 -> 原因 -> 结论”的工程直觉
- Agent 不是“让模型自由发挥”，而是把不稳定模型放进可控系统：工具白名单、状态管理、重试降级、人工审批、安全边界
- 传统工程能力依然重要，但要补上 LLM 特有问题：上下文预算、Prompt 注入、模型幻觉、厂商限流、非确定性输出
- 优先自己实现最小闭环，再决定是否抽公共模块、是否引入框架

---

## 第一阶段：基础构建（Week 1-4）

| 周 | 主题 | 实验 | 交付物 |
|---|---|---|---|
| **W1** ✅ | Embedding 基础 | 调 API 获取向量、手写余弦相似度、分析相似度矩阵 | `01_embedding_basics.py` |
| **W2** | 分块 + 模型选型 | 实现 3 种 Chunking 策略（固定长度/按段落/滑动窗口）；理解“怎么切文本”本质上是在决定后续能否召回证据；选做：拉 `bge-m3` 对比 `nomic-embed-text` | `02_chunking_and_models.py` |
| **W3** | 向量数据库 | Chroma 存储向量、语义搜索、Top-K 检索；补充阅读 HNSW/IVF 原理；初步理解“什么适合进向量库，什么不适合” | `03_vector_search.py` |
| **W4** | Prompt 基础 + RAG 管道 | 上半周：System Prompt、Few-shot、上下文预算；补充：RAG 中的 Prompt Injection 与非可信上下文；下半周：串联 W2-W3 组装完整 RAG | `04_basic_rag.py` |

**里程碑**：用中文友好模型 + 自己写的代码，对一份 PDF 文档问答。

---

## 第二阶段：RAG 进阶（Week 5-9）

| 周 | 主题 | 实验 | 交付物 |
|---|---|---|---|
| **W5** | 混合检索 | BM25 + 向量双路检索，合并排序，对比纯向量效果 | `05_hybrid_search.py` |
| **W6** | Reranking | Cross-Encoder 重排序，量化 Top-K 准确率提升；明确区分“召回不全”与“排序不准” | `06_reranking.py` |
| **W7** | 查询改写 + 多路召回控制 | HyDE、Query Expansion，多路合并去重；补充：Late Chunking、CRAG / Self-RAG 变体；学习何时该改写查询、何时不该过度依赖模型自由发挥 | `07_query_enhancement.py` |
| **W8** | RAG 评估（上） | 手写 Retrieval Recall 和 Precision；构建评测数据集（问题-标准答案对）；开始形成“证据质量可量化”的意识 | `08_rag_evaluation.py` |
| **W9** | RAG 评估（下） | 手写 Answer Faithfulness（LLM-as-Judge）；补充拒答质量、误答率、安全失败率等维度；端到端评估报告，定位瓶颈 | `09_rag_evaluation_advanced.py` |

**里程碑**：能对 RAG 系统做量化评估，定位"是检索不行还是生成不行"。

---

## 第三阶段：Agent 工程（Week 10-13）

> ⚠️ 本阶段切换至**云端 API**（GPT-4o-mini 或 Qwen-Max），重点不只是“会调模型”，而是“能把不稳定模型放进可控系统”

| 周 | 主题 | 实验 | 交付物 |
|---|---|---|---|
| **W10** | 可靠工具调用 | 环境切换（云端 API 配置）；主线：Function Calling + 工具 Schema 设计 + 参数校验 + 工具白名单 + 超时/重试/降级；目标不是“调起来”，而是“调得可控” | `10_reliable_tool_calling.py` |
| **W11** | Agent Runtime 基础 | ReAct / 分步规划；补充：状态管理、checkpoint / resume、最大轮次、人类审批、补偿式回滚；理解 Agent 不等于“无限循环调用模型” | `11_agent_runtime.py` |
| **W12** | Agentic RAG + 执行编排 | Agent 判断是否检索、何时检索、何时拒答、何时请求人工确认；FastAPI 暴露接口；补充上下文压缩与关键状态保留 | `12_agentic_rag/` |
| **W13** | 综合项目收尾 | 接入 LangSmith / Phoenix 可观测性；多文档支持；失败案例分析；加入 Prompt 注入、工具幻觉、限流超时等验收场景；整理为面试作品 | `13_final_project/` |

**里程碑**：可演示的完整系统，不只“能跑通”，还要能解释为什么这样设计、怎么失败恢复、如何做最低限度安全防护。

---

## 面试补充（贯穿全程）

| 周 | 补充内容 | 对应面试题 |
|---|---|---|
| W3 | HNSW / IVF 索引原理 | Q4、Q8 |
| W4 | Prompt Injection、上下文预算、非可信上下文 | 安全追问 |
| W7 | Late Chunking、CRAG / Self-RAG 变体 | Q13、Q15 |
| W11 | Agent 状态管理、工具失败恢复、人工审批 | Q20、Q22 |
| W13 | 多语言 RAG、Token 成本控制、Agent 落地边界 | Q29、Q30 |

---

## 技术栈

```text
W1-W9（RAG 阶段）：
  LLM：Ollama qwen3:8b
  Embedding：bge-m3（W2 起替换 nomic-embed-text）
  向量库：Chroma
  全手写 Python

W10-W13（Agent 阶段）：
  LLM：GPT-4o-mini 或 Qwen-Max（云端 API）
  Agent Runtime：先手写最小闭环，必要时再引入编排框架
  API 框架：FastAPI
  可观测性：LangSmith 或 Phoenix
  重点能力：Tool Calling、状态管理、上下文压缩、失败恢复、安全防护
```

---

## 快速开始

```bash
# 安装开发环境（包含 pytest / ruff）
pip install -e .[dev]

# 初始化本地配置
python scripts/dev.py init-env
```

默认配置走本地 Ollama 的 OpenAI 兼容 Embedding 接口：

```env
EMBEDDING_URL=http://localhost:11434/v1/embeddings
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_API_KEY=ollama
```

---

## 本地开发命令

推荐统一使用跨平台脚本 [scripts/dev.py](D:/AI/ai-learning/scripts/dev.py)：

```bash
# 安装依赖
python scripts/dev.py install

# 初始化 .env
python scripts/dev.py init-env

# 运行静态检查
python scripts/dev.py lint

# 运行测试
python scripts/dev.py test

# 一次跑完 lint + test
python scripts/dev.py check

# 运行每周实验
python scripts/dev.py week1
python scripts/dev.py week2
```

---

## CI

仓库已提供最小 GitHub Actions 工作流 [.github/workflows/ci.yml](D:/AI/ai-learning/.github/workflows/ci.yml)：

- Python 3.11
- 安装 `pip install -e .[dev]`
- 执行 `ruff check .`
- 执行 `pytest`
- 运行平台：Linux / macOS / Windows

这意味着后续新增公共模块或测试时，可以直接纳入统一质量门禁。

Python 项目元数据、`pytest` 配置和 `ruff` 配置已集中放在 [pyproject.toml](D:/AI/ai-learning/pyproject.toml)。

---

## 当前工程化状态

当前已经具备这些基础能力：

- 公共配置：`common/config.py`
- Embedding 封装：`common/embedding.py`
- 相似度封装：`common/similarity.py`
- 分块封装：`common/text_splitters.py`
- 检索封装：`common/search.py`
- 基础测试：`tests/`
- 跨平台开发脚本：`scripts/dev.py`
- 最小 CI：`.github/workflows/ci.yml`

---

## 规则

- 核心逻辑自己写，不要让 AI 生成完整实现
- 可以查文档，卡住超过 30 分钟找导师要提示
- 每周在对应 README 里写 3 句话总结：学到了什么、踩了什么坑、下周关注什么

---

## 课件生成规范

后续新增或重写周课件时，统一参考 [COURSEWARE_TEMPLATE.md](/Users/tongshuanglong/ai/ai-learning/COURSEWARE_TEMPLATE.md)。

课件生成经验和评审结论统一沉淀在 [COURSEWARE_LOG.md](/Users/tongshuanglong/ai/ai-learning/COURSEWARE_LOG.md)，更新时机与 `LEARNING_LOG.md` 一致。

目标不是让 AI “多写内容”，而是确保课件满足：

- 只围绕一个主问题展开
- 生成前必须参考 `README.md`、`LEARNING_LOG.md` 和 `COURSEWARE_LOG.md`
- 代码组织必须遵守当前项目架构
- 能承接上周并为下周铺垫
- 有完整实验闭环和验收标准
- 会显式暴露常见误区，而不是只给结论
