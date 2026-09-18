# HCC Codifier

A Streamlit app that takes a clinical note as input and returns a table of HCC (Hierarchical
Condition Category) and ICD-10 assessment codes, using an LLM (via [LlamaIndex](https://www.llamaindex.ai/))
to apply CMS risk-adjustment coding guidelines.

> **Note:** This is a portfolio/demo project, not a certified medical coding tool. Do not paste
> real patient PHI into the hosted demo — use de-identified or synthetic clinical notes.

## How it works

```
Clinical note (up to, but not including, the Assessment/Plan sections)
        │
        ▼
extract_assessment (hcc_codifier.coder)
        │  system prompt encodes CMS HCC coding guidelines (hcc_codifier.prompts)
        ▼
LlamaIndex OpenAI LLM wrapper (gpt-4o by default)
        │
        ▼
Table: ICD-10 Code | ICD-10 Description | Reasoning
```

## Project structure

```
.
├── app.py                       # Streamlit entry point
├── src/hcc_codifier/
│   ├── coder.py                 # builds messages, calls the LLM
│   ├── config.py                # loads OPENAI_API_KEY / OPENAI_MODEL from .env
│   └── prompts.py                # the CMS HCC-coding system prompt
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
git clone https://github.com/hammuneer/hcc_codification_openai.git
cd hcc_codification_openai
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Configuration

```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY (OPENAI_MODEL is optional, defaults to gpt-4o)
```

### Run

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (default: http://localhost:8501), paste in a clinical note,
and click **Get Diagnosis**.

## Testing

```bash
pytest
```

## License

No license file is currently included in this repository; all rights reserved by default.
