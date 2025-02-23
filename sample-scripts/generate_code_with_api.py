import openai

# OpenAI APIキーの設定（実際のキーに置き換えてください）
API_KEY = "your-api-key"

# ChatGPTに送信するプロンプト
prompt = """
以下の要求仕様に基づき、C++のクラス定義と基本的なメソッドを実装してください。
また、GoogleTestを用いた単体テストコードも生成してください。

## 要求仕様
- クラス名: TemperatureSensor
- 機能:
  - センサーから温度を取得する `getTemperature()` メソッド
  - 現在の温度を保存する `currentTemperature` メンバ変数
  - 温度が一定の閾値を超えた場合に警告を出す `isOverThreshold()` メソッド
- 初期化時にしきい値（`threshold`）を設定する
- 言語: C++
- クラス設計: オブジェクト指向に基づいた適切な設計を行うこと
- テスト: GoogleTestを用いた単体テストを作成すること

## 出力形式
1. `.h` ヘッダーファイル（クラス定義）
2. `.cpp` 実装ファイル
3. `test.cpp` GoogleTestの単体テスト
"""

def generate_code(prompt):
    """ChatGPT APIを利用してコードを生成する"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 最新のモデルを指定
        messages=[{"role": "system", "content": "You are a helpful coding assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.2  # 生成のばらつきを抑える
    )
    return response["choices"][0]["message"]["content"]

# 生成されたコードを取得
generated_code = generate_code(prompt)

# 結果をファイルに保存
with open("generated_code.cpp", "w", encoding="utf-8") as f:
    f.write(generated_code)

print("C++コードを生成し、generated_code.cpp に保存しました。")
