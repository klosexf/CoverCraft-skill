# 看图选风格

向不知道风格长什么样的用户展示真实样图，帮助选择视觉方向。这是生图前的浏览功能，不调用图片模型，不要求完整脚本或先回答画幅/人物才能看图。

## 展示时机与选择流程

- 本轮没有指定风格或明确参考时，先按已知主题展示最多三种推荐：**B 编号、名称、一张真实缩略图、一句适用理由**，附全部十种图库入口和「你帮我决定」。与尚缺的画幅/人物选择一起展示，避免分成多轮问卷。
- 用户明确说「先看看」「让我选」「不知道风格是什么」时，先展示图片，等待选择风格或授权自主选择，再生成；缺少主题时可直接展示完整图库，不编造针对本期的推荐。
- 用户已明确指定风格、参考图或授权自主决定时直接沿用，不重复要求选菜单。画幅与人物已经清楚、用户要求直接制作而未要求先选风格时，可展示推荐作为默认并继续制作，不把风格变成第三个必答问题。
- 只要求看风格时，展示完即可，不生图，不索取视频脚本、自拍或画幅。用户只选风格但尚未提供主题时也先接受选择，真正制作时再补足缺少的内容与两项设置。
- 接受 B02、02、编号 2、蓝黑科技等明确指向同一条目的说法；「第二张」按本轮展示顺序解释，不能误认为一定是 B02。记录展示顺序与选中的 B 编号；含糊且影响结果时再补问。
- 不让新用户选择 30 个内部构图分支。先选基础风格，Agent 依据主题选分支；用户想看进阶选项时再读取 [style-catalog.md](style-catalog.md)。

用户可以直接回复：`B02，竖版，无人物。` 或 `风格你决定，横版，有人物，用原创角色。` 风格选择不自动保存为长期偏好，只有明确要求长期沿用时才保存。

## 怎样把图片展示给用户

