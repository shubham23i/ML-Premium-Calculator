# codebasics ML course: codebasics.io, all rights reserverd

import pandas as pd
from joblib import load

import os


def load_artifact(filename):
    path = os.path.join("artifacts", filename)
    return load(path)

model_young = load_artifact("model_young.joblib")
model_rest = load_artifact("model_rest.joblib")
scaler_young = load_artifact("scaler_with_cols.joblib")
scaler_rest = load_artifact("scaler_with_cols.joblib")


def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    # Split the medical history into potential two parts and convert to lowercase
    diseases = medical_history.lower().split(" & ")

    # Calculate the total risk score by summing the risk scores for each part
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)  # Default to 0 if disease not found

    max_score = 14 # risk score for heart disease (8) + second max risk score (6) for diabetes or high blood pressure
    min_score = 0  # Since the minimum score is always 0

    # Normalize the total risk score
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)

    return normalized_risk_score

def preprocess_input(input_dict):
    import pandas as pd

    # All features used in training
    expected_columns = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan', 'genetical_risk', 'normalized_risk_score',
        'gender_Male',
        'region_Northwest', 'region_Southeast', 'region_Southwest', 'region_Northeast',
        'marital_status_Unmarried',
        'bmi_category_Normal', 'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight',
        'smoking_status_No Smoking', 'smoking_status_Occasional', 'smoking_status_Regular',
        'employment_status_Salaried', 'employment_status_Self-Employed', 'employment_status_Freelancer'
    ]

    # Create dataframe with zeros
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    # Encode categorical selections
    if input_dict['Gender'] == 'Male':
        df['gender_Male'] = 1

    region_map = {
        'Northwest': 'region_Northwest',
        'Southeast': 'region_Southeast',
        'Southwest': 'region_Southwest',
        'Northeast': 'region_Northeast'
    }
    df[region_map.get(input_dict['Region'], '')] = 1

    if input_dict['Marital Status'] == 'Unmarried':
        df['marital_status_Unmarried'] = 1

    bmi_map = {
        'Normal': 'bmi_category_Normal',
        'Obesity': 'bmi_category_Obesity',
        'Overweight': 'bmi_category_Overweight',
        'Underweight': 'bmi_category_Underweight'
    }
    df[bmi_map.get(input_dict['BMI Category'], '')] = 1

    smoking_map = {
        'No Smoking': 'smoking_status_No Smoking',
        'Occasional': 'smoking_status_Occasional',
        'Regular': 'smoking_status_Regular'
    }
    df[smoking_map.get(input_dict['Smoking Status'], '')] = 1

    employment_map = {
        'Salaried': 'employment_status_Salaried',
        'Self-Employed': 'employment_status_Self-Employed',
        'Freelancer': 'employment_status_Freelancer'
    }
    df[employment_map.get(input_dict['Employment Status'], '')] = 1

    # Numerical columns
    df['age'] = input_dict['Age']
    df['number_of_dependants'] = input_dict['Number of Dependants']
    df['income_lakhs'] = input_dict['Income in Lakhs']
    df['genetical_risk'] = input_dict['Genetical Risk']

    # Insurance Plan
    plan_map = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df['insurance_plan'] = plan_map.get(input_dict['Insurance Plan'], 1)

    # Normalized risk
    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])

    # Scaling
    df = handle_scaling(input_dict['Age'], df)

    # Final reindex to ensure exact match with model
    expected_features = model_young.get_booster().feature_names
    df = df.reindex(columns=expected_features, fill_value=0)

    # Ensure numeric
    df = df.astype(float)

    return df


def handle_scaling(age, df):
    # scale age and income_lakhs column
    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level'] = None # since scaler object expects income_level supply it. This will have no impact on anything
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    df.drop('income_level', axis='columns', inplace=True)

    return df
    df = handle_scaling(input_dict['Age'], df)

    # Force correct column order & drop unexpected columns
    expected_features = model_young.get_booster().feature_names
    input_df = input_df.reindex(columns=expected_features, fill_value=0)

    # Ensure all numeric types
    df = df.astype(float)

    return d

def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['Age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])

