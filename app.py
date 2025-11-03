from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

def get_llm_response(input_text, selected_expert):
    """
    入力テキストと選択された専門家の種類を基に、LLMからの回答を取得する関数。

    Args:
        input_text (str): ユーザーからの入力テキスト。
        selected_expert (str): 選択された専門家の種類。

    Returns:
        str: LLMからの回答。
    """
    system_template = "あなたは、{genre}に詳しいAIです。ユーザーからの質問に100文字以内で回答してください。"
    human_template = "{question}"

    genre = "メジャーリーグの野球解説者" if selected_expert == "メジャーリーグの野球解説者" else "教育カウンセラー"

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template),
    ])

    messages = prompt.format_prompt(genre=genre, question=input_text).to_messages()

    llm = ChatOpenAI(temperature=0)
    response = llm.invoke(messages)

    return response.content

st.title("専門家の種類を選択できるチャットボットアプリ")

st.write("##### 動作モード1: メジャーリーグの野球解説者")
st.write("メジャーリーグの試合に関する質問に答えます。例えば、選手の成績やチームの歴史について質問できます。")
st.write("##### 動作モード2: 教育カウンセラー")
st.write("教育に関する質問に答えます。例えば、進路相談や学習方法について質問できます。")


selected_item = st.radio(
    "動作モードを選択してください。",
    ["メジャーリーグの野球解説者", "教育カウンセラー"]
)

input_message = st.text_input(label="質問を入力してください。")

if st.button("実行"):
    if input_message:
        try:
            response = get_llm_response(input_message, selected_item)
            st.write(f"回答: {response}")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.error("質問を入力してください。")