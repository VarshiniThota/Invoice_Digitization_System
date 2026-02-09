# 📄 Invoice Digitization System (AWS + AI)

A serverless invoice processing system that allows users to upload invoice PDFs via a Streamlit web application. Uploaded invoices are automatically processed using an event-driven AWS architecture to extract structured invoice data and present it in a human-readable format with Excel export support.

# 🚀 Project Overview

Companies receive invoices in multiple formats (PDFs, images) from different vendors. Manually extracting invoice details is time-consuming and error-prone.
This project automates the entire process using AWS managed services and a lightweight UI.

#🔧 AWS Services Used

- **Amazon S3** – Stores invoice PDFs and extracted results  
- **AWS Lambda** – Serverless backend processing  
- **Amazon Textract (AnalyzeExpense)** – AI-powered invoice data extraction  
- **AWS IAM** – Secure access using IAM users and roles  
- **Amazon CloudWatch** – Logging and monitoring

  ## 🖥️ Application Features
- Upload invoice PDFs through a Streamlit web interface  
- Automatic invoice processing using S3-triggered Lambda  
- Extracted invoice summary (vendor, date, total amount, etc.)  
- Line items displayed in tabular format  
- Download extracted invoice data as Excel  
- Designed with AWS Free Tier cost awareness  

## 🧪 About the S3 Upload Script (Important)

The script located at:
aws_s3\s3\invoice_uploads.py
was created **only for testing and learning purposes**.

It was used to:
- Verify IAM permissions
- Test S3 bucket creation
- Manually trigger Lambda during early development

⚠️ **This script is NOT used in the final application.**

The actual application uploads files using the Streamlit UI.

## 🌐 How Streamlit Uploads Files to AWS S3

1. The Streamlit application uses **boto3** (AWS SDK for Python).
2. AWS credentials are picked up automatically from the local AWS CLI configuration (`aws configure`).
3. When a user uploads an invoice and clicks **Upload Invoice**:
   - The file is sent directly from the browser to Amazon S3.
   - The invoice is stored in the `raw/` folder of the S3 bucket.
4. The S3 upload triggers an **S3 PUT event**.
5. The event invokes the Lambda function.
6. Lambda calls **Amazon Textract (AnalyzeExpense)** to extract structured invoice data.
7. The extracted output is saved back to S3 in the `json/` folder.
8. Streamlit fetches the processed output from S3 and displays it to the user.
 ## 🔁 Lambda Function Deployment Note

The Lambda function code included in this repository was written and tested locally, but it was **deployed and executed using the AWS Lambda Console**.

For this project:
- The Lambda function was created directly in the AWS Console.
- The code from `lambda/lambda_function.py` was copied into the Lambda editor.
- An S3 trigger was configured via the AWS Console to invoke the function on invoice uploads.
- The Lambda execution role was attached to allow access to Amazon S3, Amazon Textract, and CloudWatch Logs.

This approach was intentionally chosen to:
- Better understand AWS Lambda configuration and triggers
- Practice IAM role attachment and permissions
- Gain hands-on experience with AWS Console–based serverless workflows

The Lambda code in this repository represents the **exact logic used in the deployed function**.


## 🔐 Security & Authentication

- No AWS credentials are hardcoded in the source code.
- Streamlit uses AWS credentials configured via AWS CLI (local execution).
- Lambda uses an IAM execution role for secure service access.
- S3 buckets block all public access.

## 💰 Cost Considerations

- Designed to stay within AWS Free Tier limits.
- Tested using single-page invoice PDFs.
- All AWS resources are deleted after testing to avoid unexpected charges.
## 🧠 Key Learnings

- Event-driven serverless architecture  
- IAM users vs IAM roles  
- AI-based document processing with Amazon Textract  
- Secure AWS access without hardcoded credentials  
- Cost-aware cloud development  
- UI + Cloud + AI integration  

## 📌 Future Enhancements
- Multi-invoice dashboard
- Processing status tracking
- CSV export in addition to Excel
- Authentication and user management
- Cloud deployment of Streamlit application

## 🏁 Conclusion

This project demonstrates a real-world serverless cloud solution for invoice automation using AWS and AI services, with a focus on clean architecture, security, scalability, and cost control.


