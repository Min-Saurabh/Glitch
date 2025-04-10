import streamlit as st
from main import get_llm, get_agent_executor, CodeResponse, save_code_to_file
import json

st.set_page_config(
    page_title="🚀 Modern AI Code Generator",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with emoji support and better spacing
st.markdown("""
    <style>
        .big-title {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            background: linear-gradient(45deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem !important;
        }
        .subheader {
            font-size: 1.1rem !important;
            text-align: center;
            color: #6B7280 !important;
            margin-bottom: 2rem !important;
        }
        .stTextArea textarea {
            min-height: 150px !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }
        .stButton button {
            width: 100%;
            background: linear-gradient(45deg, #4F46E5, #06B6D4) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 0.75rem !important;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }
        .footer {
            margin-top: 3rem;
            font-size: 0.9rem;
            text-align: center;
            color: #9CA3AF !important;
            padding-top: 1rem;
            border-top: 1px solid #E5E7EB;
        }
        .stDownloadButton button {
            background: linear-gradient(45deg, #10B981, #06B6D4) !important;
        }
        .stAlert {
            border-radius: 10px !important;
        }
        .code-block {
            border-radius: 10px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="big-title">Glitch Early-Build</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Describe your code in plain English and let AI do the magic ✨</div>', unsafe_allow_html=True)

# Session state init
if "code_count" not in st.session_state:
    st.session_state.code_count = 0
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# Main content container
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Input area with emoji and better placeholder
        query = st.text_area(
            "**Describe your code** ✍️", 
            placeholder="""Example: 
- Create a Python function that calculates Fibonacci sequence
- Build a React component for a todo list with checkboxes
- Make a SQL query to find customers with most orders""", 
            height=180,
            help="Be as specific as possible for better results"
        )
    
    with col2:
        # API key section
        if st.session_state.code_count >= 3:
            st.markdown("### 🔑 API Key")
            st.session_state.user_api_key = st.text_input(
                "Enter your Gemini API Key", 
                type="password",
                label_visibility="collapsed",
                placeholder="sk-xxxxxxxxxxxxxxxx"
            )
            st.markdown("*Required after 3 free uses*", help="Get your API key from Google AI Studio")

# Features grid below input
st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0;">
        <div style="background: #F9FAFB; padding: 1rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 1.5rem;">📋</div>
            <div style="font-weight: 600;">Multiple Languages</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Python, JavaScript, Java, C++ & more</div>
        </div>
        <div style="background: #F9FAFB; padding: 1rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 1.5rem;">🧠</div>
            <div style="font-weight: 600;">Smart AI</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Understands complex requirements</div>
        </div>
        <div style="background: #F9FAFB; padding: 1rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 1.5rem;">⚡</div>
            <div style="font-weight: 600;">Fast Results</div>
            <div style="font-size: 0.8rem; color: #6B7280;">Generates code in seconds</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Generate button with conditional rendering
if st.session_state.code_count < 3 or st.session_state.user_api_key:
    generate = st.button("✨ Generate Code", use_container_width=True)
else:
    generate = False
    st.warning("Please enter your API key to continue generating code")

# Free uses counter
if st.session_state.code_count < 3:
    st.progress(st.session_state.code_count / 3, text=f"🎉 Free uses remaining: {3 - st.session_state.code_count}")

# Main generation logic
if generate:
    if not query.strip():
        st.warning("Please describe what code you want to generate")
    else:
        with st.spinner("🧙‍♂️ Conjuring your code... This usually takes 10-30 seconds"):
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
                
                # Results section with tabs
                tab1, tab2 = st.tabs(["👩‍💻 Generated Code", "📝 Explanation"])
                
                with tab1:
                    st.markdown(f"**File:** `{response.filename or 'generated_code'}.{response.language}`")
                    st.code(response.code, language=response.language, line_numbers=True)
                    
                    # Download button with nice styling
                    st.download_button(
                        "💾 Download Code", 
                        response.code, 
                        file_name=f"{response.filename or 'generated_code'}.{response.language}", 
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with tab2:
                    st.markdown(response.explanation or "*No explanation provided by the AI*")
                
                st.info(save_code_to_file(response.code, response.language, response.filename))
                st.session_state.code_count += 1

            except Exception as e:
                st.error("🔥 Something went wrong during code generation")
                st.error(str(e))
                if 'output' in locals():
                    with st.expander("🔍 View raw output for debugging"):
                        st.text(output)

# Footer with social links
st.markdown("""
    <div class="footer">
        Glitch Early-Build❇️ · 
        <a href="#" target="_blank">GitHub</a> · 
        <a href="#" target="_blank">Twitter</a> · 
        <a href="#" target="_blank">Docs</a>
        <br><br>
        💡 Tip: Describe both what the code should do and how it should be structured for best results
    </div>
""", unsafe_allow_html=True)