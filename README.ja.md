<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">TourMind Booking Skills</a></b><br />
  <strong>AI Agent で世界中のホテルと航空券を検索・予約</strong>
</h1>

<a href="https://tourmind.com/skills">
  <img alt="TourMind Booking Skills" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  お客様をスマートな旅へ
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">製品ページ</a> |
  <a href="https://auth.journione.ai">Token を取得</a> |
  <a href="https://tourmind.com">会社サイト</a>
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

AI Agent に、ホテルの検索から予約までを完結できる機能と、世界中の航空券を検索・予約できる機能を追加します。普段お使いの Agent クライアントを離れることなく、世界中のホテルとフライトを検索し、主要な OTA やサプライヤーのリアルタイム料金を比較して、空室・空席状況と最終料金を確認できます。TourMind Booking Skills を通じて予約と決済を完了し、予約状況を確認できます。

## ホテル Skill のデモ

以下の GIF では、ホテル Skill の利用イメージをご覧いただけます。

### 1. リアルタイムでホテルを検索

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="TourMind ホテル検索デモ" width="720" />
  </a>
</div>

### 2. 実際の客室を比較

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="TourMind 客室比較デモ" width="720" />
  </a>
</div>

### 3. 最終料金を確認して決済

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="TourMind ホテル料金確認・決済デモ" width="720" />
  </a>
</div>

## 主な機能

- **ホテル：** 世界中のホテルとリアルタイムの客室を検索し、料金、写真、設備、食事、キャンセル条件を比較できます。空室を再確認して、予約、決済、キャンセルまで進められます。
- **航空券：** 空港を検索し、片道、往復、複数都市のフライトを比較できます。時刻、座席クラス、乗り継ぎ、手荷物、合計金額を確認し、選んだ運賃の再確認、予約、予約状況の確認、決済へ進められます。
- **旅程をまとめて計画：** 日程、予算、希望に合わせて旅程を作り、航空券とホテルを一緒に探すよう Agent に依頼できます。
- **安心できる取引：** 検索だけで予約が作成されることはありません。ホテルまたは航空券の予約、対象となるホテル予約のキャンセル、決済の前に、Agent が重要な内容を表示し、明示的な確認を待ちます。
- **自然な会話：** 複雑な検索フォームを使わず、使い慣れた言語で希望を伝えられます。

## 対応 Agent クライアント

TourMind Booking Skills は、ChatGPT（Work / Codex モード）、Claude Code、WorkBuddy、QClaw、Marvis、OpenClaw、Kimi Work、Doubao Work Mode、Qwen Work Mode、Hermes、Cursor、および Skill に対応するその他の Agent クライアントで利用できます。

## 最適な TourMind 連携方法を選ぶ

この Skill リポジトリは、ホテルと航空券について個人ユーザー（ToC）と法人ユーザー（ToB）の両方に対応しています。MCP は構成が異なるため、用途に合う接続先を選択してください。

