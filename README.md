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
- 模型、框架和协议都按“当前主流能力”动态替换，不把路线绑定到某个固定模型名或框架名
- 可观测性和评估要前移：从 RAG 优化阶段开始记录实验结果，Agent 阶段必须能追踪每一步工具调用和状态变化

## 2026-05 路线校准

当前路线不推倒重来，只做三点校准：

1. **模型名去硬编码**：W10-W13 不再固定押注 `GPT-4o-mini` 或某个厂商模型，而是按当时可用的主流低成本模型和推理模型选择。
2. **MCP 前移到工具调用阶段**：W10 开始对比传统 Function Calling 与 MCP 工具接口，重点理解工具描述、权限边界、输入校验和审计。
3. **观测与评估前移**：W5 开始保存结构化实验结果，W8-W9 引入 tracing / eval 思维，W13 负责整合展示，而不是最后才补。

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
| **W5** | 混合检索 + 实验记录 | BM25 + 向量双路检索，合并排序，对比纯向量效果；把查询、Top-K、命中情况和结论结构化落盘 | `05_hybrid_search.py` |
| **W6** | Reranking | Cross-Encoder 或轻量规则重排序，量化 Top-K 准确率、延迟和成本；明确区分“召回不全”与“排序不准” | `06_reranking.py` |
| **W7** | 查询改写 + 多路召回控制 | HyDE、Query Expansion、多路去重；对比 Late Chunking / 段落分块 / 滑窗分块，不把任何策略当默认最优；补充 CRAG / Self-RAG 的适用边界 | `07_query_enhancement.py` |
| **W8** | RAG 评估（上） | 手写 Retrieval Recall、Precision、MRR；构建评测数据集（问题-标准答案-证据块）；开始形成“证据质量可量化”的意识 | `08_rag_evaluation.py` |
| **W9** | RAG 评估（下） | 手写 Answer Faithfulness（LLM-as-Judge）；补充拒答质量、误答率、安全失败率、引用一致性；引入最小 tracing / eval 报告定位瓶颈 | `09_rag_evaluation_advanced.py` |

**里程碑**：能对 RAG 系统做量化评估，定位"是检索不行还是生成不行"。

---

## 第三阶段：Agent 工程（Week 10-13）

> ⚠️ 本阶段切换至**云端 API**。模型按当时主流能力选择：低成本模型用于常规工具调用，推理模型用于复杂规划和长任务验证。重点不只是“会调模型”，而是“能把不稳定模型放进可控系统”。

| 周 | 主题 | 实验 | 交付物 |
|---|---|---|---|
| **W10** | 可靠工具调用 + MCP 入门 | 环境切换（云端 API 配置）；Function Calling + 工具 Schema 设计 + 参数校验 + 工具白名单 + 超时/重试/降级；补一个最小 MCP 工具接口对照实验，理解工具协议和权限边界 | `10_reliable_tool_calling.py` |
| **W11** | Agent Runtime 基础 | ReAct / 分步规划；探讨推理模型对 Agent 规划层的重塑与约束；补充状态管理、checkpoint/resume、最大轮次、人类审批、补偿式回滚、工具调用审计 | `11_agent_runtime.py` |
| **W12** | Agentic RAG + 执行编排 | Agent 判断是否检索、何时检索、何时拒答、何时请求人工确认；FastAPI 暴露接口；补充上下文压缩、关键状态保留、敏感信息不进模型上下文 | `12_agentic_rag/` |
| **W13** | 综合项目收尾 | 多文档支持与安全加固；整合 tracing、评估报告、工具调用轨迹和人工干预点；**发挥 Vue 前端优势，交付 Controllable Agent Dashboard（可视化状态交互看板，支持 HITL 断点干预与 DAG 渲染）** | `13_final_project/` |

**里程碑**：可演示的完整系统，不只“能跑通”，还要能解释为什么这样设计、怎么失败恢复、如何做最低限度安全防护。

---

## 面试补充（贯穿全程）

| 周 | 补充内容 | 对应面试题 |
|---|---|---|
| W3 | HNSW / IVF 索引原理 | Q4、Q8 |
| W4 | Prompt Injection、上下文预算、非可信上下文 | 安全追问 |
| W7 | Late Chunking、CRAG / Self-RAG 变体及适用边界 | Q13、Q15 |
| W10 | Function Calling、MCP、工具权限边界、工具调用审计 | 工具调用追问 |
| W11 | Agent 状态管理、工具失败恢复、人工审批 | Q20、Q22 |
| W13 | 多语言 RAG、Token 成本控制、Agent 落地边界、可观测性 | Q29、Q30 |

---

## 技术栈

```text
W1-W9（RAG 阶段）：
  LLM：Ollama qwen3:8b
  Embedding：bge-m3（W2 起替换 nomic-embed-text）
  向量库：Chroma
  全手写 Python

W10-W13（Agent 阶段）：
  LLM：当前主流低成本模型 + 当前主流推理模型（按价格、上下文、工具调用稳定性动态选择）
  Tool Protocol：Function Calling + 最小 MCP 工具接口对照
  Agent Runtime：先手写最小闭环，再引入 Controllable DAG 编排思想
  API / 前端：FastAPI + Vue 3（实现 Controllable Agent 可视化交互看板）
  可观测性：结构化日志 + tracing + LangSmith 或 Phoenix
  重点能力：Tool Calling、MCP、状态管理（Checkpoint）、上下文压缩、安全防御（防注入）、人类协同（HITL）、审计与回滚
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
