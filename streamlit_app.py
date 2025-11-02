import streamlit as st
import google.generativeai as genai

st.title("💬 Chatbot (Gemini 2.5 Pro)")
st.write(
    "このチャットボットは Google Gemini 2.5 Pro モデルを使って応答を生成します。"
    "APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) から取得できます。"
)

gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するには Gemini API キーを入力してください。", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("メッセージを入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini形式: 単なる文字列リストで渡す
        context = [m["content"] for m in st.session_state.messages]

        # Gemini 2.5 Proから応答を得る
        response = model.generate_content(context)
        answer = (
            response.text if hasattr(response, "text")
            else response.candidates[0].content.parts[0].text
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
