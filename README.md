# Backlog風 TODO管理アプリ

個人利用向けのタスク管理アプリです。親子タスク、カンバン、タイムライン、ダッシュボードを備えています。

## 1. 起動方法

```bash
cp .env.example .env

docker-compose up --build
```

- Appleシリコン（M1/M2/M3）環境では `docker-compose.yml` に `platform: linux/arm64` を指定済みです。

- Web UI: http://localhost:3000
- API docs: http://localhost:8000/docs
- API health: http://localhost:8000/health

## 2. 初回セットアップ（マイグレーション/シード）

`backend/scripts/start.sh` で自動的に以下が実行されます。

```bash
alembic upgrade head
python -m app.seed
```

## 3. 主なURL

- Web UI: `http://localhost:3000`
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## 4. よくあるエラーと対処

- **DB接続エラー**
  - `db` コンテナが起動しているか確認してください。
  - `docker-compose ps` で `db` のステータスを確認します。

- **フロントがAPIに接続できない**
  - `.env` の `NEXT_PUBLIC_API_BASE` が `http://localhost:8000` になっているか確認してください。
  - 変更後は `docker-compose up --build` を再実行してください。

- **マイグレーション失敗**
  - `db_data` ボリュームを削除して再作成します。
  - `docker-compose down -v` を実行後に再起動してください。

## 5. テスト

```bash
cd backend
pytest
```
