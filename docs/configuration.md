# 配置说明

## 插件元数据

- `plugin.json`：OlivaDice 插件入口配置，包含插件 ID、名称、版本、作者、入口文件和描述。
- `app.json`：OlivOS 应用配置，包含命名空间、菜单入口、兼容版本、优先级、支持平台和插件说明。
- `ai-plugin.json`：第三方/OpenAI 插件清单，声明插件名称、描述、鉴权方式和 OpenAPI 地址。
- `openapi.yaml`：第三方集成用的 OpenAPI 规范示例。

## 运行时配置路径

插件运行后会在 OlivOS 的 `plugin/data/ChefChatAI` 目录下保存运行时数据：

- `config.json`：主配置文件，保存 API、人设、聊天功能、资料库、情绪图片等设置。
- `history.json`：上下文历史记录。
- `knowledge_files/sources`：导入资料库的原始文件。
- `knowledge_files/texts`：资料库解析后的文本缓存。
- `knowledge_files/index.json`：资料库索引。
- `emotion_images`：情绪图片目录。
- `sticker_library`：表情包库。

这些运行时目录已加入 `.gitignore`，避免把 API Key、聊天记录和私有资料提交到仓库。

## API 配置

设置页中可以选择以下接口预设，也可以使用自定义 OpenAI 兼容接口：

- DeepSeek：`https://api.deepseek.com`
- OpenAI：`https://api.openai.com/v1`
- DashScope 通义千问：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 智谱 GLM：`https://open.bigmodel.cn/api/paas/v4`
- Kimi / Moonshot：`https://api.moonshot.cn/v1`
- OpenRouter：`https://openrouter.ai/api/v1`
- SiliconFlow：`https://api.siliconflow.cn/v1`
- 本地 / OneAPI：`http://127.0.0.1:3000/v1`

需要配置的核心参数包括：

- `base_url`：接口地址，不需要手动补 `/chat/completions`，插件会自动拼接。
- `api_key`：服务商密钥。不要提交到 GitHub。
- `model`：模型名称。
- `temperature`：回复随机性。
- `max_tokens`：最大输出长度。
- `timeout_seconds`：请求超时时间。
- `extra_headers`：额外请求头，适用于 OpenRouter 等服务。
- `extra_body`：额外请求体字段，适用于兼容接口的特殊参数。

## 聊天触发

默认群聊触发方式：

- `厨师 你的问题`
- `.chef 你的问题`
- `.ai 你的问题`
- @ 机器人后提问

私聊默认也使用触发词，可在设置页开启“私聊任意消息自动回复”。

## 安全与隐私

- API Key 默认只保存在本地运行时配置中，不应提交到仓库。
- 导出 API 配置时，建议导出不含密钥的模板。
- 网页检索安全模式默认开启，会拦截本机地址、内网地址和非常见端口。
- 资料库、历史记录、表情包、情绪图片等个人数据默认不提交到 GitHub。
