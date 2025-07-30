import streamlit as st
import requests
import time

# 💄 設定頁面與主題配色
st.set_page_config(page_title="品牌專屬 AI 機器人", layout="wide")

# 🎨 主題顏色
PRIMARY = "#ab452b"
ACCENT = "#d4c7b9"
BG = "#e9e6e2"
TEXT_DARK = "#2f2f2f"
BG_LIGHT = "#fefbf7"

# 🧽 自訂 CSS
st.markdown(f"""
    <style>
        body {{
            background-color: {BG};
            color: {TEXT_DARK};
        }}
        .stFormSubmitButton > button {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            width: 15%;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        .stButton > button,
        div.row-widget.stButton {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            width: 70%;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        .stButton > button:hover,
        div.row-widget.stButton,
        .stFormSubmitButton > button:hover {{
            background-color: #93361f;
        }}
        .stTextInput > div > div > input,
        .stTextArea textarea {{
            background-color: {BG_LIGHT};
            border: 1px solid {ACCENT};
        }}
        .stTextArea textarea {{
            font-family: 'Courier New', monospace;
        }}
        .stMarkdown h3 {{
            color: {PRIMARY};
            margin-top: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"# <span style='color:{PRIMARY}'>品牌專屬 AI 機器人</span>", unsafe_allow_html=True)

# Webhook URLs
N8N_BASE_URL = "https://turtlelu.zeabur.app/webhook-test"
GENERATE_URL = f"{N8N_BASE_URL}/generate-draft"
REWRITE_URL = f"{N8N_BASE_URL}/ai-rewrite"
SAVE_URL = f"{N8N_BASE_URL}/save-doc"

# Session state
st.session_state.setdefault("article_draft", "")
st.session_state.setdefault("doc_url", "")

# ──────────────
# 步驟 1：輸入需求
# ──────────────
st.markdown("### 👣 步驟 1：填寫文章需求")

with st.form("article_form"):
    keywords = st.text_input("🔑 目標關鍵字", "學生搬家、學生搬家費用")
    title = st.text_input("📌 建議標題", "學生搬家要注意什麼？搬家費用如何計算？")
    outline = st.text_area("📝 文章大綱", """學生搬家須注意事項(例如：找有合法執照的搬家公司、找免費詢價報價服務、易碎品須標示清楚)
學生搬家費用如何計算？(說明會影響費用的因素，如：搬家距離、是否需要打包等)
學生搬家省錢技巧(例如：蒐集免費紙箱、盡量減少搬運體積、找同學併車搬運)
介紹超便宜搬家學生搬家服務，並附上聯繫資訊 (附上地址、官網／FB／Google 商家連結、Line/電話聯繫方式)""")
    generate = st.form_submit_button("產生草稿")

if generate:
    status_placeholder = st.empty()
    status_placeholder.info("✍️ AI 正在撰寫草稿中...")

    time.sleep(20)  # 前 20 秒提示為草稿中
    status_placeholder.info("🤖 AI 正在潤稿中...")

    try:
        res = requests.post(GENERATE_URL, json={
            "title": title,
            "keywords": keywords,
            "outline": outline
        })
        res.raise_for_status()
        data = res.json()
        content = data.get("content", "")
        st.session_state["article_draft"] = content
        status_placeholder.success("✅ 草稿產出成功！")
    except Exception as e:
        status_placeholder.error(f"❌ 草稿產出失敗：{e}")

# ──────────────
# 步驟 2：預覽草稿 + AI 助理 + 儲存（合併並美化）
# ──────────────
if st.session_state["article_draft"]:
    st.markdown("### 👣 步驟 2：預覽草稿、請 AI 協助修改，或直接儲存")

    edited_text = st.text_area(
        "✏️ 草稿內容（可修改，H1 為文章標題）",
        value=st.session_state["article_draft"],
        height=400,
        label_visibility="visible"
    )

    ai_prompt = st.text_input("🤖 想請 AI 協助什麼？（如：加強結尾、轉換語氣）")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔁 請 AI 協助重寫", key="rewrite_button", use_container_width=True):
            with st.spinner("🤖 AI 助理潤稿中..."):
                try:
                    ai_res = requests.post(REWRITE_URL, json={
                        "draft": edited_text,
                        "instruction": ai_prompt
                    })
                    ai_res.raise_for_status()
                    result = ai_res.json()
                    updated = result.get("updated_text", "")

                    if updated:
                        st.session_state["article_draft"] = updated
                        st.success("✅ AI 已優化內容！")
                    else:
                        st.warning("⚠️ 沒收到 AI 回傳內容，請確認")
                except Exception as e:
                    st.error(f"❌ AI 修改失敗：{e}")
                    st.text(ai_res.text)

    with col2:
        if st.button("✅ 儲存並上傳至 Google Docs", key="save_button", use_container_width=True):
            with st.spinner("📤 正在儲存中..."):
                try:
                    save_res = requests.post(SAVE_URL, json={ "markdown": edited_text })
                    save_res.raise_for_status()

                    # ✅ 正確解析 webhook 回傳的 JSON 格式
                    result = save_res.json()  # 必須放第一行

                    # ✅ 解析出網址與文件名
                    doc_url = result.get("docUrl", "").strip()
                    doc_name = result.get("docName", "").strip()

                    # ✅ 儲存至 session state
                    st.session_state["doc_url"] = doc_url
                    st.session_state["doc_name"] = doc_name
                    st.session_state["doc_saved"] = True

                except Exception as e:
                    st.error(f"❌ 儲存失敗：{e}")
                    if save_res is not None:
                        st.text(save_res.text)

    # ✅ 成功後顯示卡片（移到區塊外，不會遮住按鈕）
    if st.session_state.get("doc_saved"):
        st.markdown(f"""
        <div style="background-color:#f0f8f3; border-left: 6px solid #34a853; padding: 1rem; border-radius: 6px; margin-top: 1.5rem;">
            <p style="margin:0;">📄 <strong>文件已建立成功：</strong> {st.session_state.get("doc_name", "")}</p>
            <p style="margin:0;">👉 <a href="{st.session_state.get("doc_url", "#")}" target="_blank" style="color:#2b6cb0;font-weight:bold;">點我查看 Google 文件</a></p>
        </div>
        """, unsafe_allow_html=True)
