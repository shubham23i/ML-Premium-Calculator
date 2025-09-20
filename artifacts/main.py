import streamlit as st

# Page setup
st.set_page_config(page_title="Insurance Risk Input Form", layout="wide")

st.title("Insurance Premium Calculator")

# =========================
# Input Form
# =========================
with st.form("insurance_form"):

    st.subheader("Personal Information")

    # --- Row 1 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    with col2:
        region = st.selectbox("Region", ["Northwest", "Southeast", "Northeast", "Southwest"])
    with col3:
        marital_status = st.radio("Marital Status", ["Unmarried", "Married"], horizontal=True)

    # --- Row 2 ---
    col4, col5, col6 = st.columns(3)
    with col4:
        bmi_category = st.selectbox("BMI Category", ["Normal", "Obesity", "Overweight", "Underweight"])
    with col5:
        smoking_status = st.selectbox(
            "Smoking Status",
            ["No Smoking", "Regular", "Occasional", "Smoking=0", "Does Not Smoke", "Not Smoking"]
        )
    with col6:
        employment_status = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Freelancer"])

    st.subheader("Financial & Medical Information")

    # --- Row 3 ---
    col7, col8, col9 = st.columns(3)
    with col7:
        income_level = st.selectbox("Income Level", ["<10L", "10L - 25L", "25L - 40L", "> 40L"])
    with col8:
        medical_history = st.selectbox(
            "Medical History",
            [
                "Diabetes", "High blood pressure", "No Disease",
                "Diabetes & High blood pressure", "Thyroid", "Heart disease",
                "High blood pressure & Heart disease", "Diabetes & Thyroid",
                "Diabetes & Heart disease"
            ]
        )
    with col9:
        insurance_plan = st.radio("Insurance Plan", ["Bronze", "Silver", "Gold"], horizontal=True)

    # --- Submit button ---
    submitted = st.form_submit_button("Submit")

# =========================
# Display results
# =========================
if submitted:
    st.success("✅ Form submitted successfully!")
    st.write({
        "Gender": gender,
        "Region": region,
        "Marital Status": marital_status,
        "BMI Category": bmi_category,
        "Smoking Status": smoking_status,
        "Employment Status": employment_status,
        "Income Level": income_level,
        "Medical History": medical_history,
        "Insurance Plan": insurance_plan,
    })
