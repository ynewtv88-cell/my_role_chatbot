# Role-based Creative Chatbot (Claude version)
# Same app as the OpenAI version, powered by Anthropic's Claude API.

import streamlit as st
import anthropic

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(page_title="🎭 Role-based Creative Chatbot", layout="wide")
st.title("🎭 Role-based Creative Chatbot")
st.write("Select a creative role and ask your question!")

# -----------------------
# Sidebar: API Key + Role Selection
# -----------------------
st.sidebar.header("🔑 API & Role Settings")

api_key = st.sidebar.text_input(
    "Enter your Anthropic API Key:",
    type="password",
    placeholder="sk-ant-xxxxxxxx",
)

# Each role is a "system prompt": it tells the AI who it is and how to think.
roles = {
    "🎥 Video Director":
    "You are a professional film director. Always analyze ideas in terms of visual storytelling — use camera movement, lighting, framing, and emotional tone to explain your thoughts. Describe concepts as if you are planning a film scene.",

    "💃 Dance Instructor":
    "You are a dance instructor. Always respond using movement and rhythm metaphors. Translate ideas into body motion, choreography, and stage presence. Think in terms of energy, flow, and physical expression.",

    "👗 Fashion Stylist":
    "You are a fashion stylist. Explain every idea using the language of color, texture, and silhouette. Think visually — how something would appear, feel, and harmonize.",

    "🎭 Acting Coach":
    "You are an acting coach. Speak as if guiding an actor through emotion and timing. Use scene examples, emotional layering, and body language descriptions.",

    "🎨 Art Curator":
    "You are an art curator. Reflect in an analytical yet poetic tone. Compare artistic elements, styles, and their emotional effects as if curating an exhibition.",
}

role_name = st.sidebar.selectbox("Choose a role:", list(roles.keys()))
role_description = roles[role_name]
st.sidebar.info(role_description)

# -----------------------
# User Input Area
# -----------------------
user_input = st.text_area(
    "💬 Enter your question or idea:",
    height=100,
    placeholder="e.g., How can I express sadness in movement?",
)

# -----------------------
# Generate Response
# -----------------------
if st.button("Generate Response"):
    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API key in the sidebar.")
    elif not user_input:
        st.warning("Please enter a question first!")
    else:
        try:
            client = anthropic.Anthropic(api_key=api_key)
            with st.spinner("AI is thinking..."):
                response = client.messages.create(
                    model="claude-haiku-5-5",
                    max_tokens=1024,                 # required by the Claude API
                    system=role_description,         # the role goes in its own field
                    messages=[{"role": "user", "content": user_input}],
                )
                # The reply is a list of content blocks; join the text blocks.
                answer = "".join(b.text for b in response.content if b.type == "text")
                st.success(f"🎬 {role_name} says:")
                st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
