import streamlit as st
from utils.ui import inject_css

inject_css()

st.markdown("## 📣 社群貼文產生器")

with st.form("post_form"):
    brand = st.text_input("品牌名稱", "台大搬家公司")
    product = st.text_input("服務/產品特色", "學生搬家快速又便宜")
    platform = st.selectbox("平台", ["Facebook", "Instagram", "Threads", "LINE VOOM"])
    tone = st.selectbox("語氣", ["活潑", "專業", "親切", "幽默"])
    submit = st.form_submit_button("🚀 產生貼文")

if submit:
    st.markdown("### ✨ AI 產出貼文：")
    st.success(f"{brand} 專屬 {platform} 貼文：\n\n{product}，立即體驗！ ({tone} 語氣)")
