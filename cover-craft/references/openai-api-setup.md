# 用户自行配置 OpenAI 图片 API

这是可选路径。默认仍是 GPT Image 工具优先，缺少时使用平台原生生图工具。用户明确选择 API 或保存了持续 API 使用偏好时，这个选择优先；仅检测到 Key 不自动调用 API。

## 配置

1. 在支持本地脚本的宿主中使用其可用的 Python 环境，按需安装本包的 `requirements-openai.txt`，或使用宿主已经维护的 OpenAI 图片客户端。默认生图不依赖这些可选 API 依赖。
2. 在本地环境或平台的密钥配置中设置 `OPENAI_API_KEY`；不要求将 Key 粘贴到聊天，也不写入偏好文件、提示词、日志或安装包。
3. 使用 `OPENAI_IMAGE_MODEL` 或助手的 `--model` 指定你有访问权限的 GPT Image 型号。包内不硬编码“最新”型号；选择依据当前 [OpenAI 图片指南](https://developers.openai.com/api/docs/guides/image-generation)。
4. 可选设置 `OPENAI_IMAGE_SIZE`、`OPENAI_IMAGE_QUALITY`，或传 `--size`、`--quality`。这些值必须符合所选模型的实时限制；助手只做基本格式检查，服务仍可能拒绝不支持的组合。
5. 制作时明确说“本期使用我配置的 OpenAI 图片 API”。若要求长期使用，可将 `generation.backend` 设置为 `openai-api`；改回 `auto` 即恢复默认顺序。

例如偏好文件可以增加以下字段；这里只是格式示例，`null` 表示通过环境或本次参数另行指定模型：

```json
{
  "generation": {
    "backend": "openai-api",
    "openai_model": null,
    "openai_size": null,
    "openai_quality": null
  }
}
```

合并这些字段时保留个人设计与系列设置。Agent 将非空配置映射到助手参数；本次参数优先。缺少 `generation` 或 `backend` 时默认为 `auto`。选择 API 后配置不完整，说明缺少哪个字段，不自动切换到其他模型。

## 在 Codex 中执行

有宿主维护的 `imagegen` Skill 与 CLI 时，读取其 API/CLI 文档，使用它提供的 `generate` 或接收图片的 `edit` 路径，不修改宿主脚本。API 选择不等于允许降级用户指定模型。具体参数与支持尺寸以当前宿主文档和官方 API 为准。

## 在其他支持本地脚本的宿主中执行

可使用 [scripts/openai_image.py](../scripts/openai_image.py)。这是基于官方 Python SDK 的可选助手，按显式配置的型号生成一张独立图片；不绑定 Agent 的聊天模型，不执行自动换型号或自动重试。

先准备本轮提示词，再作不联网的检查：

```bash
python3 /absolute/cover-craft/scripts/openai_image.py --prompt-file /absolute/prompt.txt --out-dir /absolute/outputs/cover-api-a --dry-run
```

已设置 `OPENAI_IMAGE_MODEL` 时可省略 `--model`；否则明确传入当前可用型号。检查仅确认本地文件与参数格式，不验证真实账号权限、余额或 API 可达性，也不创建图片。

无参考图片时去掉 `--dry-run`，执行 `images.generate`。有参考或修改目标时按提示词编号传入图片，助手使用 `images.edit`：

```bash
python3 /absolute/cover-craft/scripts/openai_image.py --prompt-file /absolute/prompt.txt --image /absolute/style.png --image /absolute/software.png --out-dir /absolute/outputs/cover-api-a
```

参考用于创作新封面时，在提示词中明确它们是风格/产品参考；修改现有封面时，把当前成图列为第一修改目标。所有输入先实际查看，不能只引用档案文字。助手将图片真实作为文件输入传入模型，保留编号顺序。

输出新目录中的 `cover.png`、`prompt.txt`、`generation.json`。已有目录会拒绝覆盖；每个构思与画幅分别执行。`requested_model` 记录请求型号，`model_id` 仅记录服务确实返回的型号；未返回时为 `null`。

接口依据：[官方 Python 生成接口](https://developers.openai.com/api/reference/python/resources/images/methods/generate)、[官方 Python 编辑接口](https://developers.openai.com/api/reference/python/resources/images/methods/edit)，于 2026-10-06 核对。生成/编辑返回的 base64 图片被解码并保存，图片仍须进行中文、内容、人物和画幅验收。

该助手不读取 Key 文件、不扫描其他应用配置，不会自动充值。没有本地脚本能力的宿主可以使用其真实可用的 OpenAI 图片集成；集成也没有时，说明缺少执行能力，不能仅凭安装 Skill 宣称 API 已接通。
