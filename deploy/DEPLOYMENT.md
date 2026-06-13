Auto-Stocker デプロイ手順（Ubuntu 22.04 / 24.04 想定）

前提:
- サーバーに root または sudo 権限があること
- PostgreSQL がインストール済みであり DB/ユーザーを作成できること
- Arduino の接続はサーバー側で行うか、テスト時はモックで運用

1) ユーザー・環境準備
```bash
sudo useradd -r -s /bin/false autostocker || true
sudo mkdir -p /opt/auto-stocker
sudo chown $USER:$USER /opt/auto-stocker
cd /opt/auto-stocker
```

2) ソース配置（Git clone など）
```bash
git clone <repo> .
```

3) 仮想環境と依存インストール
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

4) PostgreSQL セットアップ
```sql
-- psql
CREATE USER stk_user WITH PASSWORD 'strongpass';
CREATE DATABASE auto_stocker OWNER stk_user;
```
config.py の `DB_URL` を `postgresql://stk_user:strongpass@localhost:5432/auto_stocker` に合わせて編集。

5) DB 初期化
```bash
python scripts/init_db.py
```

6) Gunicorn + systemd 設定
- `deploy/auto-stocker.service` を `/etc/systemd/system/auto-stocker.service` にコピーし、`ExecStart` のパスを環境に合わせる。

```bash
sudo cp deploy/auto-stocker.service /etc/systemd/system/auto-stocker.service
sudo systemctl daemon-reload
sudo systemctl enable --now auto-stocker.service
sudo journalctl -u auto-stocker -f
```

7) nginx 設定
- `deploy/nginx_auto_stocker.conf` を `/etc/nginx/sites-available/auto-stocker` に配置し、`sites-enabled` へリンク
```bash
sudo cp deploy/nginx_auto_stocker.conf /etc/nginx/sites-available/auto-stocker
sudo ln -s /etc/nginx/sites-available/auto-stocker /etc/nginx/sites-enabled/auto-stocker
sudo nginx -t
sudo systemctl restart nginx
```

8) シリアルデバイス権限
- Arduino を接続し、`config.py` の `SERIAL_PORT` を実機に合わせる。
- `www-data`（Gunicorn 実行ユーザー）がデバイスにアクセスできるようにグループ付与等を設定。

9) Cron ログローテーション
```bash
sudo cp deploy/cron_rotate.sh /opt/auto-stocker/deploy/cron_rotate.sh
sudo chmod +x /opt/auto-stocker/deploy/cron_rotate.sh
# crontab -e
# 0 0 1 * * /opt/auto-stocker/deploy/cron_rotate.sh
```

トラブルシューティング:
- Gunicorn が起動しない: `journalctl -u auto-stocker -b` を確認
- nginx 502: Gunicorn のポート（8000）へ接続出来るか確認

セキュリティ:
- 実運用では `SECRET_KEY` を安全に管理し、DB パスワードは平文で置かないこと（環境変数など）。
