import os
import apprise
from datetime import datetime

def send_to_discord(gmail_emails, outlook_emails, webhook_url):
    apobj = apprise.Apprise()
    apobj.add(webhook_url)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    gmail_plus = [email for email in gmail_emails if "+" in email and "." not in email]
    gmail_dot = [email for email in gmail_emails if "." in email and "+" not in email]
    gmail_plus_dot = [email for email in gmail_emails if "+" in email and "." in email]
    
    outlook_plus = [email for email in outlook_emails if "+" in email]

    message = (
        f"**Date and Time:** {timestamp}\n\n"
        "**Gmail Emails:**\n"
        "**Plus and Plus Dot Combination:**\n" + "\n".join(gmail_plus) + "\n" + "\n".join(gmail_plus_dot) + "\n\n"
        "**Dot Variation:**\n" + "\n".join(gmail_dot) + "\n\n"
        "**Outlook Emails:**\n"
        "**Plus:**\n" + "\n".join(outlook_plus)
    )

    apobj.notify(body=message, title="Generated Emails")

def send_txt_to_discord(emails, webhook_url):
    apobj = apprise.Apprise()
    apobj.add(webhook_url)
    
    with open("generated_emails.txt", 'w') as file:
        for email in emails:
            file.write(email + "\n")
    
    apobj.notify(
        body="Generated emails are attached.",
        title="Generated Emails",
        attach={"file": "generated_emails.txt"}
    )
