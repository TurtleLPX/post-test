import streamlit as st

# 主題色
PRIMARY = "#ab452b"
ACCENT = "#d4c7b9"
BG = "#e9e6e2"
TEXT_DARK = "#2f2f2f"
BG_LIGHT = "#fefbf7"

st.set_page_config(
    page_title="品牌專屬 AI 工具箱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown(f"""
    <style>
        body {{
            background-color: {BG};
            color: {TEXT_DARK};
        }}
        .dashboard-card {{
            background-color: {BG_LIGHT};
            border: 1px solid {ACCENT};
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            transition: 0.2s;
            cursor: pointer;
            text-decoration: none;
        }}
        .dashboard-card:hover {{
            transform: scale(1.02);
            border-color: {PRIMARY};
        }}
        .dashboard-title {{
            color: {PRIMARY};
            font-size: 1.4rem;
            margin-bottom: 0.5rem;
        }}
        .dashboard-desc {{
            font-size: 1rem;
            color: {TEXT_DARK};
        }}
        a, .dashboard-desc a {{
            text-decoration: none !important;
            color: inherit !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"# 🧠 <span style='color:{PRIMARY}'>品牌專屬 AI 工具箱</span>", unsafe_allow_html=True)
st.markdown("選擇一項功能開始使用：")

# 卡片區
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <a href="/SEO文章產生器" target="_self">
        <div class="dashboard-card">
            <div class="dashboard-title">📄 SEO文章產生器</div>
            <div class="dashboard-desc">
                幫你自動生成部落格或教學文草稿，結合關鍵字、品牌語氣、SEO架構與自動上傳 Google Docs。
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <a href="/社群貼文產生器" target="_self">
        <div class="dashboard-card">
            <div class="dashboard-title">📣 社群貼文產生器</div>
            <div class="dashboard-desc">
                根據品牌語氣與行銷目標，快速產出 Facebook／Instagram／LINE 等文案。
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)
