import streamlit as st
import requests
import json
import re
from config import *
from prompts import get_prompt_for_model

# Load CDT codes database
@st.cache_data(ttl=0)  # Clear cache immediately
def load_cdt_codes():
    """Load CDT codes from JSON file"""
    try:
        with open(CDT_CODES_FILE, 'r') as f:
            cdt_codes = json.load(f)
        return cdt_codes
    except Exception as e:
        st.error(ERROR_MESSAGES["cdt_codes_load"].format(error=str(e)))
        return []

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
    }
    .stats-box {
        background-color: #d4edda;
        color: #155724;
        font-weight: 500;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    .prompt-box {
        background-color: #f8f9fa;
        color: #333333;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        border-left: 4px solid #6c757d;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.4;
    }
    .prompt-box code {
        background-color: #e9ecef;
        color: #495057;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
    }
    .prompt-label {
        font-weight: bold;
        color: #495057;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def send_to_ollama(procedure_summary, cdt_codes):
    """Send procedure summary to Ollama API and return response, also return prompt"""
    system_message = get_prompt_for_model(OLLAMA_MODEL, cdt_codes)
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"Please analyze this dental procedure summary and provide the appropriate CDT codes: {procedure_summary}"
            }
        ],
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json(), payload
    except requests.exceptions.RequestException as e:
        raise Exception(ERROR_MESSAGES["ollama_connection"].format(error=str(e)))

def is_json_parseable(text):
    """Check if text can be parsed as JSON"""
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def extract_json_from_text(text):
    """Extract JSON from text that might contain additional content"""
    # Look for JSON patterns in the text
    json_pattern = r'\{.*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None

