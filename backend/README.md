# 実行する前に

## Backend

- 最新版のPythonをインストール

- 環境設定

```bash
cd backend
# Pipenvをインストール
pip install --user pipenv

#Pipenvでライブラリをインストール
pipenv install

# env copy
cp .env.example .env
```

# 実行

- Backend
    - まずはディレクトリーを変える
        - `cd backend`
    - ローカルで実行したい場合
        - `docker compose up -d api_db #データベースを起動`
        - ` export FLASK_APP=app && export FLASK_ENV=development && pipenv run python -m flask run`
    - dockerで実行したい場合
        - `docker compose up -d`

