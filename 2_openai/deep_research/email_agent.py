# import os
# from typing import Dict

# import sendgrid
# from sendgrid.helpers.mail import Email, Mail, Content, To
# from agents import Agent, function_tool


# @function_tool
# def send_email(subject: str, html_body: str) -> Dict[str, str]:
#     """Send an email with the given subject and HTML body"""
#     sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
#     from_email = Email("alekar.samruddhi@gmail.com")  # put your verified sender here
#     to_email = To("samalekar2@gmail.com")  # put your recipient here
#     content = Content("text/html", html_body)
#     mail = Mail(from_email, to_email, subject, content).get()
#     response = sg.client.mail.send.post(request_body=mail)
#     print("Email response", response.status_code)
#     return "success"


# INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
# You will be provided with a detailed report. You should use your tool to send one email, providing the 
# report converted into clean, well presented HTML with an appropriate subject line."""

# email_agent = Agent(
#     name="Email agent",
#     instructions=INSTRUCTIONS,
#     tools=[send_email],
#     model="gpt-4o-mini",
# )

import os

import sendgrid
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail

load_dotenv()


def send_email(report_text: str) -> int:
    sg = sendgrid.SendGridAPIClient(
        api_key=os.getenv("SENDGRID_API_KEY")
    )

    message = Mail(
        from_email="alekar.samruddhi@gmail.com",
        to_emails="samalekar2@gmail.com",
        subject="Deep Research Report",
        html_content=f"""
<html>
<body style="font-family: Arial, sans-serif;">
<pre style="white-space: pre-wrap;">
{report_text}
</pre>
</body>
</html>
""",
    )

    response = sg.send(message)

    print("Email status:", response.status_code)

    return response.status_code