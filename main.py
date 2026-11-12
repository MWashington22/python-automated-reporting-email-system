import pandas as pd
import sqlite3
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
import traceback
import os
import sys


#Script to load sales data, generate report, create chart, and email results

try:

    print("Step 1: Starting script")

    # 1. Load CSV data
    print("Loading data...")
    file_name = "sales.csv"  # change to sales.xlsx if needed

    if file_name.endswith(".csv"):
        data = pd.read_csv(file_name)
    elif file_name.endswith(".xlsx"):
        data = pd.read_excel(file_name)
    else:
        raise ValueError("Unsupported file type")


    # 2. Connect to SQLite database
    conn = sqlite3.connect("sales.db")

    # 3. Save data to database
    data.to_sql("sales", conn, if_exists="replace", index=False)

    # after loading data
    print("Step 2: Data loaded")

    # 4. Run SQL queries for report
    query_total_sales = """
    SELECT SUM(quantity * price) AS total_sales FROM sales;
    """

    query_top_product = """
    SELECT product, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product
    ORDER BY total_quantity DESC
    LIMIT 1;
    """

    total_sales = pd.read_sql_query(query_total_sales, conn)
    top_product = pd.read_sql_query(query_top_product, conn)

    # after SQL
    print("Step 3: Database complete")

    # 5. Print report
    print("\n📊 AUTO REPORT")
    print("----------------------------")
    print(f"Total Sales: ${total_sales.iloc[0]['total_sales']:.2f}")
    print(f"Top Product: {top_product.iloc[0]['product']}")
    print("----------------------------")

    report_text = f"""
    AUTO SALES REPORT
    ----------------------------
    Total Sales: ${total_sales.iloc[0]['total_sales']:.2f}
    Top Product: {top_product.iloc[0]['product']}
    ----------------------------
    """

    with open("report.txt", "w") as file:
        file.write(report_text)

    print(report_text)

    # Create product sales summary
    query_product_sales = """
    SELECT product, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product;
    """

    product_sales = pd.read_sql_query(query_product_sales, conn)

    # Create bar chart
    plt.figure()
    plt.bar(product_sales["product"], product_sales["total_quantity"])
    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")
    plt.xticks(rotation=45)

    # Save chart as image
    plt.tight_layout()
    plt.savefig("sales_chart.png")
    plt.close()

    # after chart
    print("Step 4: Chart created")

    print("📊 Chart saved as sales_chart.png")

    # Send email report
    print("Step 5: Sending email")

    EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    TO_EMAIL = os.getenv("REPORT_RECIPIENT", EMAIL_ADDRESS)

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Gmail credentials are missing from environment variables.")

    msg = EmailMessage()
    msg["Subject"] = "Automated Sales Report"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(report_text)

    # Attach chart image
    with open("sales_chart.png", "rb") as img:
        msg.add_attachment(
            img.read(),
            maintype="image",
            subtype="png",
            filename="sales_chart.png"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("Report and chart emailed successfully!")

    conn.close()

    print("Step 6: Email sent")

except Exception as e:
    with open("error_log.txt", "w") as f:
        f.write(traceback.format_exc())

plt.close("all")
sys.exit()
