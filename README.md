# Auto-Stocker (1x8) システム

ローカルLAN内で動作する小型自動入出庫システムの参照実装です。

主な構成:
- Flask + Gunicorn (バックエンド API)
- PostgreSQL (製品マスター・棚ステータス・履歴)
- Arduino (USB シリアル経由でLED制御)

起動手順（開発用）:
1. Python 仮想環境を作成し有効化
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 設定を config.py で編集（DB 接続 / シリアルポート）
3. DB 初期化
   ```bash
   python scripts/init_db.py
   ```
5. 管理者ユーザー作成（任意）
   ```bash
   python scripts/create_admin.py admin strongpassword
   ```
4. 開発サーバー起動
   ```bash
   flask run --host=0.0.0.0
   ```

デプロイ / systemd / gunicorn の設定や cron によるログローテーション例は `deploy/` にあります。

CI (GitHub Actions): `.github/workflows/ci.yml` を追加しました。プッシュ/PR 時に `pytest` を自動実行します。

デプロイ手順は `deploy/DEPLOYMENT.md` を参照してください（nginx 設定例、systemd ユニット、cron 例を含む）。
