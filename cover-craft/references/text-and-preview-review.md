# 中文文字与列表预览验收

生图前确定文字清单，生图后检查真实像素。文字核对和列表检查分别记录，生成辅助文件并不等于验收通过。

## 文字清单

每套方案保存一个 `text-spec.json`；多方案可以各存一个文件或用 `variants` 分组。只记录本轮要画出的文字，视频标题作为预览的元数据单独存。可按以下形状填写：

```json
{
  "schema_version": 1,
  "video_title": "Codex 省额度小技巧：先在 ChatGPT 聊清楚方案",
  "cover_headline": {
    "text": "Codex额度用太快？",
    "display_lines": ["Codex额度", "用太快？"],
    "source": "根据脚本拟写",
    "required": true
  },
  "cover_subtitle": {
    "text": "省额度小技巧",
    "display_lines": ["省额度小技巧"],
    "source": "用户明确指定",
    "required": true
  },
  "other_text": [
    {"text": "ChatGPT", "role": "品牌", "required": true},
    {"text": "先讨论", "role": "流程", "required": true},
    {"text": "开发说明", "role": "文档", "required": true, "allow_repeat": true},
    {"text": "Codex", "role": "品牌", "required": true},
    {"text": "再开发", "role": "流程", "required": true}
  ],
  "background_text": "none",
  "allowed_numbers": [],
  "allow_extra_text": false
}
```

例子中的文案是当前脚本的示例，不自动用于别的视频。标题断行只改变布局；用户要求逐字采用时保持字词、标点与有意义的空格。确认用户给的是封面标题之前，不擅自缩写。

文字来源也可记为“根据视频描述拟写”“根据封面描述拟写”或“用户明确指定”，与实际输入一致。纯画面请求无视频标题时 `video_title` 可为 `null`，预览助手不传 `--video-title`。用户要求无字时，主/副标题置为 `null`、`other_text` 为空数组，禁止额外文字与数字；验收检查全图是否无意出现文字，不以没有标题判失败。无标题封面的缩略图重点检查主体和构图是否清楚。

软件素材有两种处理：

- 示意界面用无字线条、色块和图标，避免模型捏造可读的小标签。
- 必须保留准确界面时，指定真实素材与需要保留的区域；把关键可读文字从已查看的素材中加入清单。不能要求逐字准确而又只传模糊缩略截图。

品牌名、流程标签也属于文字，不能只核对大标题。允许某词出现在文档和笔记本两处时明确允许重复；不要把合理重复误判为错误。装饰书本、墙面和键盘旁的便签无需文字时要求无字，不复制参考里的账号、水印和界面数字。

## 提示词加入的约束

```text
封面文字逐字采用清单，只使用指定断行。
视频标题是理解内容的元数据，不额外写到画面上。
品牌与流程标签按清单出现；开发说明可以在文档和笔记本各出现一次。
书脊、墙面和其他装饰道具无字；示意界面用无字线条。
不增加收入、百分比、倍数、年份或步骤数；必要数字从允许清单取。
```

按本轮规格调整约束，不强制所有封面都没有数字或背景文字。

## 生图后的中文专项检查

1. 看完整图，逐项核对主标题、副标题、关键标签、品牌拼写与允许数字；必要时用只读查看工具放大文字区域。
2. 检查视觉相近字、漏字、重复字、标点、意外口号和有意义的断行；“先聊清楚”不能因语境合理就接受为“先练清楚”。
3. 扫描背景可辨认的小字、书脊、设备侧栏、水印和参考遗留内容。没有必要的杂字应删除；关键文字不清楚时标为 `uncertain`，不能视为正确。
4. 看约 320 像素宽的版本，检查文字层级。辅助标签可以更弱，但重要步骤或结论不能只有在原图中才读得到。
5. 有只读 OCR 能力时可辅助核对，不依赖不存在的 OCR 工具。OCR 误识别与真实图像错误分别记录，视觉核对仍为依据。

修正时将当前成图传给所选生图工具的编辑或参考输入，只修改问题文字或区域并复核全图。工具不能接收修改目标时说明限制，不声称已经定点修字。默认最多两轮；导出脚本和预览脚本都不修字，不覆盖原图。

## 浏览列表预览

运行助手，例如：

```bash
python3 /absolute/cover-craft/scripts/preview_feed.py --image /absolute/cover-a.png --label "A · 冷暖接力" --image /absolute/cover-b.png --label "B · 清爽清单" --video-title "Codex 省额度小技巧：先在 ChatGPT 聊清楚方案" --out-dir /absolute/outputs/cover-final/feed
```

输出 `feed-preview.html`、`preview-manifest.json` 和未改动的图片副本。打开 HTML 后可以切换：

- 浅色/深色列表背景。
- 320、168、120 像素宽度，后两种是更严格的小图检查，并非所有平台的实际展示尺寸。
- 模拟时长、点赞位置及遮挡区域。
- 轻微边缘裁切与周边示例卡片，用于检查边缘安全和视线干扰。

模拟卡片明确标注为示例，不冒充真实对标封面；模拟界面的位置和比例不是平台规范。用户指定某个平台时，使用已查证规则或其实际截图制定更精确的约束，不臆测最新界面。布局预览以原图比例显示，边缘裁切只影响页面显示，不裁切交付文件。

## 记录检查结果

在 `review.json` 中按方案记录：

```json
{
  "schema_version": 1,
  "variants": [
    {
      "id": "A",
      "checks": {
        "text": {"status": "pass", "evidence": "完整图与文字清单逐项核对"},
        "content": {"status": "pass", "evidence": "开发说明连接讨论与开发，与脚本一致"},
        "people": {"status": "pass", "evidence": "无人物"},
        "aspect": {"status": "pass", "evidence": "1080×1440，为3:4"},
        "thumbnail": {"status": "pass", "evidence": "320px下主副标题清楚"},
        "feed": {"status": "not_checked", "evidence": "页面已生成，尚未打开检查"}
      },
      "repairs": []
    }
  ]
}
```

状态：`pass`、`needs_fix`、`uncertain`、`not_checked`。只有实际检查后才能填 `pass`；未核验项目和限制在交付中说明。默认验收重点为 320px 与完整图；120px 下次要文字读不清可记录为取舍，不自动触发无限生图。

列表与遮挡检查参考 [NanoThumbnail](https://github.com/yoanbernabeu/NanoThumbnail/blob/main/skills/nanothumbnail/SKILL.md)，独立整理图片用文字借鉴 [Auto-Redbook-Skills](https://github.com/comeonzhj/Auto-Redbook-Skills/blob/main/SKILL.md)；文字清单和报告结构为本技能的实现。
