# 📄 DocMind Agent — 企业智能文档分析系统

> 基于 DeepSeek V4 的多 Agent 协作文档处理框架，支持百万级上下文长链推理

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![DeepSeek](https://img.shields.io/badge/Model-DeepSeek--V4--Pro-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚨 核心痛点

企业内部每天产生大量非结构化文档（合同、研报、财务报告），传统处理方式存在以下问题：

- 人工审阅单份复杂文档平均耗时 **2-4 小时**
- 主流大模型上下文窗口受限，长文档必须分片处理，导致**信息截断与推理失真**
- 多文档交叉分析时，信息整合完全依赖人工，**决策质量不稳定**

---

## 🧠 解决方案：多 Agent 协作架构

本项目采用三层 Agent 协作范式，充分利用 DeepSeek V4 的超长上下文能力：

```
用户输入
   │
   ▼
┌─────────────────┐
│  拆解 Agent      │  ← 任务理解 & 子任务分配
└────────┬────────┘
         │ 并行分发
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐   ← 多实例并行分析 Agent
│分析 A │ │分析 B │      同时处理多份原始文档
└───┬───┘ └───┬───┘
    └────┬────┘
         ▼
┌─────────────────┐
│  汇总决策 Agent  │  ← 长链推理 + 结构化报告输出
└─────────────────┘
```

### Agent 职责说明

| Agent | 职责 | 模型 |
|-------|------|------|
| 拆解 Agent | 理解任务，拆分并行子任务 | deepseek-v4-flash |
| 分析 Agent（多实例） | 深度阅读文档，提取关键信息 | deepseek-v4-pro |
| 汇总决策 Agent | 整合结果，长链推理，生成报告 | deepseek-v4-pro |

---

## 📁 项目结构

```
docmind-agent/
├── agents/
│   ├── planner.py        # 拆解 Agent
│   ├── analyzer.py       # 分析 Agent（支持多实例并行）
│   └── summarizer.py     # 汇总决策 Agent（长链推理）
├── core/
│   ├── client.py         # DeepSeek API 客户端封装
│   ├── pipeline.py       # Agent 调度与消息路由
│   └── models.py         # 数据结构定义
├── examples/
│   └── run_demo.py       # 快速运行示例
├── requirements.txt
└── README.md
```

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API Key

```bash
export DEEPSEEK_API_KEY="your_api_key_here"
```

### 运行示例

```bash
python examples/run_demo.py --input ./docs/sample_contract.pdf
```

---

## 📊 预期成效

| 指标 | 改善前 | 改善后 |
|------|--------|--------|
| 单文档处理时长 | 2-4 小时 | < 8 分钟 |
| 人工介入率 | 100% | ~20% |
| 日均可处理文档量 | 10-20 份 | 500+ 份 |
| 日均 Token 消耗 | — | 300-500 万 |

---

## 🔧 技术栈

- **大模型**：DeepSeek V4 Pro / Flash
- **框架**：Python asyncio（异步并行 Agent）
- **文档解析**：PyMuPDF、python-docx
- **接口协议**：OpenAI 兼容 API

---

## 📄 License

MIT
