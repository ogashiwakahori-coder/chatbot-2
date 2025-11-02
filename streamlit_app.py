import streamlit as st
import google.generativeai as genai
import pdfplumber

st.title("💬 PDF対応チャットボット (Gemini 2.5 Pro)")
st.write(
    "PDFファイルをアップロードして、その内容に関する質問ができます。\n"
    "このチャットボットは Google Gemini 2.5 Pro モデルを使って応答を生成します。\n"
    "APIキーは `.streamlit/secrets.toml` に保存してください。"
)

# シークレットからAPIキーを取得
gemini_api_key = st.secrets.get("gemini", {}).get("api_key", None)

pdf_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

pdf_text = ""
if pdf_file:
    try:
        with pdfplumber.open(pdf_file) as pdf:
            pdf_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        st.success("PDF内容を読み込みました。")
        st.expander("PDF内容表示").write(pdf_text if pdf_text else "テキストが抽出できませんでした。")
    except Exception as e:
        st.error(f"PDFの読み込みエラー: {e}")

if not gemini_api_key:
    st.error("Gemini API キーが設定されていません。 `.streamlit/secrets.toml` に `api_key` をセットしてください。", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("PDF内容に関する質問を入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # コンテキスト: チャット履歴＋PDF内容
        context = [m["content"] for m in st.session_state.messages]
        if pdf_text:
            context.insert(0, f"以下はアップロードされたPDFの内容です:\n{pdf_text}")

        # Gemini 2.5 Proから応答を得る
        response = model.generate_content(context)
        answer = (
            response.text if hasattr(response, "text")
            else response.candidates[0].content.parts[0].text
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
