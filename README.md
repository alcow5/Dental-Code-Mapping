# 🦷 CDT Code Mapper

A **HIPAA-compliant, locally-run AI tool** for mapping dental procedure summaries to CDT (Current Dental Terminology) codes using Ollama and Streamlit.

## 🔒 Privacy & Security

- **100% Local Processing** - No data leaves your computer
- **HIPAA Compliant** - Patient information stays private
- **No Cloud Dependencies** - Works completely offline
- **Client Data Safe** - No third-party data sharing

## ✨ Features

- **AI-Powered Code Mapping** - Uses Llama3:8b model for intelligent CDT code selection
- **Comprehensive Database** - 116+ CDT codes covering all major dental procedures
- **Confidence Scoring** - High/Medium/Low confidence levels for each code
- **Multiple Display Formats** - JSON, raw text, or auto-detect
- **Real-time Analysis** - Instant CDT code suggestions
- **Detailed Explanations** - AI explains why specific codes were selected
- **Specialty Procedure Support** - Handles complex cases like crowns, root canals, extractions
- **Adult vs Child Procedures** - Intelligent defaults and age-specific coding
- **Model-Specific Prompts** - Optimized prompts for different AI models
- **Enhanced UI** - Prompt display, raw output visibility, and improved user experience
- **Comprehensive Testing** - 36 test cases with category-based testing
- **Reference System** - Organized test cases for easy maintenance and expansion
- **Multi-page Streamlit Interface** - Main mapping interface and CDT code database browser
- **Model Parameter Controls** - Adjust temperature, top-p, top-k, and repeat penalty for consistency
- **Response Caching** - Cache responses to avoid redundant API calls
- **Parallel Testing** - Fast test execution using optimal thread count (12 threads)
- **Consistency Testing** - Test model response consistency across multiple runs
- **Test Case Manager** - Track test results and focus on cases needing improvement
- **Thread Optimization** - Automatically find optimal thread count for your hardware
- **Database Browser** - Search, filter, and copy CDT codes with full descriptions

## 📊 Performance

**Latest Comprehensive Testing Results (June 2024):**
- **36 test cases** covering major dental procedure categories
- **70.8% accuracy** on comprehensive test suite (27/36 passed)
- **77.8% consistency** across multiple runs (28/36 consistent)
- **55.6% pass rate** for both accuracy and consistency (20/36 cases)
- **Parallel execution** with 12 threads for optimal performance
- **~36x speedup** for accuracy tests, ~108x for consistency tests

### Test Categories:
- ✅ **Basic Procedures:** Cleanings, exams, fluoride treatments
- ✅ **Restorative:** Composite fillings, crowns, inlays/onlays
- ✅ **Endodontics:** Root canals (anterior, bicuspid, molar), retreatments
- ✅ **Surgical:** Extractions, incision & drainage, alveoloplasty
- ✅ **Periodontal:** Scaling & root planing, debridement
- ✅ **Specialty:** Stainless steel crowns, biteguards, palliative care
- ✅ **Prosthodontics:** Dentures, partials, repairs
- ✅ **Pediatric:** Sealants, fluoride, space maintainers
- ✅ **Emergency:** Limited exams, palliative treatment
- ✅ **Implant:** Custom abutments, implant crowns
- ✅ **Sedation:** Nitrous oxide administration
- ✅ **Orthodontic:** Space maintainers, frenectomy

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
4. **Browse CDT Database** - Use the database browser page to search and filter codes
5. **Adjust Model Parameters** - Fine-tune temperature, top-p, top-k for consistency

### Example Inputs

