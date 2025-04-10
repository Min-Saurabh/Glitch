import streamlit as st
from main import get_llm, get_agent_executor, CodeResponse, save_code_to_file
import json

st.set_page_config(page_title="🚀 Modern AI Code Generator", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .big-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .footer {
            margin-top: 2rem;
            font-size: 0.85rem;
            text-align: center;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="big-title">🚀 AI Code Generator</div>', unsafe_allow_html=True)
st.markdown("#### Generate clean, functional code using powerful AI. Just describe what you want!")

# Session state init
if "code_count" not in st.session_state:
    st.session_state.code_count = 0
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# Input
query = st.text_area("📝 Your prompt", placeholder="e.g. Write a Python script that greets the user 👋", height=150)

# Show free usage info
if st.session_state.code_count < 3:
    st.info(f"🎉 You have {3 - st.session_state.code_count} free generations left.")
elif not st.session_state.user_api_key:
    st.warning("⚠️ Free limit reached. Please provide your own Gemini API key to continue.")
    st.session_state.user_api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

generate = st.button("⚡ Generate Code")

# Main logic
if generate:
    if not query.strip():
        st.warning("⛔ Please enter a prompt before generating.")
    elif st.session_state.code_count >= 3 and not st.session_state.user_api_key:
        st.error("❌ API key required to continue.")
    else:
        with st.spinner("Generating code..."):
            try:
                llm = get_llm(st.session_state.user_api_key)
                agent_executor = get_agent_executor(llm)
                raw_response = agent_executor.invoke({"query": query})
                output = raw_response["output"].strip()

                if output.startswith("```json"):
                    output = output.replace("```json", "").replace("```", "").strip()

                json_data = json.loads(output)
                response = CodeResponse(**json_data)

                st.success("✅ Code generated successfully!")
                st.markdown("### 🧠 Generated Code")
                st.code(response.code, language=response.language)

                filename = f"{response.filename or 'generated_code'}.{response.language}"
                st.download_button("⬇️ Download Code", response.code, file_name=filename, mime="text/plain")

                st.info(save_code_to_file(response.code, response.language, response.filename))
                st.session_state.code_count += 1

            except Exception as e:
                st.error("❌ Something went wrong while parsing or generating the response.")
                st.text_area("⚠️ Raw Output (for debugging)", output if 'output' in locals() else "")
                st.exception(e)

# Footer
st.markdown('<div class="footer">💡 Tip: You can describe code in natural language — the AI does the rest!</div>', unsafe_allow_html=True)
