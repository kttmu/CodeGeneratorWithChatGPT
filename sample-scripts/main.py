import openai
import pandas as pd

# Excelの要求仕様書を読み込む
def read_specification(file_path):
    df = pd.read_excel(file_path, sheet_name=None)
    return df

# 生成AI向けのプロンプトを作成
def generate_prompt(spec_data):
    prompt = """
    以下の要求仕様に基づいて、MISRA C++準拠のC++クラスとGoogleTestのテストコードを生成してください。
    
    【要求仕様】
    """
    for sheet_name, df in spec_data.items():
        prompt += f"\n### {sheet_name} ###\n"
        prompt += df.to_string(index=False) + "\n"
    
    prompt += """
    【出力形式】
    - C++クラス定義（.h, .cpp）
    - GoogleTestによる単体テストコード
    """
    
    return prompt

# ChatGPT APIを使用してコードを生成
def execute_prompt(prompt, api_key):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        api_key=api_key
    )
    return response["choices"][0]["message"]["content"]

# メイン処理
def main():
    file_path = "要求仕様書.xlsx"
    api_key = "your-api-key-here"  # OpenAI APIキーを設定
    
    spec_data = read_specification(file_path)
    prompt = generate_prompt(spec_data)
    output = execute_prompt(prompt, api_key)
    
    with open("generated_code.cpp", "w", encoding="utf-8") as f:
        f.write(output)
    
    print("コード生成が完了しました。'generated_code.cpp' を確認してください。")

if __name__ == "__main__":
    main()
