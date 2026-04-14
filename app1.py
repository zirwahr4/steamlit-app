import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 STOCK DASHBOARD")

# -----------------------------
# STEP 1: NUMBER OF STOCKS
# -----------------------------
n = st.number_input("Enter number of stocks:", min_value=1, step=1)

# -----------------------------
# STEP 2: INPUT STOCK DATA
# -----------------------------
stock_name = []
tickers = []
alert_price = []

st.write("### Enter Stock Details")

for i in range(int(n)):
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name", key=f"name{i}")

    with col2:
        symbol = st.text_input("Symbol", key=f"symbol{i}")

    with col3:
        alert = st.number_input("Alert", key=f"alert{i}", min_value=0.0)

    stock_name.append(name)
    tickers.append(symbol)
    alert_price.append(alert)

# -----------------------------
# STEP 3: RUN BUTTON
# -----------------------------
if st.button("Run Dashboard"):

    current_price = []

    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")

            if hist.empty:
                current_price.append(0)
            else:
                current_price.append(round(hist["Close"].iloc[-1], 2))
        except:
            current_price.append(0)

    alerts = []

    for i in range(len(stock_name)):
        if current_price[i] >= alert_price[i]:
            alerts.append(True)
            st.write(f"🚨 ALERT {stock_name[i]} = {current_price[i]}")
        else:
            alerts.append(False)
            st.write(f"OK {stock_name[i]} = {current_price[i]}")

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.write("## STOCK DASHBOARD")

    for i in range(len(stock_name)):
        status = "ALERT" if alerts[i] else "NO ALERT"
        st.write(stock_name[i], current_price[i], alert_price[i], status)

    # -----------------------------
    # GRAPH
    # -----------------------------
    colors = ["red" if a else "green" for a in alerts]

    fig, ax = plt.subplots()
    ax.bar(stock_name, current_price, color=colors)

    st.pyplot(fig)