def main():
    # Load CDT codes
    cdt_codes = load_cdt_codes()
    
    # Header
    st.markdown('<h1 class="main-header">🦷 CDT Code Mapper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Map dental procedure summaries to CDT codes using AI</p>', unsafe_allow_html=True)
    
    # Show CDT codes status
    if cdt_codes:
        st.markdown(f'<div class="stats-box">📊 <strong>CDT Database:</strong> {len(cdt_codes)} codes loaded</div>', unsafe_allow_html=True)
    
    # Sidebar for additional info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(f"""
        This app uses a locally running Ollama model ({OLLAMA_MODEL}) to map dental procedure summaries to appropriate CDT codes.
        
        **🔒 Privacy & Security:**
        - **100% Local Processing** - No data leaves your computer
        - **HIPAA Compliant** - Patient information stays private
        - **No Cloud Dependencies** - Works completely offline
        - **Client Data Safe** - No third-party data sharing
        
        **Features:**
        - Comprehensive CDT code database
        - AI-powered code mapping
        - Confidence scoring
        - Multiple display formats
        
        **Requirements:**
        - Ollama must be running locally
        - {OLLAMA_MODEL} model must be installed
        
        **To install the model:**
        ```bash
        ollama pull {OLLAMA_MODEL}
        ```
        """)
        
        # Cache clearing button
        if st.button("🔄 Refresh CDT Database", help="Clear cache and reload CDT codes"):
            st.cache_data.clear()
            st.rerun()
        
        st.header("📝 Example Inputs")
        for example in EXAMPLE_INPUTS:
            st.markdown(f"- \"{example}\"")
        
        if cdt_codes:
            st.header("📊 CDT Code Categories")
            categories = {
                "Oral Evaluations": len([c for c in cdt_codes if c['code'].startswith('D01')]),
                "Radiographic": len([c for c in cdt_codes if c['code'].startswith('D02') or c['code'].startswith('D03') or c['code'].startswith('D07')]),
                "Preventive": len([c for c in cdt_codes if c['code'].startswith('D11') or c['code'].startswith('D13')]),
                "Restorations": len([c for c in cdt_codes if c['code'].startswith('D21') or c['code'].startswith('D23') or c['code'].startswith('D25') or c['code'].startswith('D26')]),
                "Crowns": len([c for c in cdt_codes if c['code'].startswith('D27')]),
                "Endodontics": len([c for c in cdt_codes if c['code'].startswith('D31') or c['code'].startswith('D33')]),
                "Extractions": len([c for c in cdt_codes if c['code'].startswith('D71') or c['code'].startswith('D72')]),
                "Surgical": len([c for c in cdt_codes if c['code'].startswith('D74') or c['code'].startswith('D75')])
            }
            
            for category, count in categories.items():
                if count > 0:
                    st.markdown(f"- **{category}:** {count} codes")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Procedure Summary")
        procedure_summary = st.text_area(
            "Enter the dental procedure summary:",
            height=150,
            placeholder="e.g., Patient came in for routine cleaning and examination. Found moderate plaque buildup and recommended deep cleaning."
        )
        
        submit_button = st.button("🔍 Map to CDT Codes", type="primary", use_container_width=True)
    
    with col2:
        st.header("⚙️ Settings")
        response_format = st.selectbox(
            "Response Format:",
            ["Auto-detect", "Raw Text", "JSON Only"],
            help="Choose how to display the model response"
        )
        
        st.info("💡 **Tip:** The model will attempt to return structured JSON with CDT codes and explanations.")
        
        if cdt_codes:
            st.success(f"✅ {len(cdt_codes)} CDT codes available")
        else:
            st.error("❌ CDT codes database not loaded")
    
    # Results area
    if submit_button and procedure_summary.strip():
        if not cdt_codes:
            st.error("❌ CDT codes database is not available. Please check the cdt_codes.json file.")
            return
            
        st.header("📊 Results")
        
        with st.spinner(SUCCESS_MESSAGES["analyzing"]):
            try:
                response, prompt_payload = send_to_ollama(procedure_summary, cdt_codes)
                
                # Show the prompt sent to the model
                with st.expander("📝 Prompt Sent to Model", expanded=False):
                    st.markdown('<div class="prompt-label">System Message:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-box">{prompt_payload["messages"][0]["content"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="prompt-label">User Message:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-box">{prompt_payload["messages"][1]["content"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-label">Model:</div>', unsafe_allow_html=True)
                    st.code(prompt_payload["model"], language="text")
                
                if 'message' in response and 'content' in response['message']:
                    content = response['message']['content']
                    
                    # Show the raw model output
                    with st.expander("🧾 Raw Model Output", expanded=False):
                        st.markdown('<div class="prompt-label">Raw Response:</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="prompt-box">{content}</div>', unsafe_allow_html=True)
                    
                    # Try to parse as JSON
                    json_data = None
                    if response_format == "Auto-detect" or response_format == "JSON Only":
                        if is_json_parseable(content):
                            json_data = json.loads(content)
                        else:
                            json_data = extract_json_from_text(content)
                    
                    # Display results
                    if json_data and response_format != "Raw Text":
                        st.success(SUCCESS_MESSAGES["json_parsed"])
                        
                        # Display CDT codes
                        if 'cdt_codes' in json_data:
                            st.subheader("🦷 CDT Codes Found:")
                            for i, code_info in enumerate(json_data['cdt_codes'], 1):
                                confidence_color = {
                                    "high": "🟢",
                                    "medium": "🟡", 
                                    "low": "🔴"
                                }.get(code_info.get('confidence', 'unknown'), "⚪")
                                
                                with st.expander(f"{confidence_color} Code {i}: {code_info.get('code', 'N/A')}"):
                                    st.write(f"**Description:** {code_info.get('description', 'N/A')}")
                                    st.write(f"**Confidence:** {code_info.get('confidence', 'N/A')}")
                        
                        # Display explanation
                        if 'explanation' in json_data:
                            st.subheader("💡 Explanation:")
                            st.info(json_data['explanation'])
                    
                    # Display raw response
                    if response_format == "Raw Text" or (response_format == "Auto-detect" and not json_data):
                        st.subheader("📄 Raw Response:")
                        st.markdown(f'<div class="result-box">{content}</div>', unsafe_allow_html=True)
                    
                    # Show JSON structure if available
                    if json_data and response_format != "Raw Text":
                        st.subheader("🔧 JSON Structure:")
                        st.json(json_data)
                
                else:
                    st.error(ERROR_MESSAGES["unexpected_response"])
                    st.json(response)
                    
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.markdown("""
                <div class="error-box">
                    <strong>Possible solutions:</strong><br>
                    1. Make sure Ollama is running: <code>ollama serve</code><br>
                    2. Ensure {OLLAMA_MODEL} model is installed: <code>ollama pull {OLLAMA_MODEL}</code><br>
                    3. Check if the model is available: <code>ollama list</code>
                </div>
                """, unsafe_allow_html=True)
    
    elif submit_button and not procedure_summary.strip():
        st.warning(f"⚠️ {ERROR_MESSAGES['empty_input']}")

if __name__ == "__main__":
    main() 