# AWS S3 to QuickSight Serverless Data Pipeline

This project demonstrates an automated, scalable, and event-driven data pipeline built entirely on AWS. It processes raw data files from an on-premise source, transforms them using Amazon Athena, and visualizes the curated data in Amazon QuickSight. The pipeline leverages AWS services such as Lambda, Step Functions, S3, SQS, and SNS to orchestrate a seamless and reliable data flow.

![Architecture Diagram](https://tinyurl.com/yrwavs7x)

---

## 🚀 Overview

The pipeline is designed to:
- Process raw files uploaded from on-premise systems
- Perform data transformation using SQL queries in Athena
- Deliver curated Parquet datasets to analysts via QuickSight
- Automatically notify business and support teams based on success/failure

---

## 🧩 Architecture Components

### 📂 On-Premise Data Source
Raw data files are generated and uploaded to AWS using the AWS Command Line Interface (CLI).

### 🪣 Amazon S3 (Input Bucket)
Acts as the landing zone for incoming raw data files from the on-premise system.

### 🧠 AWS Lambda (Trigger)
Listens for new file uploads in the S3 input bucket. Once a predefined number of files (e.g., 5 files) are detected, it triggers the AWS Step Functions workflow.

### 🔁 AWS Step Functions (Orchestration)
Manages the end-to-end workflow of data processing:
- **Athena StartQueryExecution**: Runs a SQL query to transform and join data.
- **Wait State**: Delays execution to allow the query to complete.
- **Athena GetQueryExecution**: Checks the status of the query.
- **Choice State**:
  - On success, sends a notification to Data Analysts.
  - On failure, alerts the Support Team.

### 📂 Amazon S3 (Output Bucket)
Stores the transformed, curated data in Parquet format.

### 📬 Amazon SQS (Queue)
Receives events when new Parquet files are added to the output bucket.

### ⚙️ AWS Lambda (QuickSight Trigger)
Triggered by SQS messages to refresh the Amazon QuickSight dataset.

### 📊 Amazon QuickSight
Visualizes curated datasets via dashboards, enabling business users to derive insights.

### 🔔 Amazon SNS (Notifications)
- **To Support Team**: Alerts in case of Athena query failure.
- **To Business/Data Team**: Confirms successful data load and availability in QuickSight.

---

## ✅ Features

- Fully serverless and scalable
- Event-driven architecture using native AWS services
- Automated data transformation using SQL
- Hands-free dashboard refresh in QuickSight
- Notifications to relevant stakeholders
- Supports Parquet file output for efficient querying and storage

---

## 📸 Architecture Diagram

You can view the full architecture diagram [here](https://tinyurl.com/yrwavs7x).

---

## 🛠 Technologies Used

- AWS S3
- AWS Lambda
- AWS Step Functions
- Amazon Athena
- Amazon SQS
- Amazon SNS
- Amazon QuickSight
- AWS CLI

---

## 📈 Use Cases

- Business intelligence reporting
- Near real-time data refresh workflows
- Event-driven data pipelines
- Serverless data transformation and orchestration

---

## 📬 Contact

For more information or feedback, feel free to reach out via [LinkedIn](http://www.linkedin.com/in/praveenkumarkuppili) or check out the repository and give it a ⭐ if you find it useful.

---

