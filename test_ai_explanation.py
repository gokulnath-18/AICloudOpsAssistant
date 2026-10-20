
from agents.ai_explanation_agent import generate_ai_explanation


result = generate_ai_explanation(
    service="AWS Lambda",
    error_type="ValueError",
    issue="The function encountered an invalid value",
    evidence=[
        "DEMO_ERROR: intentionally generating a test exception",
        "[ERROR] ValueError: DEMO_ERROR: simulated invalid input",
        'File "/var/task/lambda_function.py", line 6, in lambda_handler'
    ],
    aws_explanation=(
        "The Lambda function encountered a value that "
        "its application code could not accept or process."
    ),
    recommendation=(
        "Inspect the traceback and validate input values."
    )
)

if result["success"]:
    print("\nAI EXPLANATION\n")
    print(result["explanation"])
else:
    print("\nAI AGENT ERROR\n")
    print(result["error"])
