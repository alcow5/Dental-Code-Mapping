# Configuration settings for the CDT Code Mapper app

# Ollama API settings
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3:8b"  # Default model
SUPPORTED_MODELS = [
    "llama3:8b",
    "phi:latest"
]
REQUEST_TIMEOUT = 30

# CDT Codes database
CDT_CODES_FILE = "cdt_codes.json"

# UI Configuration
PAGE_TITLE = "CDT Code Mapper"
PAGE_ICON = "🦷"
LAYOUT = "wide"

# Example inputs for the sidebar
EXAMPLE_INPUTS = [
    "Patient came in for routine cleaning and exam",
    "Extracted upper right molar due to severe decay",
    "Applied sealants to molars",
    "Root canal treatment on tooth #14",
    "Comprehensive oral evaluation for new patient",
    "Two-surface composite filling on posterior tooth",
    "Crown preparation and temporary crown placement",
    "Panoramic x-ray for orthodontic evaluation"
]

# Error messages
ERROR_MESSAGES = {
    "ollama_connection": "Error connecting to Ollama: {error}",
    "unexpected_response": "Unexpected response format from Ollama",
    "empty_input": "Please enter a procedure summary before submitting.",
    "cdt_codes_load": "Error loading CDT codes database: {error}"
}

# Success messages
SUCCESS_MESSAGES = {
    "json_parsed": "✅ Successfully parsed JSON response!",
    "analyzing": "Analyzing procedure summary...",
    "cdt_codes_loaded": "✅ CDT codes database loaded successfully"
} 