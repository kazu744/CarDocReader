# CarDoc Reader
自動車の登録手続きに必要な書類をGoogle Cloud Vision APIのOCR機能で読み取り、OpenAIのAPIを使って形式を整えて、エクセルにダウンロードできるWebアプリケーションです。

## サービスのURL
https://cardocreader.com/login<br>

下記の情報でログインしてご利用いただけます。<br>
test1@example.com<br>
Test1234<br>

## 開発理由
私は現在、自動車の登録を専門とする行政書士事務所に事務員として勤務しています。<br>
お客様から預かった紙の書類を見て、データをパソコンに打ち込むという作業を日々行っていますが、とても非効率だと感じていました。<br>
そこで、このツールを使うことで大幅に作業時間の短縮、また会社が力を入れているDX化にも貢献ができると思いこのWebアプリを作成しました。<br> 
今後は申請書類の印刷や請求書作成など一元管理できるツールにしていきたいと考えています。<br>

## 使用技術
Category | Technology Stack
-|-
バックエンド | Python, Flask
フロントエンド | HTML, CSS, JavaScript
データベース | MySQL
環境構築 | Docker
インフラ | AWS
API | OpenAI, Google Cloud Vision
etc. | Git, Github

## ER図
```mermaid

erDiagram
    users ||--o{ ocrs : ""

users {
    int id PK "ID"
    varchar(255) email "メールアドレス"
    varchar(255) password_hash "パスワード"
    text vision_api "Google Cloud Vision APIキー"
    text openai_api "OpenAI APIキー"
    dtetime created_at "作成日時"
    datetime update_at "更新日時"
    datetime deleted_at "削除日時"
}

ocrs {
    int id PK "ID"
    int user_id FK "ユーザーID"
    varchar(255) new_owner_name "新所有者氏名"
    varchar(255) new_owner_address_main "新所有者住所"
    int new_owner_address_street "新所有者丁目"
    varchar(255) new_owner_address_number "新所有者番地"
    datetime created_at "作成日時"
    datetime update_at "更新日時"
    datetime deleted_at "削除日時"
}
```


## 機能一覧
- ログイン
- アカウント新規作成
- 書類アップロード&OCR
- OCR一覧
- OCR編集
- アカウント編集

## 今後の展望
- フロントエンドの充実<br>
  必要最低限しか実装していないので、より使いやすいUIを目指す。
- CI/CDを導入<br>
- OCRできる書類の追加<br>
  現在は印鑑証明しかできませんが、車検証や車庫証明などもOCRできるようにする
