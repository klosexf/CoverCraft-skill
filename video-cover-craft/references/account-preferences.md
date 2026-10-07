# 账号偏好与系列模板

用于跨次制作保持用户明确认可的设计规则。偏好保存在本技能目录中的 `user-preferences.json`，与参考库分开；安装更新时保留已有的该文件。使用 JSON，普通文件工具即可读取和按字段修改，不需要额外服务。

仓库提供通用模板 [user-preferences.example.json](../user-preferences.example.json)，不附带个人偏好记录。首次获准保存长期要求时，可用模板创建 `user-preferences.json` 再写入授权字段。实际偏好文件已加入忽略规则，不作为发布文件。

## 读取与优先级

1. 当前用户的明确要求。
2. 用户明确指定系列的配置（`series` 中的对应条目）。
3. 账号默认配置（`defaults` 与 `design`）。
4. 参考图、基础风格与按内容自主决定的设计。

只有用户明确指定某系列或授权自动匹配时才套用系列配置。不因主题包含“AI”就擅自认定属于某系列。用户要求参考特征与已存偏好冲突时，当次指定优先；不静默改写长期文件。

偏好中的空列表、`null` 表示未设置，不推测用户立场。文件缺失就按当前要求制作；不可解析时说明未加载偏好，使用当前要求继续独立工作，不覆盖损坏文件。用户明确提供另一个偏好文件时，以该文件作为本轮来源，摘要记录实际路径。

## 什么可以保存

保存明确具有持续范围的表达，例如：

- “以后这个系列标题都用这种大字，但颜色你决定。”
- “记住，我不喜欢背景里堆小字。”
- “这个账号默认竖版无人物，下次不用问。”

“这张我选 A”“本期竖版无人物”“把标题改成省额度小技巧”只适用于当前任务。不自动将它们写成全局喜好。

用户明确说“记住”“以后沿用”或直接要求设置偏好时即可保存，无需再确认同一授权。当次偏好可记录在设计摘要中；不要每次制作都要求用户填写偏好问卷。反馈可由用户查看、修改或删除。

## 字段

| 字段 | 用途 |
| --- | --- |
| `schema_version` | 当前为 1 |
| `profile_name` | 用户指定的账号/配置名称；未指定使用“默认账号” |
| `defaults.aspect` | 明确授权长期沿用的画幅，否则 `null` |
| `defaults.people` | 明确授权长期沿用的 `none` / `photo` / `virtual`，否则 `null` |
| `defaults.use_without_asking` | 是否明确允许以上非空默认值视为已回答；未授权为 `false` |
| `design.palette_policy` | 自由延展、指定配色或其他明确规则 |
| `design.locked_colors` | 用户要求锁定的品牌色；空列表表示未锁定 |
| `design.preferred_styles` | 长期喜欢的基础/参考编号或名称，可多项 |
| `design.typography` / `composition` / `texture` | 长期字形、构图或质感规则 |
| `design.avoid` | 明确不喜欢的视觉元素 |
| `series` | 系列名到局部 `defaults` / `design` 配置的映射；只覆盖该系列提供的字段 |
| `generation.backend` | 可选，缺省或 `auto` 为 GPT Image 优先、平台原生回退；用户持续选择 API 时设置 `openai-api` |
| `generation.openai_model` / `openai_size` / `openai_quality` | 可选的 API 请求配置，非空时映射为客户端参数；Key 单独保存在本地环境或平台密钥设置 |
| `evidence` | 保存日期、字段路径、用户原话与来源，供回溯和纠正 |

画幅与人物的长期默认不自动跳过问题：需有非空有效值且 `use_without_asking: true`，并有用户明确持续授权。只配置画幅时，人物仍需询问；当前明确的横版或有人物要求覆盖默认值。照片默认不代表任何照片都能用，没有指定身份素材时仍需取得对应照片。

## 当前配置

通用模板允许自主选择配色，画幅与人物为未设置，授权依据为空；未配置 `generation` 时采用默认生图顺序。模板不表示用户已认可某个长期选择。未来可在持续授权后补充账号风格、系列模板或 API 选择，方法见 [openai-api-setup.md](openai-api-setup.md)。

修改现有 JSON 时保留无关字段和已设系列；记录本次字段与依据，不累计整份聊天记录。用户要求删除一项时一并移除对应依据；更新 Skill 时保留账号文件，源码更新不应重置个人设置。

长期配置借鉴 [baoyu-cover-image 的偏好结构](https://github.com/JimLiu/baoyu-skills/blob/main/skills/baoyu-cover-image/references/config/preferences-schema.md)；当前文件与授权规则是本技能的实现。
