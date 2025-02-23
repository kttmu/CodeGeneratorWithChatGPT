import pandas as pd

# 読み込むExcelファイルのパス
EXCEL_FILE_PATH = "/mnt/data/要求仕様書.xlsx"

def read_specification(file_path):
    """
    Excelファイルを読み込み、要求仕様を取得する
    """
    try:
        df = pd.read_excel(file_path, sheet_name=None)  # すべてのシートを辞書型で取得
    except Exception as e:
        print(f"エラー: {e}")
        return None
    
    extracted_data = {}

    # シートの構造を確認（仮に "機能一覧" というシート名を想定）
    if "機能一覧" in df:
        feature_sheet = df["機能一覧"]
        extracted_data["class_name"] = feature_sheet.iloc[0, 1]  # 例: クラス名
        extracted_data["methods"] = feature_sheet.iloc[1:, 1].dropna().tolist()  # メソッド一覧
        extracted_data["attributes"] = feature_sheet.iloc[1:, 2].dropna().tolist()  # 属性（変数）

    # 追加の情報がある場合は適宜取得
    if "非機能要件" in df:
        extracted_data["non_functional"] = df["非機能要件"].to_dict()

    return extracted_data

def generate_prompt(spec):
    """
    取得した要求仕様をもとにプロンプトを生成する
    """
    class_name = spec.get("class_name", "UnknownClass")
    methods = "\n".join(f"- {m}" for m in spec.get("methods", []))
    attributes = "\n".join(f"- {a}" for a in spec.get("attributes", []))
    
    prompt = f"""
以下の要求仕様に基づき、C++のクラス定義と基本的なメソッドを実装してください。
また、GoogleTestを用いた単体テストコードも生成してください。

## 要求仕様
- クラス名: {class_name}
- メンバ変数:
{attributes}

- メソッド:
{methods}

- 言語: C++
- クラス設計: オブジェクト指向に基づいた適切な設計を行うこと
- テスト: GoogleTestを用いた単体テストを作成すること

## 出力形式
1. `.h` ヘッダーファイル（クラス定義）
2. `.cpp` 実装ファイル
3. `test.cpp` GoogleTestの単体テスト
"""
    return prompt

# 要求仕様を読み込む
spec_data = read_specification(EXCEL_FILE_PATH)

if spec_data:
    prompt_text = generate_prompt(spec_data)
    print("生成されたプロンプト:\n")
    print(prompt_text)
else:
    print("要求仕様書の読み込みに失敗しました。")
