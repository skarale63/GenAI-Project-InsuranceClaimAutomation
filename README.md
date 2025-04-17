# GenAI-Project-InsuranceClaimAutomation

A Generative AI-powered application that automates insurance claim processing using LLMs. This tool analyzes medical bills and disease information to determine whether an insurance claim should be **approved** or **rejected**, along with the **reason** for the decision.

---

## Key Features

- Upload and analyze medical bills and related documents  
- Query claims using natural language  
- LLM-based decision engine for claim approval/rejection  
- Uses LangChain, Python, and Streamlit for end-to-end workflow  
- User-friendly Streamlit interface

---

## Tech Stack

- **Python 3.10+**
- **LLMs (via LangChain)**
- **Streamlit** – for UI
- **LangChain** – for chaining LLM logic
- **ChatOllama + ConversationalRetrievalChain** – for document Q&A (internal)

---

## Installation & Setup

Run the following commands to set up and start the project:

```bash
# Step 1: Setup environment
bash venv_setup.py

# Step 2: Navigate to GenAI-Project-InsuranceClaimAutomation git repo directory
cd GenAI-Project-InsuranceClaimAutomation

# Step 3: Activate virtual environment
source env/Scripts/activate  # Use `source env/bin/activate` on Mac/Linux

# Step 4: Launch the Streamlit app
streamlit run app.py

## project_structure

GenAI-Project-InsuranceClaimAutomation/
├── app.py
├── Bills/
│   ├── Alzheimer.pdf
│   ├── Bodyache.pdf
│   ├── HIV.pdf
├── config/
│   ├── prompts.yaml
├── faiss_index/
│   ├── index.faiss
│   ├── index.pkl
├── notebook/
│   ├── 01_operation_on_bill_data.ipynb
├── README.md
├── requirements.txt
├── resources/
│   ├── med_bill1.pdf
│   ├── MembershipHandbook-22-23.pdf
│   ├── MembershipHandbook.pdf
│   ├── Patient Information.pdf
│   ├── Worldwide Assistance Programme.pdf
├── setup.py
├── src/
│   ├── helper.py
│   ├── __init__.py
├── venv_setup.sh