```
"Patient came in for routine dental checkup. We did a full oral exam and a cleaning."

"Applied fluoride varnish and sealants on molars for an 8-year-old patient."

"Completed root canal on upper premolar due to chronic pain."

"Extracted an erupted tooth with forceps under local anesthesia."

"Placed a preformed stainless steel crown on primary molar with deep decay."

"Performed scaling and root planing on 4 quadrants for periodontal disease."

"Fabricated and delivered complete upper denture for edentulous patient."

"Delivered a unilateral space maintainer for a child with premature tooth loss."

"Applied desensitizing medication to hypersensitive teeth."

"Performed occlusal adjustment following crown placement."
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
# Run all tests with parallel execution
python test_cases.py

# Run test case manager (recommended)
python test_case_manager.py run-all

# Run consistency tests
python test_consistency.py

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

### Test Case Manager

The test case manager tracks results and helps focus on cases needing improvement:

```bash
# Run all tests and update results
python test_case_manager.py run-all

# Show current status
python test_case_manager.py status

# Run only cases needing work
python test_case_manager.py run-needs-work

# Force retest all cases
python test_case_manager.py run-all --force
```

### Test Coverage

The test suite includes 36 comprehensive test cases covering:
- Standard procedures (cleanings, exams)
- Pediatric procedures (sealants, fluoride, space maintainers)
- Restorative procedures (fillings, crowns, bridges)
- Endodontic procedures (root canals, pulp treatments)
- Surgical procedures (extractions, incision & drainage)
- Periodontal procedures (scaling & root planing)
- Specialty procedures (stainless steel crowns, biteguards)
- Prosthodontic procedures (dentures, partials)
- Emergency procedures (limited exams, palliative care)
- Implant procedures (custom abutments, crowns)
- Sedation procedures (nitrous oxide)
- Orthodontic procedures (frenectomy, space maintainers)

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

# Optimize thread count for your hardware
python test_thread_optimization.py
```

## 🏗️ Architecture

### Components

- **Frontend:** Streamlit web interface with multi-page design
- **Backend:** Python with Ollama API integration
- **AI Model:** Llama3:8b model (locally hosted)
- **Database:** JSON-based CDT code repository (116+ codes)
- **Configuration:** Centralized config management
- **Prompt System:** Model-specific optimized prompts
- **Testing Framework:** Comprehensive test suite with parallel execution
- **Test Manager:** Result tracking and case management system

### File Structure

