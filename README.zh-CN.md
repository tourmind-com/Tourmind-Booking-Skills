<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">TourMind Booking Skills</a></b><br />
  <strong>让你的 Agent 搜索和预订全球酒店与机票</strong>
</h1>

<a href="https://tourmind.com/skills">
  <img alt="TourMind Booking Skills" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  把你的客户带入智能旅行
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">产品页面</a> |
  <a href="https://auth.journione.ai">获取 Token</a> |
  <a href="https://tourmind.com">公司官网</a>
</div>

<br />

[![ClawHub installs](https://img.shields.io/badge/ClawHub_installs-2.1k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Release](https://img.shields.io/github/v/release/tourmind-com/Tourmind-Booking-Skills?label=release)](https://github.com/tourmind-com/Tourmind-Booking-Skills/releases/latest)
[![License](https://img.shields.io/github/license/tourmind-com/Tourmind-Booking-Skills)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

让你的 AI Agent 同时具备端到端的酒店预订能力和覆盖全球的机票搜索与预订能力。无需离开常用的 Agent 客户端，即可搜索全球酒店与航班资源，对比主流 OTA 和供应商的实时价格，核验库存与最终价格，并通过 TourMind Booking Skills 完成预订与支付、查询订单。

## 酒店 Skill 示例展示

以下 GIF 展示酒店 Skill 的使用体验。

### 1. 搜索实时酒店

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="TourMind 酒店搜索演示" width="720" />
  </a>
</div>

### 2. 对比真实房型

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="TourMind 酒店房型对比演示" width="720" />
  </a>
</div>

### 3. 核验最终价格并支付

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="TourMind 酒店验价与支付演示" width="720" />
  </a>
</div>

## 核心能力

- **酒店：** 搜索全球酒店和实时房型，对比价格，查看图片、设施、餐食与取消政策，重新核验库存，并完成预订、支付和取消。
- **机票：** 查询机场及单程、往返或多城市航班，对比时间、舱等、中转、行李和总价，重新核验选中的票价，并继续下单、查询订单和支付。
- **完整行程规划：** 让 Agent 根据日期、预算和偏好规划行程，同时搜索适合的机票与酒店组合。
- **更安心的交易流程：** 搜索不会自动创建订单。创建酒店或机票预订、取消符合条件的酒店订单或发起支付前，Agent 会展示重要信息并等待你明确确认。
- **自然语言交流：** 直接用你习惯的语言描述需求，不必自己填写复杂的搜索表单。

## 支持的 Agent 客户端

TourMind Booking Skills 支持 ChatGPT（Work / Codex 模式）、Claude Code、WorkBuddy、QClaw、Marvis、OpenClaw、Kimi Work、豆包工作模式、千问工作模式、Hermes、Cursor，以及其他支持 Skill 的 Agent 客户端。

## 选择合适的 TourMind 接入方式

本 Skill 仓库已经整合酒店和机票的个人用户（ToC）与企业用户（ToB）能力。MCP 的组织方式不同，请根据使用场景选择合适的接入方式。

| 接入方式 | 适用用户 | 能力 | 仓库 |
|---|---|---|---|
| TourMind Booking Skills | ToC 与 ToB | 酒店与机票 Skill | **[本仓库](https://github.com/tourmind-com/Tourmind-Booking-Skills)** |
| 酒店 MCP — 个人用户（ToC） | ToC | 面向个人用户的酒店搜索与预订 | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| 酒店 MCP — 企业用户（ToB） | ToB | 面向企业用户的酒店搜索与预订 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |
| 机票 MCP — 个人与企业共用 | ToC 与 ToB | 个人和企业用户共用同一个机票 MCP | [Flight Booking AI MCP](https://github.com/tourmind-com/flight-booking-ai-mcp.git) |

## 1 分钟安装

任选下面一种方式即可。

### 让 Agent 帮你安装

复制下面这段话，发送给你的 Agent：

```text
请帮我接入 TourMind Booking Skills。Skill 仓库地址：git@github.com:tourmind-com/Tourmind-Booking-Skills.git。
```

### 或者使用一条命令安装

```bash
npx skills add tourmind-com/tourmind-booking-skills
```

安装器会识别两个独立 Skill：酒店使用 `tourmind-booking`，机票使用 `flight-booking-ai`。按照提示同时选中两个即可。如果你确定要跳过选择，并将两个 Skill 安装到所有已检测到的 Agent 客户端，可以在命令末尾添加 `--all`。

搜索和比较酒店、查询机场不需要 Token。机票实时搜索和验价，以及任何真实预订、订单或支付操作都需要 Token。

如果你已有 TourMind 账号，可以使用账号中的 [Skill Token](https://tourmind.com/user/skill-token)。开发者和个人用户也可以前往 [auth.journione.ai](https://auth.journione.ai) 获取兼容的 Token。请只在私密对话中发送给你信任的 Agent：

```text
请使用以下 TourMind Skill Token 调用 AI Skill：
<YOUR_SKILL_TOKEN>

Token 仅用于 TourMind AI Skill 鉴权，请不要在公开对话、公开代码仓库或共享文档中暴露完整 Token。
```

Agent 会自动为已安装的 Skill 保存并配置 Token，你不需要自己创建或修改 Token 文件。

安装完成后，直接让 Agent 帮你找酒店、查机票，或者把两者放在一起规划即可。

## 示例 Prompt

### 搜索酒店

```text
帮我找 2026 年 12 月 9 日至 13 日东京的酒店，两位成人入住。希望是靠近交通便利车站的双床房，平均每晚不超过 18,000 日元，优先免费取消，最好含早餐。请展示当前最合适的 5 个选项，包括房型图片、入住总价、餐食、取消政策和各自优缺点。暂时不要预订。
```

### 搜索机票

```text
帮我查 2026 年 12 月 9 日从上海前往东京、12 月 13 日从东京返回上海的往返机票，两位成人，经济舱，优先直飞。请按总价、起降时间、机场、中转次数、飞行时长和行李额度对比可选航班，展示每个选项的托运行李额度，并标出包含每人至少一件托运行李的航班。暂时不要预订。
```

### 一起规划机票和酒店

```text
帮两个人规划一次大阪五日游。先对比时间合适的往返机票，再根据日期和预算找交通方便的酒店，说明最值得考虑的机票与酒店组合，并分别列出预计机票和酒店费用。先让我选择，不要自动下单。
```

### 继续查看喜欢的酒店

```text
我比较喜欢你刚才推荐的那家靠近新宿站的酒店。请看看现在还有哪些双床房，重新核验最划算的房型，并告诉我最终价格、餐食和取消政策。然后告诉我接下来需要提供哪些信息，等我确认后再预订。
```

### 继续查看喜欢的航班

```text
刚才那个上午出发的直飞航班最适合我。请重新核验最新总价，再汇总行程和托运行李额度，并告诉我需要提供哪些乘机人与联系人信息。把完整预订信息给我核对，等我确认后再帮我预订。
```

### 查询订单

```text
请帮我查一下刚才预订的酒店或机票现在是什么状态。如果还可以支付，先告诉我可用的支付方式和最终金额，等我确认后再继续。
```

## 工作流程

以下步骤均由 Agent 在对话中完成，你不需要自己调用接口或管理本地文件。

### 酒店搜索与预订

```text
目的地、日期、入住人数、房间数、预算和偏好
  → 解析城市、区域、地点或指定酒店（search_location / 酒店名称搜索）
  → 搜索最多 20 家候选酒店（search_hotels）
  → 批量核验实时房型与入住总价（batch_query_room_rates；单家酒店使用 query_room_rates）
  → 排序并展示最多 5 家经过核验的酒店
  → 展示所选酒店的详情、图片和实时房型（get_hotel_detail + 实时房价查询）
  → 根据酒店详情核对必要费用，再重新核验所选房型的最终价格、库存和取消政策（check_room_availability）
  → 订单操作需要认证时配置 Token；如果渠道发生变化，先重新查询房价；无论渠道是否变化，都要使用新 Token 重新核验最终价格和库存
  → 提供住客的证件姓名和联系邮箱
  → 展示完整预订信息并等待明确确认
  → 创建酒店订单（create_booking）
  → 按用户要求查询订单；发起支付或取消符合条件的酒店订单前，需要分别获得明确确认（query_booking / pay_order / cancel_booking）
```

`search_hotels` 返回的候选起价只用于初步筛选。向用户展示的可订价格来自实时房价查询，最终下单使用 `check_room_availability` 返回的最新结果。选择酒店或房型不等于确认预订；支付和取消都需要分别核对并再次确认。选择 Stripe 时，Agent 会先说明额外收取的 3.5% 处理费，以及该费用一旦收取便不可退款。

### 机票搜索与预订

```text
航线、日期、行程类型、舱等、航班偏好及成人 / 儿童 / 婴儿人数
  → 查询机场并核对日期和乘客组成（search_airports）
  → 配置 Token 后搜索实时航班（search_flights）
  → 对比前 10 个航班报价的时间、机场、舱等、中转、行李和总价
  → 在搜索结果生成后未满 20 分钟时选择一个报价
  → 重新核验所选航班与最新总价（verify_offer）
  → 提供乘机人、旅行证件和联系人信息
  → 核对完整行程、价格和乘机人信息，并明确确认预订
  → 创建机票订单（create_booking）
  → 查询订单，仅在订单仍可支付时继续（query_order）
  → 选择支付方式，核对完整支付信息，并单独确认支付
  → 再次查询订单；只有信息未变化且订单仍可支付时，才创建一次支付链接（create_payment）
  → 按需查询订单或支付状态（query_order / query_payment）
```

选择航班只代表允许重新验价，不代表确认预订。如果搜索条件发生变化或距离搜索完成已经达到 20 分钟，Agent 会先征得同意再重新搜索。支付链接不代表已经支付成功或已经出票。Stripe 会额外收取 3.5% 且不可退款的处理费；WeChat Pay、Alipay 和 Online Banking 仅适用于 CNY 订单。

机票 Skill 当前支持机场查询、实时航班搜索与验价、预订、订单查询，以及第三方支付创建和查询。暂不执行机票取消、改签、发起退款、购买附加服务或人工出票操作；这些需求请联系机票客服。

## Token 与安全说明

- 酒店和机票 Skill 共用同一个 TourMind Skill Token；每位用户只需申请一次，无需重复申请。
- 任一已安装的 Skill 需要鉴权时，Agent 都会将同一个 Token 保存到该 Skill 本地的 `skill_token.txt` 中。所有 ToB Skill API 调用都必须使用对应本地文件中的 Token，你无需自行创建或编辑文件。
- 不要在 Prompt、日志、截图、URL、Git 提交或 Issue 中暴露完整 Token。
- 在 macOS 或 Linux 上，Agent 会执行 `chmod 600 skill_token.txt`，将 Token 文件权限限制为仅当前用户可读写。
- 收到 HTTP 401 或包含 `unauthorized` 的认证响应时，Agent 会删除失效的本地 Token，并停止本次认证操作。单独的“权限未开通”响应不会被当作 Token 失效。
- 返回的酒店查询结果页面是只读的，在过期前可重复打开。
- 创建酒店或机票预订、取消符合条件的酒店订单或发起支付前，必须在已认证的 AI 对话中获得用户明确确认。

## FAQ

[TourMind Skill 使用常见问题](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues/23#issue-5276313315)

## 帮助与支持

- 产品页面：[tourmind.com/skills](https://tourmind.com/skills)
- 开发者与个人用户获取 Token：[auth.journione.ai](https://auth.journione.ai)
- GitHub 支持：[提交 Issue](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues)
- 酒店支持：[hotel@tourmind.com](mailto:hotel@tourmind.com)
- 机票 24 小时客服：[flightcs1@tourmind.com](mailto:flightcs1@tourmind.com)
- 商务合作：[bp@tourmind.com](mailto:bp@tourmind.com)
- AI 产品合作：[ai@tourmind.com](mailto:ai@tourmind.com)

## 开源许可

[MIT](LICENSE) © 2026 TourMind
