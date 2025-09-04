import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Calculator", layout="wide")
st.title("💰 Loan Calculator")

# --- User Info ---
st.header("👤 Personal Details")
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=18, max_value=100, step=1)
employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Student", "Other"])
has_coapplicant = st.checkbox("Do you have a co-applicant?")

# --- Loan Details ---
st.header("📄 Loan Details")
loan_amount = st.number_input("Loan Amount (₹)", min_value=1000, step=1000)
deposit = st.number_input("Initial Deposit (₹)", min_value=0, step=1000)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, step=0.1)
years = st.slider("Loan Duration (Years)", 1, 30, 5)
extra_payment = st.toggle("Do you want to make extra yearly payments?")

if extra_payment:
    extra_amt = st.number_input("Extra Payment per Year (₹)", min_value=0, step=1000)
else:
    extra_amt = 0

# --- EMI Calculation ---
if loan_amount and interest_rate and years:
    principal = loan_amount - deposit
    monthly_rate = interest_rate / 100 / 12
    months = years * 12

    emi = principal * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)

    # Build amortization schedule
    balance = principal
    schedule = []
    for m in range(1, months+1):
        interest = balance * monthly_rate
        principal_payment = emi - interest
        balance -= principal_payment
        if m % 12 == 0 and extra_payment:
            balance -= extra_amt
        balance = max(balance, 0)
        schedule.append([m, emi, principal_payment, interest, balance])

    df = pd.DataFrame(schedule, columns=["Month", "EMI", "Principal Paid", "Interest Paid", "Remaining Balance"])

    # --- Results ---
    st.subheader("📊 Loan Summary")
    st.write(f"👤 Name: {name if name else 'Not provided'}")
    st.write(f"📌 Loan Amount: ₹{loan_amount:,.2f}")
    st.write(f"📌 Deposit: ₹{deposit:,.2f}")
    st.write(f"📌 Interest Rate: {interest_rate}%")
    st.write(f"📌 Tenure: {years} years")
    st.success(f"✅ Monthly EMI: ₹{emi:,.2f}")

    # Show DataFrame
    st.dataframe(df.head(24))  # show first 2 years

    # --- Graphs ---
    st.subheader("📈 Loan Visualization")

    col1, col2 = st.columns(2)

    with col1:
        # Remaining Balance over Time
        fig, ax = plt.subplots()
        ax.plot(df["Month"], df["Remaining Balance"], label="Balance", color="blue")
        ax.set_xlabel("Month")
        ax.set_ylabel("Remaining Balance (₹)")
        ax.set_title("Loan Balance Over Time")
        st.pyplot(fig)

    with col2:
        # Interest vs Principal over time
        fig, ax = plt.subplots()
        ax.plot(df["Month"], df["Principal Paid"].cumsum(), label="Principal Paid", color="green")
        ax.plot(df["Month"], df["Interest Paid"].cumsum(), label="Interest Paid", color="red")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Principal vs Interest Paid")
        ax.legend()
        st.pyplot(fig)
