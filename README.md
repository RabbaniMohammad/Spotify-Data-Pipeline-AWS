# Spotify Data Pipeline

---

## Overview

The **Spotify Data Pipeline** is a scalable and automated AWS-based data pipeline designed to process and analyze Spotify-like data using modern cloud technologies. It leverages **AWS Step Functions** to orchestrate the entire ETL workflow, including data processing with **Glue**, storage in **S3**, querying with **Athena**, and visualization using **QuickSight**.

---

## Technologies Used

### AWS Services
- **AWS Step Functions**: Orchestrates the ETL workflow, including Glue jobs and crawlers.
- **AWS Glue**: Performs ETL operations to transform and clean data.
- **AWS S3**: Stores raw, processed, and final data.
- **Amazon Athena**: Queries the processed data stored in S3.
- **Amazon QuickSight**: Visualizes insights from the processed data.
- **AWS SNS**: Sends notifications for workflow status updates.
- **AWS CloudWatch**: Monitors logs for job performance and debugging.

---

## Data Flow and Components

### Input Files
1. **albums.csv**: Album metadata such as album name and artist association.
2. **tracks.csv**: Track details like track ID, album association, and duration.
3. **artists.csv**: Artist-level information, including artist ID and name.

### S3 Buckets
- **Staging**: `s3://medalian/staging/`
  - Holds intermediate processed data.
- **Data Warehouse**: `s3://medalian/datawarehouse/`
  - Stores the final Parquet files in a compressed Snappy format.

---

## Workflow

### Step Function Workflow
1. **Start Glue ETL Job**:
   - Reads raw CSV files (`albums.csv`, `tracks.csv`, and `artists.csv`) from the **staging bucket**.
   - Joins the data:
     - `albums.csv` with `artists.csv` on `artist_id`.
     - The joined result with `tracks.csv` on `track_id`.
   - Removes duplicate columns and applies transformations.
   - Writes the processed data to the **data warehouse bucket** in Parquet format (Snappy compression).

2. **Start Glue Crawler**:
   - Updates the table schema in the Glue Data Catalog for the processed data.

3. **Monitor and Notifications**:
   - Uses **SNS** to notify success or failure of the ETL pipeline.
   - Logs job statuses and errors via **CloudWatch**.

### Queries and Visualization
1. **Amazon Athena**:
   - Queries the processed data stored in S3.
   - Example Query:
     ```sql
     SELECT artist_name, COUNT(track_id) AS total_tracks 
     FROM datawarehouse.tracks
     GROUP BY artist_name 
     ORDER BY total_tracks DESC;
     ```
2. **Amazon QuickSight**:
   - Builds interactive dashboards to visualize:
     - Most popular artists.
     - Track counts by album.
     - Trends in track durations.

---

## Features
- **Metadata-Driven Architecture**: Ensures flexibility in schema handling and updates.
- **Real-Time Monitoring**: Tracks job statuses and logs using **CloudWatch**.
- **Automated Notifications**: Notifies stakeholders of pipeline status via **SNS**.
- **Seamless Integration**: Orchestrates ETL processes and data catalog updates using Step Functions.

---

## Deployment Steps

### Prerequisites
1. Set up **S3 buckets** for staging, processed, and data warehouse storage.
2. Create **IAM roles** with necessary permissions for Glue, S3, Athena, and SNS.
3. Configure Glue crawlers for the processed data.

### Commands
1. **Deploy Step Functions**:
   - Use the AWS Management Console or CLI to define and deploy the Step Function workflow.
2. **Run ETL Pipeline**:
   - Start the Step Function to trigger the Glue ETL job and crawler.
3. **Monitor Logs**:
   - Access **CloudWatch** to review pipeline logs.
4. **Query Data**:
   - Use Athena to query the processed data stored in S3.
5. **Visualize in QuickSight**:
   - Connect QuickSight to Athena and create visual dashboards.

---


---

## Conclusion

The **Spotify Data Pipeline** efficiently processes and analyzes Spotify-like data using AWS services. With a focus on scalability, automation, and real-time insights, this project showcases the power of **Step Functions**, **Glue**, **Athena**, and **QuickSight** in building robust data pipelines.

---

