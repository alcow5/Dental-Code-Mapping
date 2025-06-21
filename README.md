# �� CDT Code Mapper

A **HIPAA-compliant, locally-run AI tool** for mapping dental procedure summaries to CDT (Current Dental Terminology) codes using Ollama and Streamlit.

## 🔒 Privacy & Security

- **100% Local Processing** - No data leaves your computer
- **HIPAA Compliant** - Patient information stays private
- **No Cloud Dependencies** - Works completely offline
- **Client Data Safe** - No third-party data sharing

## ✨ Features

- **AI-Powered Code Mapping** - Uses Phi model for intelligent CDT code selection
- **Comprehensive Database** - 102+ CDT codes covering all major dental procedures
- **Confidence Scoring** - High/Medium/Low confidence levels for each code
- **Multiple Display Formats** - JSON, raw text, or auto-detect
- **Real-time Analysis** - Instant CDT code suggestions
- **Detailed Explanations** - AI explains why specific codes were selected
- **Specialty Procedure Support** - Handles complex cases like crowns, root canals, extractions
- **Adult vs Child Procedures** - Intelligent defaults and age-specific coding

## 📊 Performance

**Comprehensive Testing Suite:**
- **18 test cases** covering major dental procedure categories
- **Continuous improvement** through iterative prompt refinement
- **Specialty procedure recognition** for complex dental cases
- **Multi-code response handling** for procedures requiring multiple codes

### Test Categories:
- ✅ **Basic Procedures:** Cleanings, exams, fluoride treatments
- ✅ **Restorative:** Composite fillings, crowns, inlays/onlays
- ✅ **Endodontics:** Root canals (anterior, bicuspid, molar)
- ✅ **Surgical:** Extractions, incision & drainage
- ✅ **Periodontal:** Scaling & root planing, debridement
- ✅ **Specialty:** Stainless steel crowns, biteguards, palliative care

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - [Install Ollama](https://ollama.ai/download)
3. **Phi Model** - Download the model

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cdt_code_mapper
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama model:**
   ```bash
   ollama pull phi:latest
   ```

4. **Start Ollama:**
   ```bash
   ollama serve
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Access the app:** Open http://localhost:8501 in your browser

## 📖 Usage

### Basic Usage

1. **Enter Procedure Summary** - Describe the dental procedure in natural language
2. **Click "Map to CDT Codes"** - AI analyzes and suggests appropriate codes
3. **Review Results** - View suggested codes with confidence levels and explanations

### Example Inputs

```
"Patient came in for routine dental checkup. We did a full oral exam and a cleaning."

"Applied fluoride varnish and sealants on molars for an 8-year-old patient."

"Completed root canal on upper premolar due to chronic pain."

"Extracted an erupted tooth with forceps under local anesthesia."

"Placed a preformed stainless steel crown on primary molar with deep decay."
```

### Response Format

The app returns structured JSON with:
- **CDT Codes** with descriptions and confidence levels
- **Explanations** of why codes were selected
- **Raw model output** for transparency

## 🧪 Testing

### Run Test Suite

```bash
python test_cases.py
```

### Test Coverage

The test suite includes comprehensive test cases covering:
- Standard procedures (cleanings, exams)
- Pediatric procedures (sealants, fluoride)
- Restorative procedures (fillings, crowns)
- Endodontic procedures (root canals)
- Surgical procedures (extractions, incision & drainage)
- Periodontal procedures (scaling & root planing)
- Specialty procedures (stainless steel crowns, biteguards)

### Development Testing

```bash
# Run all tests
python test_cases.py

# Verify Ollama setup
python test_setup.py
```

## 🏗️ Architecture

### Components

- **Frontend:** Streamlit web interface
- **Backend:** Python with Ollama API integration
- **AI Model:** Phi model (locally hosted)
- **Database:** JSON-based CDT code repository
- **Configuration:** Centralized config management

### File Structure

```
cdt_code_mapper/
├── app.py              # Main Streamlit application
├── config.py           # Configuration and system prompts
├── cdt_codes.json      # CDT code database
├── test_cases.py       # Comprehensive test suite
├── test_setup.py       # Ollama setup verification
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Configuration

### Model Settings

- **Model:** Phi model
- **API Endpoint:** http://localhost:11434/api/chat
- **Timeout:** 30 seconds
- **Temperature:** Default (deterministic responses)

### System Prompt

The AI uses a sophisticated system prompt that includes:
- **Code Categories** - Organized by procedure type
- **Specificity Guidelines** - Tooth type, surface count, materials
- **Adult vs Child Procedures** - Age-appropriate defaults
- **Specialty Procedures** - Complex case handling
- **Multi-Code Responses** - Multiple service scenarios

## 🛠️ Development

### Adding New CDT Codes

1. Edit `cdt_codes.json`
2. Add new code entries with format:
   ```json
   {
     "code": "DXXXX",
     "description": "Procedure description"
   }
   ```

## 📋 CDT Code Categories

The database includes codes for:
- **Oral Evaluations** (D0120-D0160)
- **Radiographic Procedures** (D0210-D0708)
- **Preventive Services** (D1120-D1330)
- **Restorations** (D2140-D2394)
- **Crowns & Fixed Prosthodontics** (D2510-D2794)
- **Endodontic Therapy** (D3320-D3348)
- **Periodontal Procedures** (D4341-D4910)
- **Extractions** (D7111-D7240)
- **Surgical Procedures** (D7450-D7530)
- **Specialty Services** (D9110-D9946)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is designed to assist dental professionals with CDT code selection but should not replace professional judgment. Always verify codes against official CDT documentation and consult with billing specialists when needed.

## 🆘 Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Install Ollama: https://ollama.ai/download
   - Start Ollama: `ollama serve`

2. **"Model not found"**
   - Download model: `ollama pull phi:latest`
   - Check available models: `ollama list`

3. **"Streamlit not found"**
   - Install dependencies: `pip install -r requirements.txt`

4. **"CDT codes not loading"**
   - Check `cdt_codes.json` file exists
   - Use refresh button in app sidebar

### Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test results with `python test_cases.py`
3. Verify Ollama setup with `python test_setup.py`
4. Open an issue on GitHub

---

**Built with ❤️ for dental professionals who value privacy and accuracy.**