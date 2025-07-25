# app/app.py
import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pbm.pipeline import process_dataframe
from dotenv import load_dotenv
load_dotenv()

# Load custom CSS
with open("app/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="PBM Tag Generator", layout="wide")

st.title("📌 PBM Tag Generator")
st.markdown("Upload your case summary Excel file to auto-generate PBM tags.")

uploaded_file = st.file_uploader("Upload Excel (.xlsx) File", type=["xls"])

if uploaded_file is not None:
    df = pd.read_html(uploaded_file)
    df = df[0]
    st.success("File uploaded successfully!")

    if st.button("🔍 Generate PBM Tags"):
        with st.spinner("Processing..."):
            df_out = process_dataframe(df, use_llm=True)
        
        st.success("✅ PBM Tags Generated!")
        st.dataframe(df_out.head(5), use_container_width=True)

        # Prepare download
        st.markdown("### 📥 Download Output")
        out_file = "pbm_output.xlsx"
        df_out.to_excel(out_file, index=False)
        with open(out_file, "rb") as f:
            st.download_button("Download Excel", f, file_name="pbm_output.xlsx")

else:
    st.info("Awaiting Excel file upload.")


