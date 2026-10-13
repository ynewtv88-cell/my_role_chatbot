import streamlit as st
import anthropic
from openai import OpenAI

# 1. 페이지 제목 설정
st.set_page_config(page_title="🎭 역할 기반 AI 챗봇", layout="wide")
st.title("🎭 역할 기반 AI 챗봇")
st.caption("Arts and Advanced Big Data | Role-based Chatbot")

# 2. 역할(페르소나) 정의
ROLES = {
    "🎥 Video Director": "You are a professional film director. Always analyze ideas in terms of visual storytelling: use camera movement, lighting, framing, and emotional tone.",
    "💃 Dance Instructor": "You are a dance instructor. Always respond using movement and rhythm metaphors. Translate ideas into body motion, choreography, and stage presence.",
    "👗 Fashion Stylist": "You are a fashion stylist. Explain every idea using the language of color, texture, and silhouette. Think visually: how something would appear, feel, and harmonize.",
    "🎭 Acting Coach": "You are an acting coach. Speak as if guiding an actor through emotion and timing. Use scene examples, emotional layering, and body language descriptions.",
    "🎨 Art Curator": "You are an art curator. Reflect in an analytical yet poetic tone. Compare artistic elements, styles, and their emotional effects as if curating an exhibition.",
    "✍️ Custom role (직접 적기)": "",
}

MODELS = {
    "OpenAI": ["gpt-4o-mini"],
    "Claude": ["claude-haiku-5-5", "claude-sonnet-5-5"],
}

# 3. 사이드바 설정
st.sidebar.header("⚙️ Settings")
provider = st.sidebar.radio("AI Provider 선택", ["OpenAI", "Claude"])
api_key = st.sidebar.text_input(
    f"{provider} API Key 입력:",
    type="password",
    placeholder="sk-..."
)
model = st.sidebar.selectbox("Model 선택", MODELS[provider])

role_name = st.sidebar.selectbox("역할(Role) 선택", list(ROLES.keys()))
if role_name.startswith("✍️"):
    role_text = st.sidebar.text_area("AI에게 줄 역할을 직접 써보세요:", "You are a poet who explains everything through the seasons.")
else:
    role_text = ROLES[role_name]
    st.sidebar.info(role_text)

language = st.sidebar.selectbox("답변 언어", ["Same as my question", "English", "한국어"])

if st.sidebar.button("🗑️ 대화 내역 삭제"):
    st.session_state.messages = []

# 4. 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 질문 및 답변
question = st.chat_input("질문을 입력하세요...")
if question:
    if not api_key:
        st.warning("왼쪽 사이드바에 API Key를 먼저 입력해주세요!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    system_prompt = role_text
    if language == "한국어":
        system_prompt += " Always answer in Korean."
    elif language == "English":
        system_prompt += " Always answer in English."

    with st.chat_message("assistant"):
        try:
            if provider == "OpenAI":
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                )
                answer = response.choices[0].message.content
            else:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model=model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=st.session_state.messages,
                )
                answer = "".join(b.text for b in response.content if b.type == "text")

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
