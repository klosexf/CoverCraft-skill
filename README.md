# CoverCraft · 封面工坊

根据视频脚本、视频描述或封面描述制作封面，支持参考图、中文标题、横竖画幅和可选人物。

A video-cover skill for AI agents. Turn a script, video summary, or visual brief into a cover; use reference images, generate or preserve Chinese headlines, and choose landscape/portrait with or without people.

## 真实生图案例

下面是使用 Codex 内置图片工具实际生成的 **6 张封面**：五种基础风格加一个冷暖接力延展，包含 3 张原创人物封面和 3 张无人物封面。人物为 AI 生成的虚拟角色，软件界面为示意设计。点击图片可查看 PNG 大图。

每种风格均支持有人物或无人物，下表标的是本次样张设置。

### 横版 · 16:9

| 黄蓝冲击 · 原创人物 | 彩色漫画 · 无人物 | 冷暖接力 · 原创人物 |
| --- | --- | --- |
| <a href="examples/images/01-yellow-blue-presenter.png"><img src="examples/images/01-yellow-blue-presenter.png" alt="黄蓝冲击：AI 工作搭档" width="280"></a> | <a href="examples/images/04-color-comic-no-person.png"><img src="examples/images/04-color-comic-no-person.png" alt="彩色漫画：AI 知识库" width="280"></a> | <a href="examples/images/06-cold-warm-presenter.png"><img src="examples/images/06-cold-warm-presenter.png" alt="冷暖接力：先聊清楚，再动手" width="280"></a> |
| 黄蓝大字、放射动线、人物展示设备 | 粗轮廓、彩色对象、前后变化 | 蓝橙光域、人物递出文档、两工具接力 |

### 竖版 · 3:4

| 蓝黑科技 · 无人物 | 白橙清单 · 原创人物 | 极简编辑 · 无人物 |
| --- | --- | --- |
| <a href="examples/images/02-blue-tech-no-person.png"><img src="examples/images/02-blue-tech-no-person.png" alt="蓝黑科技：先聊清楚，再开发" width="280"></a> | <a href="examples/images/03-white-orange-presenter.png"><img src="examples/images/03-white-orange-presenter.png" alt="白橙清单：资料整理不再乱" width="280"></a> | <a href="examples/images/05-minimal-no-person.png"><img src="examples/images/05-minimal-no-person.png" alt="极简编辑：把需求写清楚" width="280"></a> |
| 深蓝设备、发光工作流、白青标题 | 白橙图标、清楚任务层级、人物引导 | 奶油白与深绿、留白、纸张质感 |

[查看案例详情、输入内容和实际提示词](examples/README.md)。这些是本次实际输出；模型版本与每次生成结果可能不同。

## 能做什么

- **三种输入任选一种**：完整脚本、视频内容简介，或直接描述想要的封面画面；也可以组合。
- **参考图与风格延展**：5 种基础风格、15 个基础分支、31 个参考档案；配色可按内容自由变化。
- **先确认画幅与人物**：只补问尚未明确的选择，不要求本人出镜。
- **GPT Image 优先**：不可用时使用平台自带生图工具；也支持用户自行配置并明确选用 OpenAI 图片 API。
- **输出与检查**：实际图片、PNG/JPEG 导出、缩略图、列表预览，以及中文文字核对与设计依据。

Skill 的完整入口在 [cover-craft/SKILL.md](cover-craft/SKILL.md)，使用条件和工具能力以宿主提供的实际工具为准。

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
