# CoverCraft · 封面工坊

根据视频脚本、视频描述或封面描述制作封面，支持参考图、中文标题、横竖画幅和可选人物。

A video-cover skill for AI agents. Turn a script, video summary, or visual brief into a cover; use reference images, generate or preserve Chinese headlines, and choose landscape/portrait with or without people.

## 真实 AI 生图案例

以下 **6 张实际封面**对应不同 AI 用途，包含 3 张原创人物封面、3 张无人物封面，横竖版各 3 张。选题为虚构案例；工具界面、论文、修复结果和模型回答为示意。点击图片查看 PNG 原图。

### 横版 · 16:9

| AI 做 PPT · B08 未来办公 | AI 编程 · B06 发布会实测 | AI 多模型对比 · B07 双阵营对比 |
| --- | --- | --- |
| <a href="examples/ai-topics-v2/images/02-ai-ppt.png"><img src="examples/ai-topics-v2/images/02-ai-ppt.png" alt="AI 做 PPT" width="280"></a> | <a href="examples/ai-topics-v2/images/05-ai-code.png"><img src="examples/ai-topics-v2/images/05-ai-code.png" alt="AI 编程" width="280"></a> | <a href="examples/ai-topics-v2/images/06-ai-models.png"><img src="examples/ai-topics-v2/images/06-ai-models.png" alt="AI 多模型对比" width="280"></a> |
| 无人物 | 原创虚拟人物 | 无人物 |

### 竖版 · 3:4

| AI 办公挑战 · B01 黄蓝冲击 | AI 读论文 · B03 白橙清单 | AI 修复照片 · B10 立体概念 |
| --- | --- | --- |
| <a href="examples/ai-topics-v2/images/01-ai-office.png"><img src="examples/ai-topics-v2/images/01-ai-office.png" alt="AI 办公挑战" width="280"></a> | <a href="examples/ai-topics-v2/images/03-ai-paper.png"><img src="examples/ai-topics-v2/images/03-ai-paper.png" alt="AI 读论文" width="280"></a> | <a href="examples/ai-topics-v2/images/04-ai-restore.png"><img src="examples/ai-topics-v2/images/04-ai-restore.png" alt="AI 修复照片" width="280"></a> |
| 原创虚拟人物 | 原创虚拟人物 | 无人物 |

[查看六个选题、设计依据和实际提示词](examples/ai-topics-v2/README.md)。这六个案例展示了六种风格，完整基础风格库共 10 种，30 个分支不代表均已实测。

## 能做什么

- **三种输入任选一种**：完整脚本、视频内容简介，或直接描述想要的封面画面；也可以组合。
- **参考图与风格延展**：10 种 AI 基础风格、30 个基础分支、31 个原参考档案；配色可按内容自由变化。
- **先确认画幅与人物**：只补问尚未明确的选择，不要求本人出镜。
- **GPT Image 优先**：不可用时使用平台自带生图工具；也支持用户自行配置并明确选用 OpenAI 图片 API。
- **输出与检查**：实际图片、PNG/JPEG 导出、缩略图、列表预览，以及中文文字核对与设计依据。

Skill 的完整入口在 [cover-craft/SKILL.md](cover-craft/SKILL.md)，使用条件和工具能力以宿主提供的实际工具为准。

## 10 种 AI 基础风格

| 编号 / 名称 | 独立的视觉结构 | 适用的 AI 内容 | 配色与标题起点 |
| --- | --- | --- | --- |
| B01 黄蓝冲击 | 大字、强色块、单一夸张动作或对象 | AI 工具亮相、办公挑战、功能变化 | 黄蓝或柠檬紫墨；粗斜字与明确描边 |
| B02 蓝黑科技 | 深色设备空间、透视、重点光域与工作流 | AI 编程、软件教程、自动化 | 蓝黑青白或深绿暖金；白色粗标题 |
| B03 白橙清单 | 浅底、层次清楚的任务卡和功能图标 | AI 技能列表、论文整理、步骤说明 | 白橙或晨雾薄荷；黑色粗字、重点条 |
| B04 彩色漫画 | 漫画轮廓、分格、问题与解法或夸张比喻 | AI 误区、功能讲解、模型概念 | 有限明亮色块；漫画轮廓字 |
| B05 极简编辑 | 大留白、单一 AI 工具或成果、一句观点 | AI 经验复盘、提示词、方法观点 | 中性色与一个重点色；编辑式标题 |
| B06 发布会实测 | 摄影工作室、主展示对象、体验或问答标题 | AI 新功能体验、工具评测、发布解读 | 炭黑暖金或灰蓝银白；粗斜标题与一处版本重点 |
| B07 双阵营对比 | 同等视觉重量的两区、共同任务与比较对象 | 两模型、两工具、两种 AI 做法的对比 | 冷暖或两套可区分色；两方名与一个主问题 |
| B08 未来办公 | 统一空间内的环幕、悬浮设备、成果舞台 | AI 办公、PPT、文档、Agent 协作 | 蓝紫云白或薄荷银灰；宽块字与少量任务标签 |
| B09 矩阵控制室 | 重复任务格阵、一个被强调的活动单元、控制台 | 多 Agent 调度、批处理、排错与知识库 | 深墨青电光或紫青；短大字，重点格最亮 |
| B10 立体概念 | 一个大 3D 概念物、剖面或尺度差解释关系 | AI 能力、Token、检索、图像修复和系统原理 | 白底黄黑或深靛珊瑚；重字与清楚对象轮廓 |


默认示例围绕 AI 工具、办公、编程、模型对比、Agent 与图像能力。每种风格均支持有人物、无人物及横竖版。风格规格与样张分别记录，不表示 30 个分支均已实测。

[YouTube / 哔哩哔哩封面调研与来源](cover-craft/references/ai-creator-cover-research.md)

## 安装

下载本仓库后进入 `cover-craft` 文件夹：

```bash
python3 scripts/install_skill.py --target codex
```

默认安装到 Codex 的用户技能目录；已有同名技能时，加 `--replace` 可先备份再替换。其他支持 Skill 的 Agent 平台请按其方式导入整个 `cover-craft` 文件夹，保留参考文档、图片和脚本。

API 是可选路径，配置说明见 [OpenAI 图片 API](cover-craft/references/openai-api-setup.md)。不需要把 API Key 写入仓库。公共版本不包含个人偏好记录；安装后只有你明确要求长期沿用时才保存设置。

## 使用

```text
$cover-craft

视频描述：教大家先在 ChatGPT 讨论开发需求，整理开发说明，再交给 Codex 实现。
做一张竖版 3:4，无人物。
没有标题，请帮我拟写；参考内置 R12-02 的冷暖分区，改成两工具接力。
只做一张，配色你决定。
```

也可以直接提供画面要求：

```text
$cover-craft

封面描述：深青书房背景，暖橙光照着右下方笔记本电脑。
左侧聊天面板，中央开发说明，发光箭头连接到电脑。
上方主标题逐字采用“Codex额度用太快？”，副标题“省额度小技巧”。
竖版 3:4，无人物，生成一张。
```

[完整说明](cover-craft/README.md) · [更多调用示例](cover-craft/references/examples.md) · [基础风格目录](cover-craft/references/style-catalog.md)

默认生成的是扁平图片，中文文字和参考素材需要验图；可编辑文字层是可选额外流程。实际生图模型由工具或所选 API 决定，未知型号不会被标成 GPT Image。
