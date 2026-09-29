# media-badges

自托管的媒体文件名徽标（badge）规则库，合并自两套公开配置并做了清洗与修正。

## 来源

- **StreamBridge Studio Markers**（streambridge-studio-markers.vercel.app）— 中文 PT 圈重度规则，强项是 152 条中文流媒体来源识别（爱优腾芒 B 站等）
- **Xperience Badge Studio**（xperience-app.com）— 英文 release 圈精选，强项是 SEADEX / HYBRID 等发布组标签与独立 IMAX 组，配 kingsize 高清 WebP 图标

## 本库做了什么

- 图标全部自托管（371 个，PNG/WebP 原样保留），不再依赖第三方 Vercel / CDN
- 剥除 StreamBridge 正则中嵌入的零宽隐写 ID（U+200B/200C/2064 等，136 条）
- 移除 17 条禁用（isEnabled=false）的废弃规则
- 修正 Xperience 的 60FPS 正则：原 `60(FPS|fps)` 漏匹配 `60 fps`、`59.94fps`、`60.0Hz`，且会误报 `160FPS`；现改为带边界锚定的 `(?i)(?<![0-9])(?:59\.94|60(?:\.0+)?)[ ._-]*(?:fps|hz)(?![A-Za-z0-9])`
- 全部 355 条正则通过编译校验

## 文件

| 文件 | 内容 |
|---|---|
| `badges.json` | 合并版，25 组 / 355 条，ID 加 `sb-` / `xp-` 前缀避免冲突 |
| `streambridge-badges.json` | StreamBridge 单独清洗版（15 组 / 254 条） |
| `xperience-badges.json` | Xperience 单独清洗版（10 组 / 101 条） |
| `icons/` | 自托管图标，`sb-*` 为 StreamBridge 来源，`xp-*` 为 Xperience 来源 |

## 引用地址

合并版：

```
https://raw.githubusercontent.com/joshcheng820222/media-badges/refs/heads/master/badges.json
```

## 结构说明

每条 filter 含 `name`（显示名）、`pattern`（匹配文件名的正则）、`imageURL`（图标）、颜色与 `groupId`（分组）。组与 filter 的 schema 与上游保持一致，可直接导入兼容该格式的 Badge Studio / Nuvio 生态工具。
