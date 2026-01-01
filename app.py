import streamlit as st
import re
import numpy as np
from PIL import Image
import easyocr

# Initialize OCR
reader = easyocr.Reader(['en', 'hi'], gpu=False)

PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
VOTER_REGEX = r"\b[A-Z]{3}[0-9]{7}\b"

def extract_text(image):
    results = reader.readtext(np.array(image))
    return " ".join([r[1] for r in results])

def extract_pan(text):
    pan = re.search(PAN_REGEX, text)
    dob = re.search(r"\d{2}/\d{2}/\d{4}", text)
    return {
        "document_type": "PAN Card",
        "pan_number": pan.group() if pan else None,
        "dob": dob.group() if dob else None
    }

def extract_voter(text):
    voter = re.search(VOTER_REGEX, text)
    gender = "Male" if "Male" in text else "Female" if "Female" in text else None
    return {
        "document_type": "Voter ID",
        "voter_id": voter.group() if voter else None,
        "gender": gender
    }

st.title("🪪 Government ID OCR")
st.write("Upload PAN Card or Voter ID")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    text = extract_text(image)
    st.text_area("Extracted Text", text)

    if re.search(PAN_REGEX, text):
        st.json(extract_pan(text))
    elif re.search(VOTER_REGEX, text):
        st.json(extract_voter(text))
    else:
        st.warning("Could not identify document")