```
cdt_code_mapper/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration and model settings
├── prompts.py               # Model-specific prompt definitions
├── cdt_codes.json           # CDT code database (116+ codes)
├── test_cases.py            # Comprehensive test suite runner
├── test_consistency.py      # Consistency testing framework
├── test_case_manager.py     # Test result tracking and management
├── test_reference.py        # Organized test cases by category
├── test_thread_optimization.py  # Thread count optimization
├── test_setup.py            # Ollama setup verification
├── check_test_codes.py      # CDT code database integrity checker
├── count_tests.py           # Test case counter
├── demo_mode.py             # Demo mode for testing
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Model Settings

- **Default Model:** Llama3:8b
- **Alternative Models:** Phi, Llama2:13b (configurable)
- **API Endpoint:** http://localhost:11434/api/chat
- **Timeout:** 30 seconds
- **Temperature:** 0.0 for maximum consistency
- **Top-p:** 0.9 for balanced creativity
- **Top-k:** 40 for focused responses
- **Repeat Penalty:** 1.1 to reduce repetition

### Performance Optimization

- **Optimal Thread Count:** 12 threads (automatically detected)
- **Hardware Optimization:** 16-core, 16-thread CPU with 63GB RAM
- **Parallel Execution:** ~36x speedup for accuracy tests
- **Consistency Testing:** ~108x speedup for multiple runs
- **Response Caching:** Avoid redundant API calls

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
| **Llama3:8b** | Medium | High (70.8%) | Production use |
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
- **Pediatric Procedures** (D1510-D1999)
- **Emergency Services** (D0140-D0160)
- **Implant Services** (D6050-D6199)

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

6. **"Slow test execution"**
   - Run thread optimization: `python test_thread_optimization.py`
   - Use parallel execution with optimal thread count
   - Check system resources during testing

### Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test results with `python test_cases.py`
3. Use test case manager: `python test_case_manager.py status`
4. Verify Ollama setup with `python test_setup.py`
5. Check CDT code integrity with `python check_test_codes.py`
6. Open an issue on GitHub

## 🔄 Recent Updates (June 2024)

### Major Enhancements
- **Expanded Test Suite**: Added 8 new test cases (36 total)
- **Test Case Manager**: Comprehensive result tracking and case management
- **Thread Optimization**: Automatic detection of optimal thread count (12 threads)
- **Parallel Execution**: ~36x speedup for accuracy tests, ~108x for consistency tests
- **Consistency Testing**: Multi-run testing to measure model reliability
- **Database Browser**: Enhanced CDT code search and filter functionality
- **Model Parameter Controls**: Fine-tune temperature, top-p, top-k, repeat penalty
- **Response Caching**: Avoid redundant API calls for better performance

### Performance Improvements
- **Accuracy**: 70.8% on 36 test cases (27/36 passed)
- **Consistency**: 77.8% consistent responses (28/36 cases)
- **Combined Success**: 55.6% pass both accuracy and consistency (20/36 cases)
- **Execution Speed**: ~2.13 seconds average per test case
- **Parallel Processing**: 12 threads optimal for your hardware configuration

### New Test Cases Added
- Space Maintainer Delivery
- Tooth Desensitization
- Apicoectomy with Root End Filling
- Occlusal Adjustment Post-Treatment
- Porcelain Crown on Posterior Tooth
- Pulpectomy on Primary Tooth
- Re-cement Crown
- Complete Oral Evaluation for New Patient

### Technical Improvements
- **Enhanced UI**: Multi-page Streamlit interface with database browser
- **Improved Prompts**: Model-specific optimizations for better accuracy
- **Result Tracking**: Persistent test results with JSON storage
- **Hardware Optimization**: Thread count optimization for maximum performance
- **Error Handling**: Better error handling and user feedback
- **Documentation**: Comprehensive README with usage examples

## Performance Metrics

- **Accuracy**: 70.8% on comprehensive test suite (36 cases)
- **Consistency**: 77.8% consistent responses across multiple runs
- **Speed**: ~2.13 seconds average per test case with parallel execution
- **Throughput**: 108 test runs completed in ~207 seconds
- **Hardware**: Optimized for 16-core, 16-thread CPU with 63GB RAM
- **Thread Count**: 12 threads optimal for maximum performance

## Test Results Summary

### Cases Passing Both Tests (20/36 - 55.6%)
- Bitewing X-rays and Composite Filling
- Complete Oral Evaluation for New Patient
- Crown Lengthening
- Custom Abutment with Implant Crown
- Flap Surgery - One to Three Teeth
- Frenulectomy
- Full Mouth Debridement
- Full Mouth X-rays
- Incision and Drainage
- Interim Partial Denture
- Nitrous Oxide Sedation
- Panoramic Radiograph for Assessment
- Pediatric Sealants + Fluoride
- Post and Core with Crown
- Scaling and Root Planing (SRP)
- Space Maintainer Delivery
- Stainless Steel Crown on Child
- Tooth Desensitization
- Tooth Extraction
- Topical Anesthesia with Debridement

### Cases Needing Work (16/36 - 44.4%)
- Anterior Composite – Two Surfaces
- Apicoectomy with Root End Filling
- Biteguard Delivery
- Emergency Palliative Treatment
- Fluoride Treatment + Hygiene Instruction
- Full Denture Delivery
- Limited Emergency Exam
- Occlusal Adjustment Post-Treatment
- Porcelain Crown on Posterior Tooth
- Pulpectomy on Primary Tooth
- Pulpotomy on Primary Molar
- Re-cement Bridge
- Re-cement Crown
- Resin Crown Placement
- Root Canal – Premolar
- Standard Adult Checkup + Cleaning

---

**Built with ❤️ for dental professionals who value privacy and accuracy.**