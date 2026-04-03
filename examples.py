#!/usr/bin/env python3
"""
Poor Man's Router - 使用示例

运行: python examples.py
"""

from poor_mans_router import PoorManRouter


def demo_basic():
    """基础使用"""
    print("=" * 60)
    print("基础使用演示")
    print("=" * 60)

    router = PoorManRouter()

    # 推荐模型
    tasks = [
        "帮我写Python代码",
        "翻译成英文",
        "画一幅风景画",
        "生成一个视频",
    ]

    for task in tasks:
        result = router.get_best_for_task(task)
        print(f"\n📝 任务: {task}")
        print(f"   类型: {result['task_type']}")
        print(f"   建议: {result['suggestion']}")


def demo_status():
    """查看状态"""
    print("\n" + "=" * 60)
    print("模型状态")
    print("=" * 60)

    router = PoorManRouter()
    status = router.get_status()

    print(f"\n总计 {len(status)} 个模型")

    # 按类型分组
    by_type = {}
    for s in status:
        t = s['type']
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(s)

    for t, models in by_type.items():
        print(f"\n【{t.upper()}】")
        for m in models[:3]:
            icon = "✅" if m['available'] else "❌"
            print(f"  {icon} {m['provider']} {m['name']}")


def demo_selection():
    """手动选择"""
    print("\n" + "=" * 60)
    print("手动选择模型")
    print("=" * 60)

    router = PoorManRouter()

    # 只看chat模型
    print("\n📊 可用的Chat模型:")
    model = router.select_model("chat")
    if model:
        print(f"   推荐: {model.provider} {model.name}")
        print(f"   剩余: {model.quota_remaining} {model.quota_type}")

    # 看image模型
    print("\n📊 可用的Image模型:")
    model = router.select_model("image")
    if model:
        print(f"   推荐: {model.provider} {model.name}")
        print(f"   剩余: {model.quota_remaining} {model.quota_type}")


def demo_usage_record():
    """记录使用"""
    print("\n" + "=" * 60)
    print("记录使用量")
    print("=" * 60)

    router = PoorManRouter()

    # 记录使用
    router.record_usage("groq-llama-3.3-70b", tokens=10)

    # 查看状态
    model = router.select_model("chat")
    print(f"\n使用后: {model.name}")
    print(f"剩余额度: {model.quota_remaining} (记录了10次使用)")


if __name__ == "__main__":
    demo_basic()
    demo_status()
    demo_selection()
    demo_usage_record()

    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)
