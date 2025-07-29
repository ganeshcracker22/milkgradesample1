
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MilkGrade AI", layout="wide")

st.title("🥛 MilkGrade AI - Batch Quality Dashboard")

st.markdown("""
MilkGrade AI scores your dairy plant milk batches based on:
- **Fat %**
- **SNF**
- **Milk Temperature**
- **CIP (Cleaning-in-Place) Completion**
- **Microbial Risk**
""")

uploaded_file = st.file_uploader("📤 Upload Milk Batch Excel File", type=["xlsx", "csv"])

def calculate_score(row):
    score = 0
    score += 20 if row["Fat %"] >= 3.5 else 0
    score += 20 if row["SNF"] >= 8.3 else 0
    score += 20 if row["Temp (°C)"] <= 8.0 else 0
    score += 20 if row["CIP Done?"].strip().lower() == "yes" else 0
    score += 20 if row["Microbial Risk"].strip().lower() == "no" else 0
    return score

def risk_label(score):
    if score == 100:
        return "Excellent"
    elif score >= 60:
        return "Moderate"
    elif score > 0:
        return "At Risk"
    else:
        return "Critical"

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    df["MilkGrade Score"] = df.apply(calculate_score, axis=1)
    df["Risk Level"] = df["MilkGrade Score"].apply(risk_label)

    st.success("✅ File uploaded and processed successfully!")
    st.dataframe(df.style.applymap(
        lambda val: "background-color: #90ee90" if val == "Excellent" else (
                    "background-color: #fff59d" if val == "Moderate" else (
                    "background-color: #ffcccb" if val == "At Risk" else (
                    "background-color: #f44336; color: white" if val == "Critical" else ""))
        , subset=["Risk Level"]
    ))
else:
    st.info("👈 Upload your batch file to begin. You can download a sample file below.")

    sample_data = pd.DataFrame({
        "Batch ID": ["B001", "B002", "B003"],
        "Fat %": [3.6, 2.8, 3.5],
        "SNF": [8.5, 7.9, 8.3],
        "Temp (°C)": [6.2, 10.5, 7.8],
        "CIP Done?": ["Yes", "No", "Yes"],
        "Microbial Risk": ["No", "Yes", "No"],
        "Time of Milk": ["5:30 AM", "9:00 AM", "6:00 AM"]
    })

    st.download_button("📥 Download Sample Excel", data=sample_data.to_csv(index=False), file_name="sample_batches.csv", mime="text/csv")
