# TourMind ホテル予約 Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

あらゆる AI エージェントをエンドツーエンドのホテル予約アシスタントに変えます。世界中のホテル在庫を検索し、主要 OTA とホテルサプライヤーのリアルタイム料金を比較し、空室を確認して、TourMind との1回の会話で予約、決済、キャンセル、注文管理まで完了できます。

## デモ

### 1. リアルタイムでホテルを検索

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="TourMind ホテル検索デモ" width="720" />
  </a>
</div>

### 2. 実際の客室を比較

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="TourMind 客室詳細デモ" width="720" />
  </a>
</div>

### 3. 最終料金を確認して決済

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="TourMind 料金確認・決済デモ" width="720" />
  </a>
</div>

## 主な機能

- 都市、ホテル、ランドマーク、駅、住所、スキー場などの POI を、座標を推測せずに解決します。
- 最大 20 件のホテル候補を検索し、条件に合うリアルタイム客室商品を照会して、検証済みの上位 5 件を選択します。
- 主要 OTA とホテルサプライヤーの1泊料金、滞在合計、キャンセル条件、在庫状態をリアルタイムで比較します。
- ホテル・客室画像、設備、ベッド、食事、料金情報、根拠に基づくおすすめ理由を返します。
- 予約前に、選択した客室の料金と空室状況を再確認します。
- 予約作成、注文照会・キャンセル、Stripe、WeChat Pay、Alipay の支払い開始に対応します。
- Skill Token を公開せず、有効期限内に繰り返し開ける読み取り専用結果リンクを提供します。

## 対応 AI クライアント

| クライアント | 対応方法 |
|---|---|
| WorkBuddy | このリポジトリをユーザー Skill としてインストールまたはインポート |
| OpenAI Codex | Skills 画面、または現在のバージョンが対応するローカル Skill ディレクトリからインストール |
| Claude Code | `~/.claude/skills` に個人 Skill としてインストール |
| Agent Skills 互換クライアント | ルートの `SKILL.md` を読み込み、HTTPS `POST` リクエストを送信できる場合に利用可能 |
| MCP 対応 AI クライアント | 付属の [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) パッケージを使用 |

## 1分でインストール

