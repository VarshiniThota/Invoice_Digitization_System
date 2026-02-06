import streamlit as st
import boto3
import json
import pandas as pd
from io import BytesIO

REGION = "ap-south-1"
BUCKET_NAME = "invoice-bucket-var1307"

s3 = boto3.client("s3", region_name=REGION)
st.set_page_config(page_title="Invoice Digitization System", page_icon="📄")
st.title("📄 Invoice Digitization System")
st.write("Upload an invoice PDF to extract structured data.")

uploaded_file = st.file_uploader("Choose an invoice PDF", type=["pdf"])
def parse_textract_response(data):
    summary = {}
    line_items = []

    expense_doc = data["ExpenseDocuments"][0]

    for field in expense_doc.get("SummaryFields", []):
        label = field.get("LabelDetection", {}).get("Text", "")
        value = field.get("ValueDetection", {}).get("Text", "")
        if label and value:
            summary[label.title()] = value

    for group in expense_doc.get("LineItemGroups", []):
        for item in group.get("LineItems", []):
            row = {}
            for field in item.get("LineItemExpenseFields", []):
                label = field.get("LabelDetection", {}).get("Text", "")
                value = field.get("ValueDetection", {}).get("Text", "")
                if label and value:
                    row[label] = value
            if row:
                line_items.append(row)

    return summary, line_items

if uploaded_file is not None:
    s3_key = f"raw/{uploaded_file.name}"
    output_key = f"json/{uploaded_file.name}.json"

    if st.button("📤 Upload Invoice"):
        try:
            s3.upload_fileobj(uploaded_file, BUCKET_NAME, s3_key)
            st.success("✅ Invoice uploaded successfully")
            st.info("⏳ Processing started… wait 5–10 seconds")
        except Exception as e:
            st.error(f"Upload failed: {e}")

    if st.button("📥 Fetch Extracted Data"):
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=output_key)
            data = json.loads(response["Body"].read())

            summary, line_items = parse_textract_response(data)

            st.subheader("📄 Invoice Summary")
            for k, v in summary.items():
                st.write(f"**{k}**: {v}")

            st.subheader("📦 Line Items")

            if line_items:
                df = pd.DataFrame(line_items)
                st.table(df)
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Invoice Items")

                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="invoice_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No line items found.")

        except s3.exceptions.NoSuchKey:
            st.warning("⚠️ Output not ready yet. Try again in a few seconds.")
        except Exception as e:
            st.error(f"Error fetching output: {e}")
