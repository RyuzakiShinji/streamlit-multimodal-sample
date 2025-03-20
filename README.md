# Streamlit マルチモーダルチャットアプリケーション

*[English](README_en.md) | [日本語](README.md)*

このリポジトリは、Streamlitの`chat_input()`機能を使ったマルチモーダル対応チャットアプリケーションのサンプルです。Streamlitのチャットインターフェイス機能のアップデートについて解説する技術ブログの参照用として作成しました。

## 概要

本アプリケーションは、Streamlitで構築されたモダンなチャットインターフェイスで、テキストと画像の両方を入力できる機能を備えています。OpenAIのGPTモデルを活用し、会話の履歴やアップロードされた画像に基づいて応答を生成します。

特に注目すべき点は、Streamlitの`chat_input()`関数の最新アップデートにより、チャットインターフェイス内で直接ファイルをアップロードできるようになり、よりシームレスなマルチモーダル体験が実現できるようになったことです。

## 主な機能

- **マルチモーダル入力**: 1つのチャット入力フィールドでテキストと画像の両方を扱えます
- **画像アップロード機能**: チャットインターフェイスから直接画像をアップロードできます
- **会話履歴の管理**: 自然な会話UIで履歴を保持・表示します
- **OpenAI連携**: OpenAIのモデルを使って文脈に沿った応答を生成します
- **トークン管理**: モデルの制限内で効率的にトークン使用量を管理します
- **セッション管理**: ユーザーの操作間でチャットの状態を維持します

## インストール方法

このプロジェクトは依存関係の管理にPoetryを使用しています。

1. リポジトリをクローンします：
   ```bash
   git clone https://github.com/yourusername/streamlit-multimodal-sample.git
   cd streamlit-multimodal-sample
   ```

2. Poetryで依存パッケージをインストールします：
   ```bash
   poetry install
   ```

3. 仮想環境を有効化します：
   ```bash
   poetry shell
   ```

## 使い方

1. Streamlitアプリを起動します：
   ```bash
   streamlit run app.py
   ```

2. ブラウザで `http://localhost:8501` にアクセスします

3. 画面下部のチャット入力欄にメッセージを入力できます

4. 画像をアップロードする場合は、チャット入力欄横のファイルアップロードボタンをクリックして画像を選択します（対応形式：jpg、jpeg、png）

## 設定

- アップロード可能なファイルサイズは`.streamlit/config.toml`で5MBに設定されています
- デフォルトでは`gpt-4o-mini`モデルを使用していますが、コード内で変更可能です

## 主要コンポーネント

- `OpenAIClient`: OpenAI APIとの通信を担当
- `SessionManager`: アプリのセッション状態とチャット履歴を管理
- `TokenManager`: トークン数のカウントと制限付きメッセージの整形を処理
- `MessageProcessor`: OpenAI API用のメッセージを処理
- `InputHandler`: ファイルアップロードを含むユーザー入力を処理
- `ChatUI`: Streamlitのユーザーインターフェイスコンポーネントを管理

## 動作環境

- Python 3.12以上
- Streamlit 1.43.2以上
- OpenAI APIへのアクセス権
- その他の依存パッケージはpyproject.tomlを参照

## OpenAI APIキーの設定

このアプリケーションを使用するには、OpenAI APIキーが必要です。以下の手順で設定できます：

1. プロジェクトのルートディレクトリに`.env`ファイルを作成
2. 以下の形式でAPIキーを追加：`OPENAI_API_KEY=your_api_key_here`

## 使用技術

- [Streamlit](https://streamlit.io/): Webインターフェイス構築
- [OpenAI API](https://openai.com/): テキスト生成
- [tiktoken](https://github.com/openai/tiktoken): トークン化処理
- [Poetry](https://python-poetry.org/): 依存関係の管理

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。

```
MIT License

Copyright (c) 2025 RyuzakiShinji

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*このリポジトリは技術ブログ記事の参照用であり、コントリビューションは受け付けていません。*