| 連携方法 | 対象ユーザー | 機能 | リポジトリ |
|---|---|---|---|
| TourMind Booking Skills | ToC・ToB | ホテル・航空券 Skills | **[このリポジトリ](https://github.com/tourmind-com/Tourmind-Booking-Skills)** |
| ホテル MCP — 個人（ToC） | ToC | 個人ユーザー向けのホテル検索・予約 | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| ホテル MCP — 法人（ToB） | ToB | 法人ユーザー向けのホテル検索・予約 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |
| 航空券 MCP — 個人・法人共通 | ToC・ToB | 個人・法人ユーザーで共用する航空券 MCP | [Flight Booking AI MCP](https://github.com/tourmind-com/flight-booking-ai-mcp.git) |

## 1分でインストール

次のどちらかの方法を選んでください。

### Agent にインストールを依頼

次のメッセージをコピーして Agent に送信します。

```text
TourMind Booking Skills を導入してください。Skill リポジトリ：git@github.com:tourmind-com/Tourmind-Booking-Skills.git。
```

### またはコマンドを1つ実行

```bash
npx skills add tourmind-com/tourmind-booking-skills
```

ホテルの検索・比較と空港検索には Token は必要ありません。リアルタイムの航空券検索・料金確認、および実際の予約、予約状況の確認、決済には Token が必要です。

TourMind アカウントをお持ちの場合は、アカウントの [Skill Token](https://tourmind.com/user/skill-token) を利用できます。開発者と個人ユーザーは [auth.journione.ai](https://auth.journione.ai) で利用可能な Token を取得できます。信頼できる Agent に、非公開の会話でのみ送信してください。

```text
AI Skill で以下の TourMind Skill Token を使用してください：
<YOUR_SKILL_TOKEN>

この Token は TourMind AI Skill の認証専用です。公開チャット、公開コードリポジトリ、共有ドキュメントに Token 全文を記載しないでください。
```

Agent がインストール済みの各 Skill 用に Token を保存・設定します。ご自身で Token ファイルを作成・編集する必要はありません。

インストール後は、ホテル探し、航空券検索、またはその両方を組み合わせた旅行計画を Agent に依頼してください。

## プロンプト例

### ホテルを検索

```text
2026年12月9日から13日まで、大人2名で東京に泊まるホテルを探してください。交通の便利な駅に近いツインルームで、平均1泊18,000円以下、無料キャンセルを優先し、できれば朝食付きが希望です。客室写真、滞在合計、食事、キャンセル条件、各候補の長所と短所を含めて、現在予約可能な上位5件を表示してください。まだ予約はしないでください。
```

### 航空券を検索

```text
2026年12月9日に上海から東京へ出発し、12月13日に東京から上海へ戻る大人2名の往復航空券を探してください。エコノミークラスで直行便を優先してください。利用可能なフライトを合計金額、出発・到着時刻、空港、乗り継ぎ回数、所要時間、手荷物条件で比較し、各候補の受託手荷物許容量と、1人1個以上を含む候補を示してください。まだ予約はしないでください。
```

### 航空券とホテルをまとめて計画

```text
2人で行く5日間の大阪旅行を計画してください。まず利用しやすい往復航空券を比較し、その後、日程と予算に合う便利な立地のホテルを探してください。おすすめの航空券とホテルの組み合わせを説明し、予想される航空券代とホテル代を別々に表示してください。何も予約せずに私の選択を待ってください。
```

### 気に入ったホテルを詳しく確認

```text
先ほどおすすめしてくれた新宿駅近くのホテルが気に入りました。現在利用できるツインルームを確認し、最もお得なプランの最新料金、食事、キャンセル条件をもう一度確認してください。次に必要な情報を教えて、私が確認するまで予約しないでください。
```

### 気に入ったフライトを詳しく確認

```text
先ほど表示された午前出発の直行便が一番よさそうです。最新の合計金額を再確認してから、旅程と受託手荷物許容量をまとめてください。次に必要な搭乗者情報と連絡先情報を教え、予約内容をすべて表示して、私が確認するまで予約を確定しないでください。
```

### 予約状況を確認

```text
先ほど予約したホテルまたは航空券の状況を確認して、現在の状態を分かりやすく説明してください。まだ支払い可能な場合は、利用できる決済方法と最終金額を先に表示し、私が確認するまで先へ進まないでください。
```

## 予約ワークフロー

以下の手順は Agent が会話内で行います。ご自身で API を呼び出したり、ローカルファイルを管理したりする必要はありません。

### ホテルの検索と予約

```text
目的地、日程、宿泊人数、客室数、予算、希望条件
  → 都市、エリア、地点、または指定ホテルを特定（search_location / ホテル名検索）
  → 最大20件の候補ホテルを検索（search_hotels）
  → リアルタイムの客室と宿泊合計を一括確認（batch_query_room_rates、1軒の場合は query_room_rates）
  → 検証済みホテルを順位付けし、最大5件を表示
  → 選択したホテルの詳細、画像、リアルタイム客室を表示（get_hotel_detail + 客室料金照会）
  → ホテル詳細の必須料金を確認してから、選択した客室の最終料金、空室、キャンセル条件を再確認（check_room_availability）
  → 注文操作に認証が必要な場合は Token を設定し、チャネルが変わった場合は先に客室料金を再照会する。チャネル変更の有無にかかわらず、新しい Token で最終料金と空室を再確認する
  → 宿泊者のパスポート等に記載された氏名と連絡先メールアドレスを提供
  → 予約内容をすべて表示し、明示的な確認を待つ
  → ホテル予約を作成（create_booking）
  → ユーザーの依頼に応じて予約を照会し、決済または対象となるホテル予約のキャンセル前には、それぞれ明示的な確認を得る（query_booking / pay_order / cancel_booking）
```

`search_hotels` の候補料金は初期判断用です。ユーザーに表示する予約可能な料金はリアルタイムの客室料金照会から取得し、予約には `check_room_availability` の最新結果を使用します。ホテルや客室の選択は予約確認ではありません。決済とキャンセルには、それぞれ個別の内容確認と承認が必要です。Stripe を選択した場合、Agent は追加の3.5%処理手数料と、徴収後は返金されないことを事前に説明します。

### 航空券の検索と予約

```text
経路、日程、旅程タイプ、座席クラス、希望条件、成人 / 子ども / 幼児の人数
  → 空港を検索し、日付と旅客構成を確認（search_airports）
  → Token を設定してリアルタイムのフライトを検索（search_flights）
  → 上位10件の運賃を時刻、空港、座席クラス、乗り継ぎ、手荷物、合計金額で比較
  → 検索結果の取得から20分未満のうちに運賃を選択
  → 選択したフライトと最新合計金額を再確認（verify_offer）
  → 搭乗者、渡航書類、連絡先情報を提供
  → 旅程、料金、搭乗者情報をすべて確認し、予約を明示的に承認
  → 航空券予約を作成（create_booking）
  → 予約を照会し、まだ支払い可能な場合のみ続行（query_order）
  → 決済方法を選び、決済内容をすべて確認して、決済を別途承認
  → 予約を再照会し、内容が変わらず支払い可能な場合に限り、決済リンクを1回作成（create_payment）
  → 必要に応じて予約または決済状況を照会（query_order / query_payment）
```

フライトの選択は料金の再確認を許可するだけで、予約の承認ではありません。検索条件が変わった場合、または検索結果の取得から20分以上経過した場合、Agent は同意を得てから新しく検索します。決済リンクは、支払い完了や発券完了の証明ではありません。Stripe には追加の3.5%の返金不可の処理手数料がかかります。WeChat Pay、Alipay、Online Banking は CNY の予約でのみ利用できます。

航空券 Skill は現在、空港検索、リアルタイムのフライト検索・料金確認、予約、予約照会、第三者決済の作成・照会に対応しています。航空券のキャンセル、変更、返金申請、付帯サービスの購入、手動発券操作は行いません。これらについては航空券カスタマーサービスへお問い合わせください。

## Token とセキュリティ

- ホテルと航空券の Skill は、同じ TourMind Skill Token を共有します。ユーザーごとに一度取得すればよく、個別に申請する必要はありません。
- インストール済みのいずれかの Skill で認証が必要になると、Agent は同じ Token をその Skill のローカル `skill_token.txt` に保存します。すべての ToB Skill API 呼び出しでは、対応するローカルファイルに保存された Token を使用する必要があります。ファイルを自分で作成・編集する必要はありません。
- Prompt、ログ、スクリーンショット、URL、Git コミット、Issue に Token 全文を記載しないでください。
- macOS または Linux では、Agent が `chmod 600 skill_token.txt` を実行し、現在のユーザーだけが Token ファイルを読み書きできるようにします。
- 認証済みリクエストが HTTP 401 または `unauthorized` を返した場合、Agent は無効なローカル Token を削除し、その認証操作を停止します。権限が未付与であることを示す別のレスポンスは、Token の無効として扱いません。
- 返されたホテル検索結果ページは読み取り専用で、有効期限までは繰り返し開くことができます。
- ホテルまたは航空券の予約作成、対象となるホテル予約のキャンセル、または決済の開始には、認証済みの AI 会話内でユーザーの明示的な確認が必要です。

## FAQ

[TourMind Skill のよくある質問](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues/23#issue-5276313315)

## ヘルプとサポート

- 製品ページ：[tourmind.com/skills](https://tourmind.com/skills)
- 開発者・個人ユーザー向け Token：[auth.journione.ai](https://auth.journione.ai)
- GitHub サポート：[Issue を作成](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues)
- ホテルサポート：[hotel@tourmind.com](mailto:hotel@tourmind.com)
- 航空券カスタマーサービス（24時間年中無休）：[flightcs1@tourmind.com](mailto:flightcs1@tourmind.com)
- ビジネス提携：[bp@tourmind.com](mailto:bp@tourmind.com)
- AI 製品提携：[ai@tourmind.com](mailto:ai@tourmind.com)

## ライセンス

[MIT](LICENSE) © 2026 TourMind
