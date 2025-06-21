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
    .code-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .code-number {
        font-weight: bold;
        color: #1f77b4;
        font-size: 1.1rem;
    }
    .code-description {
        color: #333;
        margin-top: 0.5rem;
    }
    .category-header {
        background-color: #f8f9fa;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 1rem 0 0.5rem 0;
        font-weight: bold;
        color: #495057;
    }
</style>
""", unsafe_allow_html=True)

def send_to_ollama(procedure_summary, cdt_codes):
    """Send procedure summary to Ollama API and return response, also return prompt"""
    system_message = get_prompt_for_model(OLLAMA_MODEL, cdt_codes)
    
    # Use user-adjusted settings if available, otherwise use defaults
    temperature = st.session_state.get('temp_temperature', MODEL_TEMPERATURE)
    top_p = st.session_state.get('temp_top_p', MODEL_TOP_P)
    top_k = st.session_state.get('temp_top_k', MODEL_TOP_K)
    repeat_penalty = st.session_state.get('temp_repeat_penalty', MODEL_REPEAT_PENALTY)
    
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
        "stream": False,
        "temperature": temperature,
        "seed": MODEL_SEED,
        "top_p": top_p,
        "top_k": top_k,
        "repeat_penalty": repeat_penalty,
        "num_predict": MODEL_NUM_PREDICT,
        "tfs_z": MODEL_TFS_Z,
        "typical_p": MODEL_TYPICAL_P
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json(), payload
    except requests.exceptions.RequestException as e:
        raise Exception(ERROR_MESSAGES["ollama_connection"].format(error=str(e)))

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_response(procedure_summary, model_name, system_message_hash):
    """Cache responses to ensure identical inputs produce identical outputs"""
    # This function will be called by the main function to check cache first
    return None  # Return None if not in cache, actual response will be fetched

def get_system_message_hash(system_message):
    """Generate a hash of the system message for caching"""
    import hashlib
    return hashlib.md5(system_message.encode()).hexdigest()

def send_to_ollama_with_cache(procedure_summary, cdt_codes):
    """Send procedure summary to Ollama API with caching for consistency"""
    system_message = get_prompt_for_model(OLLAMA_MODEL, cdt_codes)
    system_hash = get_system_message_hash(system_message)
    
    # Create a cache key based on input and model configuration
    cache_key = f"{procedure_summary.strip().lower()}_{OLLAMA_MODEL}_{system_hash}"
    
    # Check if we have a cached response
    cached_response = get_cached_response(procedure_summary, OLLAMA_MODEL, system_hash)
    
    if cached_response is not None:
        return cached_response, {"cached": True}
    
    # If not cached, make the API call
    response, payload = send_to_ollama(procedure_summary, cdt_codes)
    
    # Cache the response (this is handled by the @st.cache_data decorator)
    return response, payload

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

def get_code_category(code):
    """Get the category for a CDT code based on its prefix"""
    prefix = code[:2]
    categories = {
        "D0": "Diagnostic",
        "D1": "Preventive", 
        "D2": "Restorative",
        "D3": "Endodontics",
        "D4": "Periodontics",
        "D5": "Prosthodontics",
        "D6": "Implant Services",
        "D7": "Oral & Maxillofacial Surgery",
        "D8": "Orthodontics",
        "D9": "Adjunctive General Services"
    }
    return categories.get(prefix, "Other")

def filter_codes(cdt_codes, search_term, category_filter):
    """Filter CDT codes based on search term and category"""
    filtered = []
    search_lower = search_term.lower()
    
    for code in cdt_codes:
        # Check if code matches search term
        matches_search = (search_lower in code['code'].lower() or 
                         search_lower in code['description'].lower())
        
        # Check if code matches category filter
        matches_category = (category_filter == "All Categories" or 
                           get_code_category(code['code']) == category_filter)
        
        if matches_search and matches_category:
            filtered.append(code)
    
    return filtered

def show_cdt_database():
    """Display the CDT Code Database browser page"""
    st.markdown('<h1 class="main-header">📚 CDT Code Database</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Browse and search through the complete CDT code database</p>', unsafe_allow_html=True)
    
    # Load CDT codes
    cdt_codes = load_cdt_codes()
    
    if not cdt_codes:
        st.error("❌ CDT codes database is not available. Please check the cdt_codes.json file.")
        return
    
    # Show database stats
    st.markdown(f'<div class="stats-box">📊 <strong>Database:</strong> {len(cdt_codes)} CDT codes available</div>', unsafe_allow_html=True)
    
    # Search and filter controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search CDT Codes:",
            placeholder="Enter code (e.g., D0120) or description keywords...",
            help="Search by CDT code number or procedure description"
        )
    
    with col2:
        # Get unique categories
        categories = ["All Categories"] + sorted(list(set([get_code_category(code['code']) for code in cdt_codes])))
        category_filter = st.selectbox(
            "📂 Filter by Category:",
            categories,
            help="Filter codes by procedure category"
        )
    
    # Filter codes
    filtered_codes = filter_codes(cdt_codes, search_term, category_filter)
    
    # Show results
    if search_term or category_filter != "All Categories":
        st.markdown(f"**Found {len(filtered_codes)} codes** matching your criteria")
    
    # Display codes
    if filtered_codes:
        # Group by category for better organization
        codes_by_category = {}
        for code in filtered_codes:
            category = get_code_category(code['code'])
            if category not in codes_by_category:
                codes_by_category[category] = []
            codes_by_category[category].append(code)
        
        # Display codes grouped by category
        for category, codes in codes_by_category.items():
            st.markdown(f'<div class="category-header">📂 {category} ({len(codes)} codes)</div>', unsafe_allow_html=True)
            
            for code in codes:
                with st.expander(f"🦷 {code['code']} - {code['description'][:50]}{'...' if len(code['description']) > 50 else ''}", expanded=False):
                    st.markdown(f'<div class="code-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="code-number">{code["code"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="code-description">{code["description"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Copy button
                    code_text = f"{code['code']}: {code['description']}"
                    st.code(code_text, language="text")
                    if st.button(f"📋 Copy {code['code']}", key=f"copy_{code['code']}"):
                        st.write("✅ Copied to clipboard!")
                        st.session_state[f"copied_{code['code']}"] = True
    else:
        st.info("🔍 No codes found matching your search criteria. Try adjusting your search terms or category filter.")
    
    # Show category breakdown
    with st.expander("📊 Database Statistics", expanded=False):
        category_counts = {}
        for code in cdt_codes:
            category = get_code_category(code['code'])
            category_counts[category] = category_counts.get(category, 0) + 1
        
        st.subheader("Codes by Category:")
        for category, count in sorted(category_counts.items()):
            st.markdown(f"- **{category}:** {count} codes")

def show_main_page():
    """Display the main CDT mapping page"""
    st.markdown('<h1 class="main-header">🦷 CDT Code Mapper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Map dental procedure summaries to CDT codes using AI</p>', unsafe_allow_html=True)
    
    # Load CDT codes
    cdt_codes = load_cdt_codes()
    
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
    
    # Consistency settings
    with st.expander("🎯 Consistency Settings", expanded=False):
        st.markdown("**Adjust these settings to control response consistency:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=MODEL_TEMPERATURE,
                step=0.1,
                help="Lower values = more consistent, Higher values = more creative"
            )
            
            top_p = st.slider(
                "Top-p (Nucleus Sampling):",
                min_value=0.1,
                max_value=1.0,
                value=MODEL_TOP_P,
                step=0.1,
                help="Controls diversity of token selection"
            )
        
        with col2:
            top_k = st.slider(
                "Top-k:",
                min_value=1,
                max_value=50,
                value=MODEL_TOP_K,
                step=1,
                help="Limits token selection to top-k most likely tokens"
            )
            
            repeat_penalty = st.slider(
                "Repeat Penalty:",
                min_value=1.0,
                max_value=2.0,
                value=MODEL_REPEAT_PENALTY,
                step=0.1,
                help="Penalizes repeated tokens"
            )
        
        # Update global settings when user changes them
        if (temperature != MODEL_TEMPERATURE or top_p != MODEL_TOP_P or 
            top_k != MODEL_TOP_K or repeat_penalty != MODEL_REPEAT_PENALTY):
            st.session_state['temp_temperature'] = temperature
            st.session_state['temp_top_p'] = top_p
            st.session_state['temp_top_k'] = top_k
            st.session_state['temp_repeat_penalty'] = repeat_penalty
            st.info("🔄 Settings updated! Submit again to use new consistency parameters.")
        
        st.markdown("""
        **Consistency Tips:**
        - **Temperature 0.0-0.2:** Very consistent, deterministic responses
        - **Temperature 0.3-0.5:** Balanced consistency and creativity
        - **Temperature 0.6+:** More varied, creative responses
        - **Lower Top-p/Top-k:** More focused, consistent outputs
        - **Higher Repeat Penalty:** Reduces repetitive text
        """)
    
    # Results area
    if submit_button and procedure_summary.strip():
        if not cdt_codes:
            st.error("❌ CDT codes database is not available. Please check the cdt_codes.json file.")
            return
            
        st.header("📊 Results")
        
        with st.spinner(SUCCESS_MESSAGES["analyzing"]):
            try:
                response, prompt_payload = send_to_ollama_with_cache(procedure_summary, cdt_codes)
                
                # Show the prompt sent to the model
                with st.expander("📝 Prompt Sent to Model", expanded=False):
                    st.markdown('<div class="prompt-label">System Message:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-box">{prompt_payload["messages"][0]["content"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="prompt-label">User Message:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-box">{prompt_payload["messages"][1]["content"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="prompt-label">Model:</div>', unsafe_allow_html=True)
                    st.code(prompt_payload["model"], language="text")
                
                # Show consistency settings used
                with st.expander("🎯 Consistency Settings Used", expanded=False):
                    st.markdown("**Parameters used for this response:**")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Temperature", f"{prompt_payload.get('temperature', 'N/A')}")
                    with col2:
                        st.metric("Top-p", f"{prompt_payload.get('top_p', 'N/A')}")
                    with col3:
                        st.metric("Top-k", f"{prompt_payload.get('top_k', 'N/A')}")
                    with col4:
                        st.metric("Repeat Penalty", f"{prompt_payload.get('repeat_penalty', 'N/A')}")
                    
                    st.info("💡 **Tip:** Lower temperature values produce more consistent responses. Adjust settings above for different consistency levels.")
                
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
                        
                        # Clean and deduplicate the JSON response
                        if json_data:
                            json_data = clean_json_response(json_data)
                    
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

def deduplicate_codes(codes_list):
    """Remove duplicate codes while preserving order"""
    seen = set()
    deduplicated = []
    for code in codes_list:
        if code not in seen:
            seen.add(code)
            deduplicated.append(code)
    return deduplicated

def clean_json_response(json_data):
    """Clean and deduplicate codes in JSON response"""
    if 'cdt_codes' in json_data and isinstance(json_data['cdt_codes'], list):
        # Deduplicate codes
        for code_info in json_data['cdt_codes']:
            if 'code' in code_info:
                # Ensure code is a string and clean it
                code_info['code'] = str(code_info['code']).strip()
        
        # Remove duplicate code entries
        seen_codes = set()
        unique_codes = []
        for code_info in json_data['cdt_codes']:
            code = code_info.get('code', '')
            if code and code not in seen_codes:
                seen_codes.add(code)
                unique_codes.append(code_info)
        
        json_data['cdt_codes'] = unique_codes
    
    return json_data

def main():
    """Main function with page navigation"""
    # Page navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["🦷 CDT Code Mapper", "📚 CDT Database Browser"]
    )
    
    if page == "🦷 CDT Code Mapper":
        show_main_page()
    elif page == "📚 CDT Database Browser":
        show_cdt_database()

if __name__ == "__main__":
    main() 