# run.py
import pandas as pd
from pbm.pipeline import process_dataframe
from dotenv import load_dotenv; 

load_dotenv()

INPUT_PATH = "data/input_data.xlsx"
OUTPUT_PATH = "data/cases_output_with_pbm.xlsx"

def main():
    df = pd.read_html(INPUT_PATH)
    df = df[0]
    df_out = process_dataframe(df, use_llm=True)  # set False for rule-only
    df_out.to_excel(OUTPUT_PATH, index=False)
    print(f"Saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
