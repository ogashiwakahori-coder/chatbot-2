import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot (Gemini 2.5 Pro)")
st.write(
    "このチャットボットは Google Gemini 2.5 Pro モデルを使って応答を生成します。"
    "ご利用には Google AI Studio から取得できる API キーが必要です。"
    "APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) から取得できます。"
)

# Ask user for their Gemini API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するには Gemini API キーを入力してください。", icon="🗝️")
else:
    # Configure Gemini client
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("メッセージを入力してください"):
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare context for Gemini (convert to prompt format)
        context = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                context.append({"role": "user", "parts": [m["content"]]})
            elif m["role"] == "assistant":
                context.append({"role": "model", "parts": [m["content"]]})

        # Generate response from Gemini 2.5 Pro
        response = model.generate_content(context)
        answer = response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text

        # Display and store assistant response
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
