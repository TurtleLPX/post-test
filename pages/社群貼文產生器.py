import streamlit as st
import requests
from utils.ui import inject_css

inject_css()
PRIMARY = "#ab452b"

st.markdown(f"# <span style='color:{PRIMARY}'>社群貼文產生器</span>", unsafe_allow_html=True)
st.markdown("### 🧩 填寫貼文需求")

with st.form("post_form"):
    st.text_input("📌 品牌名稱", "超便宜搬家", key="brand")
    st.selectbox("🌐 發文平台", ["Facebook", "Instagram", "Threads", "LINE VOOM"], key="platform")
    st.selectbox("🎭 小編角色", ["小編A", "小編B", "小編C"], key="editor")
    st.text_input("🎯 貼文主題", "開學季學生搬家優惠", key="topic")
    st.text_area("🖼️ 素材內容描述（例如圖片內容、現場畫面）", "學生背著行李走進宿舍的畫面，臉上帶著笑容", key="material")

    submitted = st.form_submit_button("🚀 產生貼文")

if submitted:
    st.markdown("### ✨ 貼文產出結果")

    payload = {
        "brand": st.session_state["brand"],
        "platform": st.session_state["platform"],
        "editor": st.session_state["editor"],
        "post_topic": st.session_state["topic"],
        "post_material": st.session_state["material"]
    }

    try:
        res = requests.post(
            "https://turtlelu.zeabur.app/webhook-test/generate-socialpost",
            json=payload,
            timeout=30
        )
        res.raise_for_status()
        result = res.json()
        post = result.get("post", "⚠️ 沒有收到貼文內容")

        # ✅ 顯示在 text_area（有換行）
        st.markdown("#### 📋 點右上角複製貼文")
        st.code(post, language="markdown")

        # ✅ 複製用文字處理：escape ` 和 \ 為 JS 可接受格式
        escaped_post = post.replace("\\", "\\\\").replace("`", "\\`").replace("\n", "\\n")


        with st.expander("📤 儲存資訊（將來串接 Google Sheets）"):
            st.markdown(f"""
- 品牌名稱：**{payload["brand"]}**  
- 平台：**{payload["platform"]}**  
- 小編角色：**{payload["editor"]}**  
- 主題：**{payload["post_topic"]}**  
- 素材描述：{payload["post_material"]}
            """)

    except Exception as e:
        st.error(f"❌ 請求失敗：{e}")
