# 🦷 CDT Code Mapper

A **HIPAA-compliant, locally-run AI tool** for mapping dental procedure summaries to CDT (Current Dental Terminology) codes using Ollama and Streamlit.

## 🔒 Privacy & Security

- **100% Local Processing** - No data leaves your computer
- **HIPAA Compliant** - Patient information stays private
- **No Cloud Dependencies** - Works completely offline
- **Client Data Safe** - No third-party data sharing

## ✨ Features

- **AI-Powered Code Mapping** - Uses Llama3:8b model for intelligent CDT code selection
- **Comprehensive Database** - 110+ CDT codes covering all major dental procedures
- **Confidence Scoring** - High/Medium/Low confidence levels for each code
- **Multiple Display Formats** - JSON, raw text, or auto-detect
- **Real-time Analysis** - Instant CDT code suggestions
- **Detailed Explanations** - AI explains why specific codes were selected
- **Specialty Procedure Support** - Handles complex cases like crowns, root canals, extractions
- **Adult vs Child Procedures** - Intelligent defaults and age-specific coding
- **Model-Specific Prompts** - Optimized prompts for different AI models
- **Enhanced UI** - Prompt display, raw output visibility, and improved user experience
- **Comprehensive Testing** - 28+ test cases with category-based testing
- **Reference System** - Organized test cases for easy maintenance and expansion

## 📊 Performance

**Comprehensive Testing Suite:**
- **28 test cases** covering major dental procedure categories
- **83.9% accuracy** on comprehensive test suite
- **Continuous improvement** through iterative prompt refinement
- **Specialty procedure recognition** for complex dental cases
- **Multi-code response handling** for procedures requiring multiple codes
- **Category-based testing** for targeted validation

### Test Categories:
- ✅ **Basic Procedures:** Cleanings, exams, fluoride treatments
- ✅ **Restorative:** Composite fillings, crowns, inlays/onlays
- ✅ **Endodontics:** Root canals (anterior, bicuspid, molar), retreatments
- ✅ **Surgical:** Extractions, incision & drainage, alveoloplasty
- ✅ **Periodontal:** Scaling & root planing, debridement
- ✅ **Specialty:** Stainless steel crowns, biteguards, palliative care
- ✅ **Prosthodontics:** Dentures, partials, repairs
- ✅ **Pediatric:** Sealants, fluoride, space maintainers

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - [Install Ollama](https://ollama.ai/download)
3. **Llama3:8b Model** - Download the model

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alcow5/Dental-Code-Mapping.git
   cd cdt_code_mapper
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama model:**
   ```bash
   ollama pull llama3:8b
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

"Performed scaling and root planing on 4 quadrants for periodontal disease."

"Fabricated and delivered complete upper denture for edentulous patient."
```

### Response Format

The app returns structured JSON with:
- **CDT Codes** with descriptions and confidence levels
- **Explanations** of why codes were selected
- **Raw model output** for transparency
- **System prompt** used for the analysis

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
python test_cases.py

# Run tests by category
python test_cases.py --category basic
python test_cases.py --category restorative
python test_cases.py --category endodontics
python test_cases.py --category surgical
python test_cases.py --category periodontal
python test_cases.py --category specialty
python test_cases.py --category prosthodontics
python test_cases.py --category pediatric
```

### Test Coverage

The test suite includes comprehensive test cases covering:
- Standard procedures (cleanings, exams)
- Pediatric procedures (sealants, fluoride)
- Restorative procedures (fillings, crowns)
- Endodontic procedures (root canals, retreatments)
- Surgical procedures (extractions, incision & drainage)
- Periodontal procedures (scaling & root planing)
- Specialty procedures (stainless steel crowns, biteguards)
- Prosthodontic procedures (dentures, partials)

### Development Testing

```bash
# Run all tests
python test_cases.py

# Verify Ollama setup
python test_setup.py

# Check CDT code database integrity
python check_test_codes.py

# Count test cases
python count_tests.py
```

## 🏗️ Architecture

### Components

- **Frontend:** Streamlit web interface with enhanced UI
- **Backend:** Python with Ollama API integration
- **AI Model:** Llama3:8b model (locally hosted)
- **Database:** JSON-based CDT code repository (110+ codes)
- **Configuration:** Centralized config management
- **Prompt System:** Model-specific optimized prompts
- **Testing Framework:** Comprehensive test suite with categories

### File Structure

```
cdt_code_mapper/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and model settings
├── prompts.py             # Model-specific prompt definitions
├── cdt_codes.json         # CDT code database (110+ codes)
├── test_cases.py          # Comprehensive test suite runner
├── test_reference.py      # Organized test cases by category
├── test_setup.py          # Ollama setup verification
├── check_test_codes.py    # CDT code database integrity checker
├── count_tests.py         # Test case counter
├── demo_mode.py           # Demo mode for testing
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Model Settings

- **Default Model:** Llama3:8b
- **Alternative Models:** Phi, Llama2:13b (configurable)
- **API Endpoint:** http://localhost:11434/api/chat
- **Timeout:** 30 seconds
- **Temperature:** Default (deterministic responses)

### Prompt System

The application uses a sophisticated prompt system with:
- **Model-Specific Prompts** - Optimized for different AI models
- **Code Categories** - Organized by procedure type
- **Specificity Guidelines** - Tooth type, surface count, materials
- **Adult vs Child Procedures** - Age-appropriate defaults
- **Specialty Procedures** - Complex case handling
- **Multi-Code Responses** - Multiple service scenarios
- **Detailed Examples** - Real-world procedure mappings

### Model Comparison

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **Llama3:8b** | Medium | High (83.9%) | Production use |
| **Phi** | Fast | Lower (~25-38%) | Quick testing |
| **Llama2:13b** | Slow | High | Maximum accuracy |

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

### Adding New Test Cases

1. Edit `test_reference.py`
2. Add test cases to appropriate categories:
   ```python
   "basic": [
       {
           "description": "Test description",
           "input": "Procedure summary",
           "expected_codes": ["D0120", "D1110"]
       }
   ]
   ```

### Model Switching

To switch models, edit `config.py`:
```python
MODEL_NAME = "llama3:8b"  # or "phi", "llama2:13b"
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
- **Prosthodontics** (D5110-D5999)

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
   - Download model: `ollama pull llama3:8b`
   - Check available models: `ollama list`

3. **"Streamlit not found"**
   - Install dependencies: `pip install -r requirements.txt`

4. **"CDT codes not loading"**
   - Check `cdt_codes.json` file exists
   - Use refresh button in app sidebar

5. **"Low accuracy on tests"**
   - Verify model is llama3:8b: `ollama list`
   - Check prompt configuration in `prompts.py`
   - Run test verification: `python test_setup.py`

### Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test results with `python test_cases.py`
3. Verify Ollama setup with `python test_setup.py`
4. Check CDT code integrity with `python check_test_codes.py`
5. Open an issue on GitHub

## 🔄 Recent Updates

- **Enhanced UI** with prompt display and raw output visibility
- **Model-specific prompts** for optimal performance
- **Comprehensive test suite** with 28+ test cases
- **Category-based testing** for targeted validation
- **Reference system** for organized test case management
- **Database integrity checks** for CDT code validation
- **Improved accuracy** to 83.9% on comprehensive tests
- **Enhanced prompt engineering** for complex dental procedures

---

**Built with ❤️ for dental professionals who value privacy and accuracy.**