# 🪓 Poor Man's Router - 穷鬼智能模型路由

> 专为初学者和小用量用户设计的免费AI模型路由
> 
> 参考：唐斩AI编程系列指南

[English](README_EN.md) | 中文

## ✨ 功能特点

- 🎯 **智能选择** - 根据任务类型自动选择最优模型
- 💰 **性价比优先** - DeepSeek V3.2性价比最高
- 📊 **额度监控** - 追踪使用量，额度用完自动切换
- 🔄 **免费优先** - Groq每日1440次免费额度
- 🌐 **无需代理** - 大部分模型不需要代理

## 🚀 快速开始

```bash
pip install poor-mans-router
```

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 根据任务推荐模型
result = router.get_best_for_task("帮我写Python代码")
print(result['suggestion'])
```

## 📦 支持的模型

### 性价比之选 ⭐⭐⭐

| 模型 | 提供商 | 类型 | 说明 |
|------|--------|------|------|
| **DeepSeek V3.2** | DeepSeek | 按量付费 | 性价比最高，没有之一 |
| **GLM-4.7** | 智谱AI | CodingPlan | 编程能力强，数理逻辑好 |
| **Kimi K2.5** | Kimi | CodingPlan | 便宜够用，官方支持 |
| **MiniMax 2.1** | MiniMax | CodingPlan | 能力强，老牌推荐 |

### 免费额度 ⭐⭐

| 模型 | 提供商 | 每日额度 | 需要代理 |
|------|--------|---------|---------|
| Llama 3.3 70B | Groq | 1440次/天 | ❌ |
| Mixtral 8x7B | Groq | 1440次/天 | ❌ |
| Gemma 2 9B | Groq | 1440次/天 | ❌ |
| NVIDIA NIM | NVIDIA | 无限(限速40rpm) | ❌ |
| OpenCode Zen | OpenCode | 有免费额度 | ❌ |
| Command R+ | Cohere | 1000次/月 | ❌ |
| Gemini Pro | Google | 60 RPM | ❌ |

### 聚合平台

| 平台 | 特点 |
|------|------|
| **OpenRouter** | 聚合50+模型，方便切换，可设每日上限 |

### ❌ 不推荐

| 模型 | 原因 |
|------|------|
| Claude | 政策严，易封号，不推荐接入第三方 |

## 💡 使用示例

```python
from poor_mans_router import PoorManRouter

router = PoorManRouter()

# 1. 任务推荐
result = router.get_best_for_task("写Python代码")
# → 推荐 DeepSeek V3.2（性价比最高）

# 2. 免费优先
result = router.get_best_for_task("简单问答")
# → 推荐 Groq Llama 3.3 70B（每日1440次免费）

# 3. 查看状态
status = router.get_status()
for s in status:
    if s['available']:
        print(f"{s['provider']} {s['name']}: {s['percent']:.0f}%")
```

## 📚 模型选择指南

### 按场景

| 场景 | 推荐 |
|------|------|
| 编程开发 | DeepSeek V3.2 / GLM-4.7 |
| 中文对话 | Kimi K2.5 / GLM-4.7 |
| 省钱优先 | Groq (每日1440次免费) |
| 快速原型 | OpenCode Zen (有免费额度) |

### 按成本

| 成本 | 推荐方案 |
|------|---------|
| 完全免费 | Groq (1440次/天) |
| 低成本 | DeepSeek V3.2 (按量付费) |
| 包月 | Kimi K2.5 / GLM-4.7 CodingPlan |

## ⚠️ 注意事项

1. **按量付费建议设置上限** - 避免意外超支
2. **Claude不推荐** - 政策严格，易封号
3. **DeepSeek V3.2** - 性价比最高，但需要付费
4. **OpenRouter** - 方便切换，建议设置每日限额

## 📂 项目结构

```
poor-mans-router/
├── SKILL.md              # 详细文档
├── README.md             # 本文件
├── poor_mans_router.py   # 核心代码
├── setup.py              # pip安装配置
└── examples.py          # 使用示例
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License

---

**声明：** 本项目仅供学习和研究使用。模型额度信息可能随提供商政策变化而变化，请以官方为准。
