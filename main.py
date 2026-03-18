import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Student Wallet AI", page_icon="🎓", layout="wide")

# Custom CSS for an attractive UI
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])

# --- SIDEBAR: INPUT ---
st.sidebar.header("➕ Add Transaction")
with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.now())
    t_type = st.selectbox("Type", ["Expense", "Earning"])
    
    if t_type == "Expense":
        category = st.selectbox("Category", ["Food & Snacks", "Transport", "Books/Study", "Subscription", "Rent/Bills", "Other"])
    else:
        category = st.selectbox("Category", ["Part-time Job", "Allowance", "Freelance", "Gift", "Scholarship"])
        
    amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    note = st.text_input("Note (e.g., 'Pizza with friends')")
    
    submit = st.form_submit_button("Add to Tracker")

if submit and amount > 0:
    new_data = pd.DataFrame([[date, t_type, category, amount, note]], columns=st.session_state.transactions.columns)
    st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
    st.success("Transaction recorded!")

# --- MAIN DASHBOARD ---
st.title("🎓 Student Wallet AI")
st.markdown("Track your hustle and manage your spend with ease.")

# Metrics Row
df = st.session_state.transactions
total_earnings = df[df["Type"] == "Earning"]["Amount"].sum()
total_expenses = df[df["Type"] == "Expense"]["Amount"].sum()
balance = total_earnings - total_expenses

col1, col2, col3 = st.columns(3)
col1.metric("Total Earnings", f"${total_earnings:,.2f}")
col2.metric("Total Expenses", f"${total_expenses:,.2f}", delta_color="inverse")
col3.metric("Current Balance", f"${balance:,.2f}")

st.divider()

# --- AI INSIGHTS & ANALYTICS ---
if not df.empty:
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📊 Spending Breakdown")
        expense_df = df[df["Type"] == "Expense"]
        if not expense_df.empty:
            fig = px.pie(expense_df, values='Amount', names='Category', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add some expenses to see the chart!")

    with right_col:
        st.subheader("🤖 AI Budget Coach")
        # Simple AI logic for student feedback
        if balance < 0:
            st.error("⚠️ **Coach Says:** You're spending more than you earn! Look for 'Food & Snacks' cuts.")
        elif total_expenses > (total_earnings * 0.8) and total_earnings > 0:
            st.warning("🧐 **Coach Says:** You've spent 80% of your income. Time to pause the subscriptions?")
        elif balance > 0:
            st.success("🌟 **Coach Says:** Great job! You have a surplus. Consider putting $50 into savings.")
        else:
            st.info("Add data to get personalized AI tips.")

    # --- RECENT TRANSACTIONS ---
    st.subheader("📝 Recent History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
    
    if st.button("Clear All Data"):
        st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
        st.rerun()
else:
    st.info("Welcome! Start by adding your first income or expense in the sidebar. 👈")