"""
examples/run_demo.py
快速运行示例 —— 模拟三份合同文档的并行分析
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.pipeline import run_pipeline

# 模拟文档内容（实际使用时替换为 PDF/DOCX 解析内容）
SAMPLE_DOCS = [
    """
    采购合同 A
    甲方：XX科技有限公司  乙方：YY供应商
    合同金额：人民币 150 万元
    交货期：签订后 60 个工作日内
    违约条款：逾期交货每日罚款合同总额的 0.1%，累计上限 10%
    质保期：验收后 12 个月
    付款方式：预付 30%，验收后 60 天内付清余款
    """,
    """
    服务协议 B
    委托方：XX科技有限公司  服务方：ZZ咨询公司
    服务内容：企业数字化转型咨询，为期 6 个月
    服务费用：月费 20 万元，共计 120 万元
    保密条款：服务方不得向第三方披露委托方任何商业信息，违约赔偿 500 万元
    知识产权：项目成果归委托方所有
    终止条款：任意一方提前 30 天书面通知可终止合同
    """,
    """
    租赁合同 C
    出租方：AA物业管理公司  承租方：XX科技有限公司
    租赁物：北京市朝阳区某写字楼 15 层，建筑面积 2000 平方米
    租期：3 年，自 2026 年 6 月 1 日起
    月租金：人民币 30 万元，每年递增 5%
    押金：3 个月租金，共计 90 万元
    装修：承租方可自行装修，退租时恢复原状
    """,
]

if __name__ == "__main__":
    task = "请对以下三份合同进行综合分析，识别主要风险点、付款义务汇总和关键时间节点"

    print("=" * 60)
    print("🤖 DocMind Agent 多文档协作分析系统")
    print("=" * 60)
    print(f"📋 任务：{task}")
    print(f"📄 文档数量：{len(SAMPLE_DOCS)} 份")
    print("=" * 60)

    report = run_pipeline(task, SAMPLE_DOCS)

    print("\n" + "=" * 60)
    print("📊 最终分析报告")
    print("=" * 60)
    print(report)