1. TourMind アカウントにログインし、[tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) で Skill Token を作成します。アカウントがない場合は、[法人アカウント登録](https://tourmind.com/admin/skillSignup) を利用してください。開発者または個人ユーザーは、ユーザー種別に対応する TourMind Skill バージョンを使用してください。

2. AI クライアントの Skills 画面で、次の GitHub リポジトリをインストールまたはインポートします。

   ```text
   https://github.com/tourmind-com/Tourmind-Booking-Skills.git
   ```

   クライアントがファイルシステムから Skill を読み込む場合は、個人 Skill ディレクトリにリポジトリをクローンします。

   ```bash
   CLIENT_SKILLS_DIR="<クライアントのSkillディレクトリ>"
   mkdir -p "$CLIENT_SKILLS_DIR"
   git clone https://github.com/tourmind-com/Tourmind-Booking-Skills.git "$CLIENT_SKILLS_DIR/tourmind-booking"
   ```

   一般的な個人 Skill ディレクトリ：

   | クライアント | ディレクトリ |
   |---|---|
   | WorkBuddy | `~/.workbuddy/skills` |
   | OpenAI Codex | Skills 画面、または現在の Codex バージョンが対応するローカルディレクトリを使用 |
   | Claude Code | `~/.claude/skills` |

3. インストールした `tourmind-booking` フォルダ内に `skill_token.txt` を作成し、Token 本体だけを貼り付けます。macOS または Linux ではアクセス権を制限します。

   ```bash
   chmod 600 skill_token.txt
   ```

Skills を再読み込みするか AI クライアントを再起動して、ホテルを依頼します。ローカル MCP サーバーは不要で、この Skill は HTTPS で TourMind API を直接呼び出します。

`skill_token.txt` は絶対にコミットしないでください。このファイルは `.gitignore` で除外されています。

## プロンプト例

以下の例では、エージェント自身の調査・旅程作成能力と、TourMind のリアルタイムホテル検索、料金確認、予約、決済、注文管理を組み合わせています。

```text
2名で、2027年4月9日から13日まで4泊の日本・大阪（Osaka）旅行を計画しています。関西国際空港を往復利用し、大阪湾または淡路島周辺で1～2日間の海釣りをしたいですが、レンタカーは使いません。まず、あなた自身のウェブ調査と旅程作成能力を使って、旅行者に現実的な釣りエリア、季節条件、適法なチャーター船や乗合船、公共交通の所要時間を比較し、無理のない日別プランを提案してください。そのうえで、最適な滞在拠点について TourMind でリアルタイムのホテル在庫を検索してください。平均1泊18,000円以内、ツインルーム、駅に近いこと、早朝に釣りの集合場所へ移動しやすいこと、無料キャンセルを優先し、朝食は出発時間に合う場合に希望します。検証済みの上位5軒について、客室写真、滞在合計と通貨、返された税・手数料、キャンセル条件、朝食、釣り場所への移動方法、主な長所と短所、繰り返し開ける結果リンクを表示してください。まだ予約はしないでください。
```

```text
大人2名で、2027年2月6日から12日まで6泊のイタリア・ドロミテ（Dolomites）スキー旅行を計画してください。ヴェネツィア・マルコポーロ空港に到着し、車は使わず、スキーレベルは中級です。まず、空港送迎、ゲレンデ、食事、費用対効果の観点から Cortina d’Ampezzo、Val Gardena、Alta Badia を比較し、最適な滞在拠点と現実的な日別プランを提案してください。次に TourMind を使い、平均1泊250ユーロ以下で、できればリフトまで徒歩またはシャトルで10分以内、スキー保管室、朝食、無料キャンセルがあり、可能ならサウナ付きの空室を検索してください。検証済みの上位5軒について、客室・ベッドタイプ、写真、1泊料金と滞在合計、キャンセル期限、食事、在庫状況、リフトまでの距離、満たしていない条件を表示してください。私が選んだ後、その客室の料金と空室を再確認し、正確な最終金額と条件をまとめ、明示的に確認するまで予約や決済を開始しないでください。
```

```text
比較結果の2番目のホテルを使ってください。ホテル詳細と、大人2名に適合する現在予約可能なすべての客室商品を、客室写真、ベッドタイプ、食事、キャンセル条件、リクエスト予約かどうか、1泊料金、滞在合計とともに表示してください。最も費用対効果の高い料金を推薦し、理由を説明してから、その正確な料金を再確認してください。変更があれば確認前後の値を明確に示し、変更がなければ最終予約内容をまとめて確認を求めてください。私が「予約を確定」と明示するまで、予約作成も決済開始もしないでください。
```

```text
エージェント参照ID <AGENT_REF_ID> を使って予約を照会し、現在の予約状況と支払い状況を分かりやすく説明してください。キャンセル可能な場合は、操作する前にキャンセル期限、違約金、予想返金額を表示してください。私が明示的に確認した後にだけキャンセルし、その後もう一度予約を照会して最終状態を表示してください。回答や結果リンクに Skill Token を公開しないでください。
```

## ワークフロー

```text
場所または POI
  → search_location
  → search_hotels（最大 20 件）
  → query_room_rates（対象候補のリアルタイム客室商品）
  → 検証済み上位 5 ホテルを順位付けして表示
  → get_hotel_detail + 客室画像と料金
  → 選択料金に対して check_room_availability
  → 明示的な確認後に create_booking
  → 必要に応じて pay_order / query_booking / cancel_booking
```

キャッシュされた `search_hotels.min_price` は候補選定用の参考値です。ユーザーに表示する料金は `query_room_rates` から取得し、予約には `check_room_availability` が返す最新の値を使用します。

## Token とセキュリティ

- すべての ToB Skill API 呼び出しには、ローカルの `skill_token.txt` に保存した Skill Token が必要です。
- Token をプロンプト、ログ、スクリーンショット、URL、コミット、Issue に含めないでください。
- `chmod 600` を使用して、Token ファイルを現在のユーザーだけが読み書きできるようにします。
- HTTP 401 または `unauthorized` が返された場合は、無効なローカル Token を削除します。再発行するには TourMind アカウントにログインし、[tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) で Skill Token を作成してください。アカウントがない場合は [法人アカウント登録](https://tourmind.com/admin/skillSignup) を利用し、開発者または個人ユーザーはユーザー種別に対応する Skill バージョンを使用してください。
- 結果の `web_url` は読み取り専用で、有効期限までは繰り返し開けます。料金再確認、予約、決済、キャンセル、アカウント・財務ページへのアクセスはできません。
- 予約、キャンセル、決済は、認証済み AI 会話内でユーザーが明示的に確認した場合のみ実行します。

## Skill / MCP / ToB / ToC の選択

| 対象 | 接続方式 | 認証モデル | リポジトリ |
|---|---|---|---|
| コンシューマー / ToC | 直接 HTTP Skill | 検索・空室確認は公開、注文操作のみ `user_key` が必要 | [Hotel Booking AI](https://github.com/tourmind-com/Hotel-Booking-AI) |
| ビジネス / ToB | 直接 HTTP Skill | すべての API 呼び出しに Skill Token が必要 | **[TourMind Booking Skill](https://github.com/tourmind-com/Tourmind-Booking-Skills)** |
| コンシューマー / ToC | MCP + 付属 Skill | MCP 接続は公開、注文操作のみ `user_key` が必要 | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| ビジネス / ToB | MCP + 付属 Skill | Bearer 認証された MCP 接続 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API とサポート

**API ベース URL:** `https://api.tourmind.com`

| エンドポイント | 用途 |
|---|---|
| `POST /skill/tob/check_skill_update` | Skill の更新確認 |
| `POST /skill/tob/search_location` | 地域、POI、ホテルの解決 |
| `POST /skill/tob/search_hotels` | ホテル候補の検索 |
| `POST /skill/tob/get_hotel_detail` | ホテル詳細と画像の取得 |
| `POST /skill/tob/query_room_rates` | リアルタイム客室と料金の取得 |
| `POST /skill/tob/check_room_availability` | 選択料金と在庫の再確認 |
| `POST /skill/tob/create_booking` | 確認済み予約の作成 |
| `POST /skill/tob/query_booking` | 注文の照会 |
| `POST /skill/tob/cancel_booking` | 確認後の注文キャンセル |
| `POST /skill/tob/pay_order` | 確認後の支払い開始 |

- リクエスト項目とレスポンス契約：[references/parameter_guide.md](references/parameter_guide.md)
- Skill Token：ログイン後、[tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) にアクセスしてください。アカウントがない場合は [法人アカウント登録](https://tourmind.com/admin/skillSignup) を利用し、開発者または個人ユーザーはユーザー種別に対応する Skill バージョンを使用してください。
- 製品ページ：[tourmind.com/skills](https://tourmind.com/skills)
- GitHub サポート：[Issue を作成](https://github.com/tourmind-com/Tourmind-Booking-Skills/issues)
- ホテル事業に関するお問い合わせ：`hotel@tourmind.com`
- ビジネス提携：`bp@tourmind.com`

## ライセンス

[MIT](LICENSE) © 2026 TourMind
