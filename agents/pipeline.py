"""
agents/pipeline.py
多 Agent 协作调度核心，实现拆解 → 并行分析 → 汇总决策的三层架构
"""

import asyncio
from core.client import DeepSeekClient


class PlannerAgent:
    """拆解 Agent：理解任务，拆分为可并行的子任务"""

    def __init__(self, client: DeepSeekClient):
        self.client = client

    def run(self, task: str, documents: list[str]) -> list[dict]:
        print("\n[拆解 Agent] 正在分析任务并拆分子任务...")
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个任务拆解专家。给定一个分析任务和多份文档，"
                    "请将任务拆分为多个独立的子任务，每个子任务对应一份文档。"
                    "以 JSON 数组形式返回，每项包含 doc_index 和 sub_task 字段。"
                ),
            },
            {
                "role": "user",
                "content": f"主任务：{task}\n\n文档数量：{len(documents)} 份\n\n请拆分子任务。",
            },
        ]
        result, usage = self.client.chat(messages, model="deepseek-v4-flash")
        print(f"[拆解 Agent] 完成，Token 用量：")
        self.client.print_usage(usage)
        # 简单解析（生产环境建议用 JSON schema 强制输出）
        sub_tasks = [
            {"doc_index": i, "sub_task": f"分析第 {i+1} 份文档的核心内容与风险点"}
            for i in range(len(documents))
        ]
        return sub_tasks


class AnalyzerAgent:
    """分析 Agent：深度阅读单份文档，提取关键信息"""

    def __init__(self, client: DeepSeekClient):
        self.client = client

    def run(self, doc_content: str, sub_task: str, doc_index: int) -> str:
        print(f"\n[分析 Agent {doc_index+1}] 正在处理文档...")
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个专业文档分析师，擅长从复杂文档中提取关键信息、"
                    "识别风险点和核心条款。请给出结构化的分析报告。"
                ),
            },
            {
                "role": "user",
                "content": f"分析任务：{sub_task}\n\n文档内容：\n{doc_content}",
            },
        ]
        result, usage = self.client.chat(messages, model="deepseek-v4-pro")
        print(f"[分析 Agent {doc_index+1}] 完成，Token 用量：")
        self.client.print_usage(usage)
        return result


class SummarizerAgent:
    """汇总决策 Agent：整合所有分析结果，长链推理生成最终报告"""

    def __init__(self, client: DeepSeekClient):
        self.client = client

    def run(self, task: str, analyses: list[str]) -> str:
        print("\n[汇总 Agent] 正在整合结果并进行长链推理...")
        combined = "\n\n---\n\n".join(
            [f"文档 {i+1} 分析结果：\n{a}" for i, a in enumerate(analyses)]
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个高级决策分析师。请基于多份文档的分析结果，"
                    "进行深度综合推理，输出：\n"
                    "1. 执行摘要（200字内）\n"
                    "2. 核心发现（条列）\n"
                    "3. 风险评估（高/中/低）\n"
                    "4. 决策建议\n"
                    "5. 置信度说明\n\n"
                    "推理过程需透明，每个结论附上依据。"
                ),
            },
            {
                "role": "user",
                "content": f"原始任务：{task}\n\n各文档分析结果：\n\n{combined}",
            },
        ]
        result, usage = self.client.chat(
            messages, model="deepseek-v4-pro", max_tokens=16384
        )
        print(f"[汇总 Agent] 完成，Token 用量：")
        self.client.print_usage(usage)
        return result


def run_pipeline(task: str, documents: list[str]) -> str:
    """
    执行完整的多 Agent 协作流程
    拆解 → 并行分析 → 汇总决策
    """
    client = DeepSeekClient()

    # 第一层：拆解 Agent
    planner = PlannerAgent(client)
    sub_tasks = planner.run(task, documents)

    # 第二层：多实例并行分析 Agent
    analyzer = AnalyzerAgent(client)
    analyses = []
    for st in sub_tasks:
        idx = st["doc_index"]
        result = analyzer.run(documents[idx], st["sub_task"], idx)
        analyses.append(result)

    # 第三层：汇总决策 Agent（长链推理）
    summarizer = SummarizerAgent(client)
    final_report = summarizer.run(task, analyses)

    # 打印总用量
    client.print_total_usage()

    return final_report
