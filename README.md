# s3-download-file

## 概要

サンプルコードを使用し、S3バケットに保管してあるファイルをS3 presigned URLでダウンロードする方法についてご紹介します。

## 前提

次のものが動作する環境が必要です。

1. AWS CLI
1. AWS SAM CLI
1. Docker Desktop
1. WSL2(Windowsの場合)

## 構築方法

### ソースコードを取得

1. ソースコードを取得します。

    ```shell
    git clone https://github.com/cm-fujikawa/s3-download-file.git
    ```

### ビルド&デプロイ

1. バケット名をユニークにするため、パラメータストアを作成し、任意の文字列を格納しておきます。

    ```shell
    aws ssm put-parameter --name S3DownloadFileSuffix --value `date "+%Y%m%d%H%M%S"` --type String --profile HOGEHOGE
    ```

2. ビルドして、AWSにデプロイします。ローカルにPython環境を構築しなくても済むように、ここでは、ローカルのコンテナ環境でビルドしています。

    ```shell
    cd s3-download-file
    sam build --use-container
    sam deploy --guided --stack-name s3-download-file --region ap-northeast-1 --profile HOGEHOGE
    ```

### コードを書き換え

コードを2ヶ所書き換えます。
`sam deploy`コマンドの実行結果の末尾に表示される`ListPy`、`ListHtml`の値を控えておきます。

#### Lambda関数

1. `AWSマネジメントコンソール`で`CloudFormation`を開き、`s3-download-file`スタックを開きます。
1. `リソース`タブを開きます。
1. `論理ID`が`ListFunction`という名称のLambda関数を開きます。
1. `コードソース`で`list.py`ファイルをダブルクリックします。
1. `XXXXXXXXXX`を`ListPy`の値に書き換えます。

    ```python
    S3DownloadFileApi = 'XXXXXXXXXX'
    ```

1. `Deploy`ボタンをクリックします。

#### HTMLファイル

1. ローカルで`contents`フォルダにある`list.html`ファイルを開きます。
1. `XXXXXXXXXX`を`ListHtml`の値に書き換えます。

### 静的コンテンツをアップロード

#### HTMLファイル

1. `s3-list-files-bucket-XXXXXXXX`バケットを開きます。
1. `contents`フォルダの階層ごと(`contents`フォルダと`list.html`ファイル)をコピーします。

#### ダウンロードファイル

1. `s3-download-file-bucket-XXXXXXXX`バケットを開きます。
1. ダウンロードさせたいファイルをアップロードします。

## 使用方法

1. `sam deploy`コマンドの実行結果の末尾に表示される`AccessUrl`にアクセスします。
1. `AccessUrl`は、次のようなURLです。`${S3BucketName}`には`s3-list-files-bucket-XXXXXXXX`バケット名です。

    ```text
    https://${S3BucketName}.s3-ap-northeast-1.amazonaws.com/contents/list.html
    ```

1. `s3-download-file-bucket-XXXXXXXX`バケットにあるファイルが一覧表示されます。
1. 適当なリンクをクリックします。
1. ファイルがダウンロードされます。

## スタック削除

1. S3バケット内にあるすべてのファイルを削除します。
1. S3バケット名の末尾の文字列を確認します。

    ```shell
    export S3DownloadFileSuffix=`aws ssm get-parameter --name S3DownloadFileSuffix --profile HOGEHOGE \
        | jq -r '.Parameter.Value'`
    echo $S3DownloadFileSuffix
    ```

1. S3バケットを削除します。

    ```shell
    aws s3 rb s3://s3-download-file-bucket-$S3DownloadFileSuffix --force --profile HOGEHOGE
    aws s3 rb s3://s3-list-files-bucket-$S3DownloadFileSuffix --force --profile HOGEHOGE
    ```

1. 次のコマンドでスタックを削除します。

    ```shell
    aws cloudformation delete-stack --stack-name s3-download-file --profile HOGEHOGE
    ```

## 注意

HTML、API Gatewayには認証が掛かっていないため、ここで作成したS3バケットに誰でもアクセスできてしまいます。
