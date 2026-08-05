# TourMind 酒店预订 Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

让任何 AI Agent 在一次对话中获得端到端酒店预订能力：搜索全球酒店资源、比较主流 OTA 与酒店供应商的实时价格、核验库存，并通过 TourMind 完成预订、支付、取消和订单管理。

## 示例截图

> **待补充：** 增加一张真实的端到端截图或短 GIF，展示酒店搜索、实时房价、最终库存验价和预订流程。

## 核心能力

- 解析城市、酒店、地标、车站、地址、滑雪场等 POI，不凭空编造坐标。
- 搜索最多 20 家候选酒店，查询匹配的实时房型，并选出经过验证的最佳 5 家。
- 比较主流 OTA 和酒店供应商的实时每晚价格、总价、取消政策及库存状态。
- 同时返回酒店与房型图片、设施、床型、餐食、费用和基于证据的推荐理由。
- 下单前重新核验所选房型的价格和库存。
- 创建预订、查询与取消订单，并发起 Stripe、微信支付或支付宝付款。
- 提供有时效、可重复访问的只读结果链接，同时不暴露 Skill Token。

## 支持的 AI 客户端

| 客户端 | 支持方式 |
|---|---|
| OpenAI Codex | 作为本地 Skill 安装到 `~/.codex/skills` |
| 兼容 Agent Skills 的客户端 | 客户端能够加载根目录 `SKILL.md` 并发起 HTTPS `POST` 请求时可用 |
| 支持 MCP 的 AI 客户端 | 使用配套的 [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## 1 分钟安装

1. 将 Skill 克隆到 Codex：

   ```bash
   mkdir -p ~/.codex/skills
   git clone https://github.com/tourmind-com/Tourmind-Booking-Skill.git ~/.codex/skills/tourmind-booking
   ```

2. 前往 [tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) 生成 Skill Token，将原始 Token 保存为 `~/.codex/skills/tourmind-booking/skill_token.txt`，然后限制文件权限：

   ```bash
   chmod 600 ~/.codex/skills/tourmind-booking/skill_token.txt
   ```

3. 重启 AI 客户端并提出酒店需求。无需在本地运行 MCP 服务，本 Skill 会通过 HTTPS 直接调用 TourMind API。

切勿提交 `skill_token.txt`；该文件已经被 `.gitignore` 排除。

## 示例 Prompt

```text
帮我搜索深圳西丽地铁站附近、9月12日至9月14日入住、2位成人、3公里以内的酒店。
```

```text
给我展示最合适的5家酒店，包含经过验证的实时房价、早餐、取消政策和入住总价。
```

```text
把酒店搜索接口返回的全部候选都列出来，不符合硬性条件的酒店请明确标注原因。
```

```text
重新核验我选中的房型；确认最终价格和取消政策后，再协助我预订和支付。
```

## 工作流程

```text
地点或 POI
  → search_location
  → search_hotels（最多 20 家候选）
  → query_room_rates（查询符合条件候选的实时房型）
  → 排序并展示经过验证的最佳 5 家酒店
  → get_hotel_detail + 房型图片与报价
  → check_room_availability（核验所选房价）
  → 用户明确确认后 create_booking
  → 按需调用 pay_order / query_booking / cancel_booking
```

`search_hotels.min_price` 只是缓存的候选信号。展示给用户的价格必须来自 `query_room_rates`，最终下单必须使用 `check_room_availability` 返回的最新价格和房价代码。

## Token 与安全说明

- 所有 ToB Skill API 调用都需要保存在本地 `skill_token.txt` 中的 Skill Token。
- 不要在 Prompt、日志、截图、URL、Git 提交或 Issue 中暴露 Token。
- 使用 `chmod 600` 将 Token 文件权限限制为仅当前用户可读写。
- 收到 HTTP 401 或 `unauthorized` 响应时，删除失效的本地 Token 并重新生成。
- 返回的 `web_url` 会话是只读的，在过期前可重复打开；页面不能验价、预订、支付、取消，也不能访问账户或财务功能。
- 预订、取消和支付必须在已认证的 AI 对话中获得用户明确确认。

## Skill / MCP / ToB / ToC 选择矩阵

| 用户类型 | 接入方式 | 鉴权模式 | 仓库 |
|---|---|---|---|
| 消费者 / ToC | 直连 HTTP Skill | 搜索与验价公开；订单操作才需要 `user_key` | [Hotel Booking AI](https://github.com/tourmind-com/Hotel-Booking-AI) |
| 企业 / ToB | 直连 HTTP Skill | 每次 API 调用都需要 Skill Token | **[TourMind Booking Skill](https://github.com/tourmind-com/Tourmind-Booking-Skill)** |
| 消费者 / ToC | MCP + 配套 Skill | MCP 连接公开；订单操作才需要 `user_key` | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| 企业 / ToB | MCP + 配套 Skill | MCP 连接使用 Bearer 鉴权 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API 与支持入口

**API 基础地址：** `https://api.tourmind.com`

| 接口 | 用途 |
|---|---|
| `POST /skill/tob/check_skill_update` | 检查 Skill 更新 |
| `POST /skill/tob/search_location` | 解析地区、POI 或酒店 |
| `POST /skill/tob/search_hotels` | 搜索候选酒店 |
| `POST /skill/tob/get_hotel_detail` | 获取酒店详情和图片 |
| `POST /skill/tob/query_room_rates` | 获取实时房型和价格 |
| `POST /skill/tob/check_room_availability` | 重新核验所选房价和库存 |
| `POST /skill/tob/create_booking` | 创建已确认的预订 |
| `POST /skill/tob/query_booking` | 查询订单 |
| `POST /skill/tob/cancel_booking` | 确认后取消订单 |
| `POST /skill/tob/pay_order` | 确认后发起支付 |

- 请求字段与响应契约：[references/parameter_guide.md](references/parameter_guide.md)
- 获取 Skill Token：[tourmind.com/user/skill-token](https://tourmind.com/user/skill-token)
- 产品页面：[tourmind.com/skill](https://tourmind.com/skill)
- GitHub 支持：[提交 Issue](https://github.com/tourmind-com/Tourmind-Booking-Skill/issues)
- 酒店业务咨询：`hotel@tourmind.com`
- 商务合作：`bp@tourmind.com`

## 开源许可

[MIT](LICENSE) © 2026 TourMind
