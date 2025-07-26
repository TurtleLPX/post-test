import streamlit as st
import requests

st.title("📝 自動產文請求介面")

with st.form("article_form"):
    title = st.text_input("文章標題", "第一次搬家好迷茫？搬家N大流程全攻略")
    keywords = st.text_input("關鍵字", "搬家,流程,注意事項")
    tone = st.multiselect("語氣風格", ["親切感", "專業性", "資訊豐富", "警示性", "行動導向"])

    submitted = st.form_submit_button("送出產文請求")

if submitted:
    with st.spinner("送出請求中，請稍候..."):
        response = requests.post("https://your-n8n-domain.com/webhook/new-article", json={
            "title": title,
            "keywords": keywords,
            "tone": ", ".join(tone)
        })

    if response.status_code == 200:
        st.success("✅ 產文流程已啟動！")
        result = response.json()
        if "docUrl" in result:
            st.markdown(f"[👉 查看產出文章]({result['docUrl']})")
        else:
            st.write(result)
    else:
        st.error(f"❌ 發送失敗，狀態碼：{response.status_code}")