1. **聊天图片卡片**：读取 [菜单数据](../assets/style-menu.json) 与 [样张索引](../assets/style-examples/manifest.json)，找到真实缩略图。宿主支持本地图片时，解析为当前安装目录的绝对路径后内联展示，并链接原 PNG。不要使用开发者电脑的固定路径；不同 Agent 的安装目录不同。
2. **完整图库**：打开或提供技能根目录的 [style-picker.html](../style-picker.html)。它不用联网，支持按内容类型/关键词浏览，点击卡片生成一条可复制的选择句。它不会自动把选择发送到 Agent；用户将短句粘贴回聊天。
3. **无法显示本地图片时**：若宿主允许展示公开网络图片，使用 `style-menu.json` 中的公开仓库图像基址与真实样张文件名；或提供 [GitHub 图文菜单](https://github.com/klosexf/CoverCraft-skill/blob/main/video-cover-craft/references/style-menu.md)。网络图片也无法展示时提供可打开的图库/PNG 链接与名称描述，说明本轮没有显示图片，不声称用户已经看过预览。

本页下方图片使用包内的相对链接，能在 GitHub 和支持相对资源的 Markdown 阅读器显示；Agent 发给聊天时要按宿主转换。GitHub 不会把 HTML 文件页直接运行成网站，在线浏览优先用 Markdown 图文菜单；下载完整技能后才能打开离线 HTML。

每种基础风格目前只有一张本版主样图。**十种都支持横/竖版、有人物/无人物，样图的设置不是风格限制。** 不按用户要求的画幅或人物去隐藏其余风格，也不为了看菜单重新生成十张图片。明确采用某图为生图参考时，再查看并实际传入 PNG，不能只给文字档案。

## 按主题推荐的起点

| 用户的视频内容 | 可展示的三种方向 | 如何说明区别 |
| --- | --- | --- |
| AI 编程、自动化、软件操作 | B02、B06、B05 | 工作流 / 实物体验 / 简洁方法 |
| AI 办公、文档、论文 | B03、B08、B01 | 功能卡 / 协作空间 / 大字冲击 |
| 两模型或两种方法比较 | B07、B04、B05 | 同题两区 / 比喻 / 观点 |
| Agent 协作、分工、批任务 | B09、B08、B02 | 格阵调度 / 少量模块 / 接力流程 |
| AI 原理、知识库、Token | B10、B04、B05 | 器物剖面 / 漫画比喻 / 极简观点 |
| 新功能、产品资讯 | B06、B01、B10 | 体验展示 / 强标题 / 立体主物 |

这只是推荐起点。用户要求或参考优先；根据具体主题说明理由，不把一个内容类别锁成一种风格，不把推荐说成点击率排名。配色可以变化。

## 全部十种风格

| 编号 / 名称 | 真实样图（点击看原图） | 长什么样 / 适合什么 |
| --- | --- | --- |
| **B01 黄蓝冲击** | [![黄蓝冲击](../assets/style-examples/thumbs/01-b01-ai-weekly.png)](../assets/style-examples/01-b01-ai-weekly.png) | 大字、强色块，突出一个工具或成果<br>适合：AI 工具亮相、AI 办公挑战 |
| **B02 蓝黑科技** | [![蓝黑科技](../assets/style-examples/thumbs/02-b02-ai-editing.png)](../assets/style-examples/02-b02-ai-editing.png) | 深色设备、重点光线，把操作关系画清楚<br>适合：AI 编程、自动剪辑、自动化教程 |
| **B03 白橙清单** | [![白橙清单](../assets/style-examples/thumbs/03-b03-ai-paper.png)](../assets/style-examples/03-b03-ai-paper.png) | 浅色背景、功能卡片，清楚又容易读<br>适合：Skill 功能列表、AI 读论文、步骤说明 |
| **B04 彩色漫画** | [![彩色漫画](../assets/style-examples/thumbs/04-b04-ai-prompt.png)](../assets/style-examples/04-b04-ai-prompt.png) | 粗轮廓、漫画比喻，直观解释问题与解法<br>适合：提示词技巧、AI 使用误区、模型概念 |
| **B05 极简编辑** | [![极简编辑](../assets/style-examples/thumbs/05-b05-ai-handoff.png)](../assets/style-examples/05-b05-ai-handoff.png) | 大留白、少量对象，让一句观点成为主角<br>适合：AI 使用心得、开发方法、研究观点 |
| **B06 发布会实测** | [![发布会实测](../assets/style-examples/thumbs/06-b06-ai-coding.png)](../assets/style-examples/06-b06-ai-coding.png) | 摄影工作室、具体展示对象，强调体验感<br>适合：AI 产品体验、AI 编程实测、新功能解读 |
| **B07 双阵营对比** | [![双阵营对比](../assets/style-examples/thumbs/07-b07-ai-models.png)](../assets/style-examples/07-b07-ai-models.png) | 两方同样清楚，用共同任务比较做法<br>适合：两模型对比、两工具比较、前后方法 |
| **B08 未来办公** | [![未来办公](../assets/style-examples/thumbs/08-b08-ai-office.png)](../assets/style-examples/08-b08-ai-office.png) | 统一办公空间、少量任务模块，展示协作<br>适合：AI 办公、文档与 PPT、多工具接力 |
| **B09 矩阵控制室** | [![矩阵控制室](../assets/style-examples/thumbs/09-b09-ai-agents.png)](../assets/style-examples/09-b09-ai-agents.png) | 重复任务格阵、一个焦点，突出调度关系<br>适合：多 Agent 调度、批处理、任务排错 |
| **B10 立体概念** | [![立体概念](../assets/style-examples/thumbs/10-b10-ai-knowledge.png)](../assets/style-examples/10-b10-ai-knowledge.png) | 大立体器物或剖面，让抽象关系看得见<br>适合：AI 知识库、检索原理、Token 概念 |

这些都是实际生成的图片，界面和主题为示意；样图中人物为原创角色。每种三个延展分支，共 30 个；其中 10 个有本版实图，另 20 个仅完成规则。详细来源与检查见 [style-validation.md](style-validation.md)。

## 为本期生成带推荐标记的菜单

需要独立预览页且宿主能运行本地脚本时，可使用 `scripts/preview_styles.py`；图片路径自动从技能安装位置解析。示例命令在技能根目录执行：

```bash
python3 scripts/preview_styles.py --out /absolute/path/to/new-style-menu.html --recommend B02 B06 B05
```

脚本仅组织已有图片，没有生图开销，最多标记三个推荐，不替代 Agent 理解脚本。输出已存在时不会覆盖，换一个新路径。离线页面引用当前技能资源，单独复制 HTML 而不保留图片路径会失效；分享时可使用随包图库、完整技能或公共图文菜单。
