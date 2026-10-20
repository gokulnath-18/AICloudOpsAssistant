
from flask import Flask, render_template, request

from agents.log_agent import analyze_log
from agents.aws_agent import analyze_aws_issue
from agents.cloudwatch_agent import fetch_recent_logs
from agents.ai_explanation_agent import generate_ai_explanation


app = Flask(__name__)

# Test Lambda CloudWatch log group
LOG_GROUP_NAME = "/aws/lambda/cloudops-error-test"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check whether a file was uploaded
    if "logfile" not in request.files:
        return render_template(
            "index.html",
            error="No log file selected."
        )

    file = request.files["logfile"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="No log file selected."
        )

    # Read the uploaded log file
    try:
        log_content = file.read().decode("utf-8")

    except UnicodeDecodeError:
        return render_template(
            "index.html",
            error="Unable to read the file. Please use a UTF-8 text file."
        )

    except Exception:
        app.logger.exception("Failed to read uploaded log file")
        return render_template(
            "index.html",
            error="Unable to read the uploaded log file."
        )

    if not log_content.strip():
        return render_template(
            "index.html",
            error="The uploaded log file is empty."
        )

    return analyze_and_display(log_content)


@app.route("/analyze-cloudwatch", methods=["POST"])
def analyze_cloudwatch():

    # Fetch recent logs from the configured CloudWatch log group
    try:
        log_content = fetch_recent_logs(
            LOG_GROUP_NAME,
            minutes=120
        )

        if (
            not log_content
            or log_content.startswith("No log events found")
        ):
            return render_template(
                "index.html",
                error=log_content or "No CloudWatch logs found."
            )

        return analyze_and_display(log_content)

    except Exception:
        app.logger.exception("CloudWatch log retrieval failed")
        return render_template(
            "index.html",
            error=(
                "Unable to fetch CloudWatch logs. "
                "Check your AWS credentials, permissions, "
                "region, and CloudWatch log group."
            )
        )


def analyze_and_display(log_content):

    # Step 1: Detect the error using the Log Agent
    result = analyze_log(log_content)

    # Step 2: Generate the AWS-specific explanation
    aws_result = analyze_aws_issue(
        result["service"],
        result["error_type"],
        result["issue"]
    )

    # Step 3: Generate an AI explanation using local Ollama
    ai_result = generate_ai_explanation(
        service=result["service"],
        error_type=result["error_type"],
        issue=result["issue"],
        evidence=result["evidence"],
        aws_explanation=aws_result["aws_explanation"],
        recommendation=aws_result["recommendation"]
    )

    # Step 4: Display all results in the dashboard
    return render_template(
        "index.html",
        service=result["service"],
        error_type=result["error_type"],
        issue=result["issue"],
        status=result["status"],
        evidence=result["evidence"],
        error_message=result["error_message"],
        error_file=result["error_file"],
        error_line=result["error_line"],
        aws_explanation=aws_result["aws_explanation"],
        recommendation=aws_result["recommendation"],
        ai_explanation=ai_result["explanation"],
        ai_error=ai_result["error"]
    )


if __name__ == "__main__":
    app.run(debug=True)
