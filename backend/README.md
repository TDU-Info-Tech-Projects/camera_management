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
        - DBを立ち上げる
            - `docker compose up api_db -d`
        - pgadminを立ち上げる (pgAdminは実行に必要ないがDBの中身を見たい時は便利！)
            - `docker compose up pgadmin -d` 
        - DBを初期化 (最初だけ実行、その後は実行しない)
            - `docker compose run --rm api /bin/sh -c "pipenv install --system && python -m database.models` 
        - APIを立ち上げる
            - `docker compose up api`

