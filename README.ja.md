# TourMind ホテル予約 Skill

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

あらゆる AI エージェントをエンドツーエンドのホテル予約アシスタントに変えます。世界中のホテル在庫を検索し、主要 OTA とホテルサプライヤーのリアルタイム料金を比較し、空室を確認して、TourMind との1回の会話で予約、決済、キャンセル、注文管理まで完了できます。

## デモ

> **追加予定：** ホテル検索、リアルタイム客室料金、最終的な料金・空室確認、予約までを示す実際のスクリーンショットまたは短い GIF を追加します。

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

1. [tourmind.com/user/skill-token](https://tourmind.com/user/skill-token) で Skill Token を生成します。

2. AI クライアントの Skills 画面で、次の GitHub リポジトリをインストールまたはインポートします。

   ```text
   https://github.com/tourmind-com/Tourmind-Booking-Skill.git
   ```

   クライアントがファイルシステムから Skill を読み込む場合は、個人 Skill ディレクトリにリポジトリをクローンします。

   ```bash
   CLIENT_SKILLS_DIR="<クライアントのSkillディレクトリ>"
   mkdir -p "$CLIENT_SKILLS_DIR"
   git clone https://github.com/tourmind-com/Tourmind-Booking-Skill.git "$CLIENT_SKILLS_DIR/tourmind-booking"
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

```text
9月12日から9月14日まで、大人2名で、深圳の西麗地下鉄駅から3 km以内のホテルを探してください。
```

```text
確認済みのリアルタイム客室料金、朝食、キャンセル条件、滞在合計を含めて、最適なホテルを5件表示してください。
```

```text
ホテル検索で返された候補をすべて表示し、必須条件を満たさない候補には理由を明記してください。
```

```text
選択した客室を再確認し、最終料金とキャンセル条件を私が確認した後に予約と支払いを手伝ってください。
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
- HTTP 401 または `unauthorized` が返された場合は、無効なローカル Token を削除して再発行します。
- 結果の `web_url` は読み取り専用で、有効期限までは繰り返し開けます。料金再確認、予約、決済、キャンセル、アカウント・財務ページへのアクセスはできません。
- 予約、キャンセル、決済は、認証済み AI 会話内でユーザーが明示的に確認した場合のみ実行します。

## Skill / MCP / ToB / ToC の選択

| 対象 | 接続方式 | 認証モデル | リポジトリ |
|---|---|---|---|
| コンシューマー / ToC | 直接 HTTP Skill | 検索・空室確認は公開、注文操作のみ `user_key` が必要 | [Hotel Booking AI](https://github.com/tourmind-com/Hotel-Booking-AI) |
| ビジネス / ToB | 直接 HTTP Skill | すべての API 呼び出しに Skill Token が必要 | **[TourMind Booking Skill](https://github.com/tourmind-com/Tourmind-Booking-Skill)** |
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
- Skill Token：[tourmind.com/user/skill-token](https://tourmind.com/user/skill-token)
- 製品ページ：[tourmind.com/skill](https://tourmind.com/skill)
- GitHub サポート：[Issue を作成](https://github.com/tourmind-com/Tourmind-Booking-Skill/issues)
- ホテル事業に関するお問い合わせ：`hotel@tourmind.com`
- ビジネス提携：`bp@tourmind.com`

## ライセンス

[MIT](LICENSE) © 2026 TourMind
