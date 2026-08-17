# TourMind 酒店预订 Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

让任何 AI Agent 在一次对话中获得端到端酒店预订能力：搜索全球酒店资源、比较主流 OTA 与酒店供应商的实时价格、核验库存，并通过 TourMind 完成预订、支付、取消和订单管理。

## 演示

### 1. 搜索实时酒店

<div align="center">
  <a href="docs/assets/demo/search-en.gif">
    <img src="docs/assets/demo/search-en.gif" alt="TourMind 酒店搜索演示" width="720" />
  </a>
</div>

### 2. 对比真实房型

<div align="center">
  <a href="docs/assets/demo/detail-en.gif">
    <img src="docs/assets/demo/detail-en.gif" alt="TourMind 酒店房型详情演示" width="720" />
  </a>
</div>

### 3. 核验最终价格并支付

<div align="center">
  <a href="docs/assets/demo/pay-en.gif">
    <img src="docs/assets/demo/pay-en.gif" alt="TourMind 验价与支付演示" width="720" />
  </a>
</div>

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
| WorkBuddy | 将本仓库安装或导入为用户 Skill |
| OpenAI Codex | 通过 Skills 界面或当前版本支持的本地 Skill 目录安装 |
| Claude Code | 作为个人 Skill 安装到 `~/.claude/skills` |
| 兼容 Agent Skills 的客户端 | 客户端能够加载根目录 `SKILL.md` 并发起 HTTPS `POST` 请求时可用 |
| 支持 MCP 的 AI 客户端 | 使用配套的 [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## 1 分钟安装

1. 前往 [tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) 生成 Skill Token。

2. 在你的 AI 客户端 Skills 界面中，安装或导入这个 GitHub 仓库：

   ```text
   https://github.com/tourmind-com/Tourmind-Booking-Skills.git
   ```

   如果客户端从本地目录加载 Skill，将仓库克隆到它的个人 Skill 目录：

   ```bash
   CLIENT_SKILLS_DIR="<你的客户端 Skill 目录>"
   mkdir -p "$CLIENT_SKILLS_DIR"
   git clone https://github.com/tourmind-com/Tourmind-Booking-Skills.git "$CLIENT_SKILLS_DIR/tourmind-booking"
   ```

   常见的个人 Skill 目录：

   | 客户端 | 目录 |
   |---|---|
   | WorkBuddy | `~/.workbuddy/skills` |
   | OpenAI Codex | 使用 Skills 界面，或使用当前 Codex 版本支持的本地目录 |
   | Claude Code | `~/.claude/skills` |

3. 在安装后的 `tourmind-booking` 目录中新建 `skill_token.txt`，文件内只粘贴原始 Token。在 macOS 或 Linux 上限制文件权限：

   ```bash
   chmod 600 skill_token.txt
   ```

重新加载 Skills 或重启 AI 客户端，然后提出酒店需求。无需在本地运行 MCP 服务，本 Skill 会通过 HTTPS 直接调用 TourMind API。

切勿提交 `skill_token.txt`；该文件已经被 `.gitignore` 排除。

## 示例 Prompt

以下示例将 Agent 自身的联网研究与行程规划能力，和 TourMind 的实时酒店搜索、验价、预订、支付及订单管理流程结合起来。

```text
我和朋友两个人计划于 2027 年 4 月 9 日至 13 日去日本大阪（Osaka）玩 4 晚，从关西国际机场往返。我们想安排 1～2 天在大阪湾或淡路岛附近海钓，不租车。请先结合你自己的联网搜索和行程规划能力，比较适合游客的钓鱼区域、当季情况、合规的包船或船钓选择以及公共交通时间，再给出节奏舒适的逐日行程。然后针对最合适的住宿基地，使用 TourMind 搜索实时酒店库存。平均房价控制在每晚 18,000 日元以内，优先双床房、靠近车站、清晨前往钓鱼集合点交通方便、可免费取消；早餐需要与早出发时间兼容。请展示经过实时验证的最佳 5 家酒店，包含房型图片、入住总价和币种、接口返回的税费、取消政策、早餐、前往钓鱼点的交通方案、各自优缺点，以及可重复打开的结果链接。暂时不要预订。
```

```text
请帮两位成人规划 2027 年 2 月 6 日至 12 日、共 6 晚的意大利多洛米蒂（Dolomites）滑雪旅行。我们从威尼斯马可·波罗机场到达，不自驾，滑雪水平中等。请先从机场接驳、雪道、餐饮和性价比角度比较 Cortina d’Ampezzo、Val Gardena 和 Alta Badia，推荐最适合的住宿基地，并给出可执行的逐日行程。再使用 TourMind 搜索平均每晚不超过 250 欧元的实时可售酒店，优先距离缆车步行或接驳 10 分钟以内、有雪具寄存、早餐、免费取消，最好有桑拿。请展示经过验证的最佳 5 家，包含房型和床型、图片、每晚价与入住总价、取消截止时间、餐食、库存状态、到缆车距离，并标明每家未满足的条件。我选定后，请重新核验该房型的实时价格和库存，汇总准确的最终金额及政策，并等待我明确确认后才能预订或发起支付。
```

```text
使用刚才对比结果中的第 2 家酒店。请展示酒店详情，以及所有适合 2 位成人且当前可预订的房型产品，包括房型图片、床型、餐食、取消政策、是否需要二次确认、每晚价格和入住总价。推荐性价比最高的一个房价，并解释理由；然后重新核验这个准确房价。如果信息有变化，请清楚列出验价前后的差异；如果没有变化，请给出最终预订摘要并询问我是否确认。在我明确回复“确认预订”之前，不要创建订单，也不要发起支付。
```

```text
请使用订单参考号 <AGENT_REF_ID> 查询我的预订，并用容易理解的语言说明当前预订状态和支付状态。如果订单可以取消，请先展示取消截止时间、违约金和预计退款金额，不要立即操作。只有在我明确确认后才取消；取消后再次查询订单并展示最终状态。回复和结果链接中都不要暴露我的 Skill Token。
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
| 企业 / ToB | 直连 HTTP Skill | 每次 API 调用都需要 Skill Token | **[TourMind Booking Skill](https://github.com/tourmind-com/Tourmind-Booking-Skills)** |
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
- 产品页面：[tourmind.com/skills](https://tourmind.com/skills)
- GitHub 支持：[提交 Issue](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues)
- 酒店业务咨询：`hotel@tourmind.com`
- 商务合作：`bp@tourmind.com`

## 开源许可

[MIT](LICENSE) © 2026 TourMind
