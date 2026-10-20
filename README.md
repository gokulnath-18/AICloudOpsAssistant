
# AI Cloud Operations Assistant

An AI-powered cloud operations assistant that analyzes application logs, detects common AWS errors, retrieves recent CloudWatch logs, and generates troubleshooting explanations using a locally running Ollama model.

## Features

- Log Agent for detecting common errors and extracting diagnostic evidence.
- AWS Agent for rule-based AWS troubleshooting recommendations.
- CloudWatch Agent for retrieving recent AWS CloudWatch log events.
- AI Explanation Agent powered by Ollama and Llama 3.2.
- Flask web dashboard for displaying analysis results.
- Local AI inference without requiring a paid LLM API.

## Architecture

Log File / AWS CloudWatch
          |
          v
   Flask Web Application
          |
          v
       Log Agent
          |
          v
       AWS Agent
          |
          v
  AI Explanation Agent
     (Ollama / Llama 3.2)
          |
          v
   Web Dashboard Results

## Technology Stack

- Python
- Flask
- AWS Lambda
- Amazon CloudWatch Logs
- Boto3
- Ollama
- Llama 3.2
- HTML and CSS

## Prerequisites

- Python 3.10 or later
- AWS account with an existing CloudWatch log group
- AWS credentials configured locally with permission to read CloudWatch logs
- Ollama installed and running
- The llama3.2:latest model downloaded

## Installation

1. Clone this repository.

   git clone YOUR_GITHUB_REPOSITORY_URL

2. Enter the project folder.

   cd AICloudOpsAssistant

3. Create a virtual environment.

   python -m venv venv

4. Activate it on Windows PowerShell.

   .\venv\Scripts\Activate.ps1

5. Install dependencies.

   python -m pip install -r requirements.txt

6. Download the AI model if needed.

   ollama pull llama3.2:latest

7. Start Ollama and run the application.

   python app.py

8. Open the dashboard.

   http://127.0.0.1:5000

## AWS Configuration

Configure AWS credentials locally using an appropriate AWS CLI profile or another supported credential provider.

Ensure that the configured AWS region and log group match the values in the application. The configured identity needs permission to read CloudWatch log events.

Do not commit AWS access keys or other credentials to this repository.

## Testing

Run the AI explanation agent test:

   python test_ai_explanation.py

Ensure Ollama is running before executing the test.

## Safety

This project analyzes logs and generates recommendations. It does not automatically apply fixes to AWS resources.

## Future Improvements

- Read-only AWS resource health checks
- Error severity classification
- Analysis history
- Interactive AI troubleshooting
- More AWS service integrations

## Author

Gokulnath V
