import streamlit as st
from main import agent_executor, CodeResponse, save_code_to_file
import json

st.set_page_config(page_title="🚀 Modern AI Code Generator", layout="centered")

# Custom CSS for styling
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

# Input Section
with st.container():
    query = st.text_area("📝 Your prompt", placeholder="e.g. Write a Python script that greets the user 👋", height=150)
    generate = st.button("⚡ Generate Code")

# Output Section
if generate:
    if query.strip():
        with st.spinner("Generating code..."):
            try:
                raw_response = agent_executor.invoke({"query": query})
                output = raw_response["output"].strip()

                if output.startswith("```json"):
                    output = output.replace("```json", "").replace("```", "").strip()

                json_data = json.loads(output)
                response = CodeResponse(**json_data)

                st.success("✅ Code generated successfully!")

                # Code Display
                st.markdown("### 🧠 Generated Code")
                st.code(response.code, language=response.language)

                # Save and download
                saved_file = save_code_to_file(
                    response.code, response.language, response.filename
                )

                filename = f"{response.filename or 'generated_code'}.{response.language}"
                st.download_button("⬇️ Download Code", response.code, file_name=filename, mime="text/plain")

                st.info(saved_file)

            except Exception as e:
                st.error("❌ Something went wrong while parsing or generating the response.")
                st.text_area("⚠️ Raw Output (for debugging)", output if 'output' in locals() else "")
                st.exception(e)
    else:
        st.warning("⛔ Please enter a prompt before generating.")

# Footer
st.markdown('<div class="footer">💡 Tip: You can describe code in natural language — the AI does the rest!</div>', unsafe_allow_html=True)
