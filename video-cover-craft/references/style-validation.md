# 十种基础风格的实图验证

Video CoverCraft 2.7.0 完成了 10 种基础风格、30 个分支的调研整合。以下是实际独立生成的 10 张新样图，每种风格验证一个分支；其余 20 个分支仅完成设计规格，尚未逐个生图。

5 张原创人物、5 张无人物；横竖各 5 张。主题为虚构 AI 内容，界面与效果是示意。实际使用 Codex 内置图片工具，具体模型 ID 未公开。生成时确实传入了所列样本的像素；博主原图不随包分发。

已逐张查看全图与 320px 小图，核对主/副标题、人物选择、风格和内容关系。模拟列表页面可供检查，但没有声称完成浏览器内的裁切测试或任何具体平台适配。B01/B04 的大标题较靠边，若平台会裁边，应按平台重新构图。

| 基础风格 / 分支 | 新样图（点击原图） | 借鉴与本期变化 |
| --- | --- | --- |
| B01-B · 黄蓝冲击<br>3:4 · 原创人物 | [![AI 写周报](../assets/style-examples/thumbs/01-b01-ai-weekly.png)](../assets/style-examples/01-b01-ai-weekly.png) | C03-S2<br>吸收黑底黄字、巨大标题与主体轮廓；换成黄蓝办公场景、新人物和周报主物件。 |
| B02-A · 蓝黑科技<br>16:9 · 无人物 | [![AI 自动剪辑](../assets/style-examples/thumbs/02-b02-ai-editing.png)](../assets/style-examples/02-b02-ai-editing.png) | C14-S2<br>吸收彩色时间线与强标题层级，移除人物和宇宙背景，改成有统一透视的剪辑工作台。 |
| B03-A · 白橙清单<br>3:4 · 原创人物 | [![AI 读论文](../assets/style-examples/thumbs/03-b03-ai-paper.png)](../assets/style-examples/03-b03-ai-paper.png) | C19-S1<br>吸收浅底标题卡的层次和完整大字；延展为白橙功能卡，加入原创讲解人物与出处标记。 |
| B04-B · 彩色漫画<br>16:9 · 原创人物 | [![AI 为什么乱答？](../assets/style-examples/thumbs/04-b04-ai-prompt.png)](../assets/style-examples/04-b04-ai-prompt.png) | C10-S2<br>吸收漫画结果画面与粗描边文字；改为原创漫画角色和模糊到清晰的提问关系。 |
| B05-A · 极简编辑<br>3:4 · 无人物 | [![先聊清楚](../assets/style-examples/thumbs/05-b05-ai-handoff.png)](../assets/style-examples/05-b05-ai-handoff.png) | C09-S1<br>吸收白底黑字与编辑式留白；移除两个人物，改成开发说明这个单一主对象。 |
| B06-B · 发布会实测<br>16:9 · 原创人物 | [![AI 编程实测](../assets/style-examples/thumbs/06-b06-ai-coding.png)](../assets/style-examples/06-b06-ai-coding.png) | C12-S1<br>吸收真人与可展示实物的体验证据；把证书换成原型电脑，改成原创亚洲男讲解者与工作室构图。 |
| B07-A · 双阵营对比<br>16:9 · 无人物 | [![ChatGPT vs Claude](../assets/style-examples/thumbs/07-b07-ai-models.png)](../assets/style-examples/07-b07-ai-models.png) | C02-S3<br>吸收绿与陶土两区和同等权重的对象；移除中间人物，加入同题输入卡，使用中立问题。 |
| B08-B · 未来办公<br>3:4 · 原创人物 | [![AI 办公搭档](../assets/style-examples/thumbs/08-b08-ai-office.png)](../assets/style-examples/08-b08-ai-office.png) | C16-S2<br>吸收办公任务围绕主体的结构，改为普通原创人物、统一未来工作台和三块协作模块。 |
| B09-A · 矩阵控制室<br>16:9 · 无人物 | [![多 Agent 调度](../assets/style-examples/thumbs/09-b09-ai-agents.png)](../assets/style-examples/09-b09-ai-agents.png) | R13-05<br>取你提供的拼图第一行最右侧的矩阵结构；改为九格任务墙和无人物控制台，任务逻辑参考 C16-S2 与 C14-S2。 |
| B10-B · 立体概念<br>3:4 · 无人物 | [![AI 知识库](../assets/style-examples/thumbs/10-b10-ai-knowledge.png)](../assets/style-examples/10-b10-ai-knowledge.png) | C01-S1<br>吸收金属立体主物和轮廓光；去掉人物、王冠和模型标志，延展为可看懂内部关系的知识库器物。 |

[逐张文字、主题、来源与实际提示词](../assets/style-examples/manifest.json) · [验图记录](../assets/style-examples/review.json) · [基础风格的全部 30 个分支](style-catalog.md)

在其他 Agent 上使用时，按所需样张查看并传入实际 PNG，可另选用户的新参考或人物照片。样张中的原创人物默认只是风格示意，不自动成为用户账号身份。
