# event-flow-api-tester
This repository contains automated tests for a serverless event driven data pipeline that integrates the Guardian API with SQS, AWS Lambda and S3 bucket.
This framework is based on python-pytest framework and generates detailed test reports via Allure and Pytest-HTML.

# Folder Structure

EVENT-FLOW-API-TESTER
    |
    |---.github/workflow/.yml (Contains the CI/CD steps)    # Handles the CI/CD commands
    |
    |--- aws_pipeline
    |     |
    |     |----guardian/articles.py                         # Get the news articles from Guardian API
    |     |----lambda_aws/lambda_handler.py                 # Check the logs on cloud watch and verify success message after SQS event and S3 file upload
    |     |----s3/s3_handler.py                             # Fetches the latest file name from S3
    |     |----sqs/sqs_handler.py                           # Pushes the news articles to SQS
    |
    |
    |--- reports
    |     |
    |     |----allure-reports                               # Contains the allure report with great UI run on a local server
    |     |----pytest-html-reports                          # Contains the pytest HTML reports good for debugging
    |
    |
    |--- tests
    |     |  
    |     |----test_aws_pipeline.py                         # Contains 3 tests - Full E2E event flow, Service failure - Lambda and S3
    |     |----test_sample.py
    |
    |
    |--- utils
    |     |
    |     |----config.py                                    # Read the configs 
    |
    |--- requirements.txt                                   # Libraies required to build the project
    |--- .gitignore                                         # File names present it are ignored for commit
    |--- pytest.ini                                         # Define pytest metadata    
    |--- README.md                                          # Contains information about the project
    |--- .env                                               # Secrets are kept in this file

# Features
- Fetches the data (News article) from Guardian Public APIs.
- Received data is pushed as JSON data to SQS, AWS SQS is a queue that pushes the data it gets to a destination.
- AWS Lambda process the event after being invoked by SQS. AWS lambda is configured to receive the event from SQS.
- AWS Lambda after extracting the data from queue message pushes the data to S3 bucket.
- Pre-defined S3 bucket stores the data, it gets from AWS Lambda.

# Setup
- To clone use
    Git Repo : git clone https://github.com/shubhankar0417/event-flow-api-tester.git
             : cd event-flow-api-tester
- To install dependencies : pip install -r requirements.txt
- Create a venv : python -m venv venv-eventflow-api
- Activate the venv : source venv-eventflow-api/bin/activate
- Running tests locally : pytest tests/ --html=reports/pytest-html-reports/report.html --self-contained-html --alluredir=reports/allure-reports/
- Generate allure report locally : allure generate reports/allure-reports -o reports/allure-reports/html
                                 : allure open reports/allure-reports/html

# GitHub Actions CI
- CI worklows in .github/workflows/framework.yml
- Runs on push to the main
- Install dependencies
- Executes tests
- Uploads HTML & Allure reports
- Deploys Allure reports to GitHub Pages : https://shubhankar0417.github.io/event-flow-api-tester/
