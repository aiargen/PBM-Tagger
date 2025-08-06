# PBM-Tagger

A comprehensive solution for automatically generating PBM (Product-Based Management) tags from case summaries using a combination of rule-based heuristics and Large Language Models (LLMs).

## 📋 Overview

PBM-Tagger is designed to streamline the process of categorizing support cases by automatically generating standardized PBM tags. The system combines rule-based heuristics with AI-powered classification to accurately categorize cases based on product, issue category, action category, and resolution comments.

## ✨ Features

- **Dual Classification Approach**: Combines rule-based heuristics with LLM-powered classification
- **Web Interface**: Streamlit-based web application for easy file upload and processing
- **Batch Processing**: Command-line tool for processing large datasets
- **Controlled Vocabulary**: Predefined product, issue, and action categories
- **Data Sanitization**: Automatic cleaning of case summaries (URLs, environment names, etc.)
- **Export Capabilities**: Output results in Excel format with download functionality

## 🏗️ Project Structure

```
PBM-Tagger/
├── app/                          # Web application components
│   ├── app.py                   # Streamlit web interface
│   └── style.css                # Custom CSS styling
├── data/                        # Data files
│   ├── input_data.xls          # Sample input data
│   └── cases_output_with_pbm.xlsx  # Sample output data
├── pbm/                         # Core PBM processing modules
│   ├── __init__.py
│   ├── pipeline.py             # Main processing pipeline
│   ├── llm_chain.py           # LLM integration and chain building
│   ├── heuristics.py          # Rule-based classification logic
│   ├── sanitize.py            # Text cleaning and sanitization
│   └── vocab.py               # Controlled vocabularies
├── .devcontainer/              # Development container configuration
├── PBM preparation.ipynb      # Data preparation and testing notebook
├── run.py                     # Command-line processing script
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aiargen/PBM-Tagger.git
   cd PBM-Tagger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   
   Create a `.env` file in the project root with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 📖 Usage

### Web Interface

1. **Start the Streamlit app**
   ```bash
   streamlit run app/app.py
   ```

2. **Upload and Process**
   - Navigate to the web interface
   - Upload your Excel file (.xls format)
   - Click "Generate PBM Tags"
   - Download the processed results

### Command Line Processing

1. **Prepare your data**
   - Place your input Excel file in the `data/` directory
   - Ensure it contains columns: "Case ID", "Subject", "Description", "Case summary"

2. **Run the processing script**
   ```bash
   python run.py
   ```

3. **Check results**
   - Output will be saved to `data/cases_output_with_pbm.xlsx`

### Jupyter Notebook

For data exploration and testing:
```bash
jupyter notebook "PBM preparation.ipynb"
```

## 🔧 Technical Architecture

### Core Components

#### 1. Pipeline (`pbm/pipeline.py`)
- Main processing orchestrator
- Handles data flow from input to output
- Integrates heuristics and LLM classification
- Generates standardized PBM tags

#### 2. LLM Chain (`pbm/llm_chain.py`)
- Integrates with OpenAI GPT and Google Gemini models
- Structured output parsing using Pydantic
- Controlled vocabulary enforcement
- Error handling and fallback mechanisms

#### 3. Heuristics (`pbm/heuristics.py`)
- Rule-based classification system
- Keyword matching for products, issues, and actions
- Fallback mechanism when LLM is unavailable
- Configurable mapping rules

#### 4. Vocabulary (`pbm/vocab.py`)
- Controlled vocabularies for classification
- Product categories: DWP, DWPC, SRM
- Issue categories: 40+ predefined categories
- Action categories: FAQ, R&D, Customization, etc.

#### 5. Sanitization (`pbm/sanitize.py`)
- Text cleaning and normalization
- URL removal
- Environment name anonymization
- Whitespace normalization

### Classification Process

1. **Data Sanitization**: Clean and normalize case summaries
2. **Heuristic Classification**: Apply rule-based classification
3. **LLM Classification**: Use AI model for enhanced classification (if enabled)
4. **Tag Generation**: Combine results into standardized PBM format
5. **Output**: Generate Excel file with results

### PBM Tag Format

```
#PBM:{product}:{issue_category}:{resolution_comments}:{action_category}
```

Example:
```
#PBM:DWPC:Customization:Resolved after removing Record-type input variable:R&D
```

## 🎯 Supported Categories

### Products
- DWP (Digital Workplace)
- DWPC (Digital Workplace Catalog)
- SRM (Service Request Management)

### Issue Categories
- Customization, Configuration, Network, Restart
- Data, Hotfix, Performance, Approval
- Customer, Defect, Workflow, Cache
- Report, Request, SRD, Entitlement
- Certificate, Infra, Connector, Integration
- And 20+ more categories...

### Action Categories
- FAQ, R&D, Customization, KA
- NA, Educate, Idea, Data

## 🔧 Configuration

### LLM Models
The system supports multiple LLM providers:
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Google**: Gemini-1.5-flash

### Processing Modes
- **Heuristic Only**: Fast processing using rule-based classification
- **LLM Enhanced**: Combines heuristics with AI classification
- **LLM Only**: Pure AI-based classification

## 📊 Data Requirements

### Input Format
Excel file (.xls) with the following columns:
- **Case ID**: Unique identifier for each case
- **Subject**: Case subject line
- **Description**: Detailed case description
- **Case summary**: Summary of the case (primary classification source)

### Output Format
Excel file with original columns plus:
- **PBM_Tag**: Generated standardized tag
- **Product**: Identified product category
- **Issue_Category**: Identified issue category
- **Action_Category**: Identified action category
- **Resolution_Comments**: Extracted resolution information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the Jupyter notebook for examples and testing
- Review the code comments for implementation details

## 🔄 Version History

- **v1.0**: Initial release with basic heuristics and LLM integration
- **v1.1**: Added Streamlit web interface
- **v1.2**: Enhanced vocabulary and classification accuracy
- **v1.3**: Improved error handling and fallback mechanisms

---

**Note**: This project requires API keys for LLM functionality. Ensure you have valid API keys configured in your `.env` file for full functionality.
