import streamlit as st
from datetime import datetime
from src.helper import get_file_content, load_yaml, check_claim_rejection, get_general_exclusion_context, get_claim_approval_context, get_insurance_docs_embedding
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOllama
import re, json
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain


claim_amount_limit = "5000"

general_exclusion_list = ["HIV/AIDS", 
                          "Parkinson's disease", 
                          "Alzheimer's disease",
                          "pregnancy", 
                          "substance abuse", 
                          "self-inflicted injuries", 
                          "sexually transmitted diseases(std)", 
                          "pre-existing conditions"]

st.title("Insurance Claims")

st.markdown("Fill in the details below for your Insurance claims:")

# User Inputs
name = st.text_input("Patient Name")
address = st.text_input("Address")
claim_reason = st.text_input("Claim Reason (e.g. headache)")
date = st.date_input("Date of Claim")
hospital_name = st.text_input("Hospital Name")
description = st.text_area("Brief Description of Illness", value="NA")

# File upload (PDF)
medical_bill = st.file_uploader("Upload Medical Bill (PDF only)", type=["pdf"])

# Submit Button
if st.button(" Insurance Claim status"):
    with st.spinner("Insurance Documents Analyzing... Please wait."):
        get_insurance_docs_embedding()
        st.success("Analyzing done!")
    if all([name, address, claim_reason, date, hospital_name, description, medical_bill]):
        with st.spinner("Processing your claim... Please wait."):
            prompts = load_yaml(f"config/prompts.yaml")
            bill = get_file_content(medical_bill)
            system_invoice_info_prompt = prompts["system_invoice_info_prompt"]
            user_content = f"INVOICE DETAILS: {bill}"

            messages = [
                SystemMessage(content=system_invoice_info_prompt),
                HumanMessage(content=user_content)
            ]

            llm = ChatOllama(model="llama2", temperature=0.1)
            response = llm(messages)
            json_data = re.search(r'\{.*\}', response.content).group()

            bill_info = json.loads(json_data)

            if bill_info['expense'] != None and int(bill_info['expense']) > int(claim_amount_limit) :
                claim_validation_message = "The amount mentioned for claiming is more than the billed amount. Claim Rejected."
                output = claim_validation_message
            elif bill_info['expense'] != None and int(bill_info['expense']) < int(claim_amount_limit) :
                claim_template = check_claim_rejection(claim_reason, general_exclusion_list, prompts)
                prompt_template = (PromptTemplate(
                                    input_variables=["claim_approval_context", 
                                                    "general_exclusion_context", 
                                                    "patient_info",
                                                    "medical_bill_info",
                                                    "max_amount",
                                                    "disease"],
                                    template=claim_template))
                
                llm = Ollama(model="llama2") 
                llmchain = LLMChain(llm=llm, prompt= prompt_template)

                patient_info = f"Name: {name}\nAddress: {address}\nClaim reason: {claim_reason}\nDate : {date}\nTotal claim amount: {bill_info['expense']}\nDescription: {description}"
                medical_bill_info = f"Medical Bill: {bill}"
                output = llmchain.run({
                                "claim_approval_context": get_claim_approval_context,
                                "general_exclusion_context": get_general_exclusion_context,
                                "patient_info": patient_info,
                                "medical_bill_info": medical_bill_info,
                                "max_amount": bill_info['expense'],
                                "disease": bill_info["disease"],
                                "claim_result_template": prompts["claim_result_template"]
                            })
            else:
                #If no expense value has been extracted
                output = "Please enter a valid Consultation Receipt."

            st.success("Claim submitted!")
            st.info(output)

    else:
        st.warning(" Please fill in all fields and upload the medical bill.")

