import random
import string
import os
import yaml
from faker import Faker
import apprise
from datetime import datetime

fake = Faker()

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_name(name_types):
    # ... existing code ...

def generate_dot_variations(username):
    # ... existing code ...

def generate_emails(base_email, name_types, add_numbers, total_count=10, plus_count=0, dot_variation_count=0, plus_dot_combination_count=0, domain="", plus_enabled=True, dot_enabled=True, plus_dot_combination_enabled=True):
    # ... existing code ...

def write_to_file(filename, emails):
    with open(filename, 'w') as f:
        for email in emails:
            f.write(f"{email}\n")

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

def main():
    control_config = load_config('config_control.yml')
    email_config = load_config('config_emails.yml')
    name_types = load_config('config_names.yml')['name_types']
    add_numbers = load_config('config_names.yml')['add_numbers']

    gmail_emails = []
    outlook_emails = []

    gmail_total_count = control_config['gmail']['count']
    outlook_total_count = control_config['outlook']['count']

    gmail_plus_count = control_config['gmail'].get('plus_count', 0)
    gmail_dot_variation_count = control_config['gmail'].get('dot_variation_count', 0)
    gmail_plus_dot_combination_count = control_config['gmail'].get('plus_dot_combination_count', 0)
    gmail_plus_enabled = control_config['gmail'].get('plus', False)
    gmail_dot_variation_enabled = control_config['gmail'].get('dot_variation', False)
    gmail_plus_dot_combination_enabled = control_config['gmail'].get('plus_dot_combination', False)

    outlook_plus_count = control_config['outlook'].get('plus_count', 0)
    outlook_dot_variation_count = control_config['outlook'].get('dot_variation_count', 0)
    outlook_plus_dot_combination_count = 0  # Outlook does not support dots
    outlook_plus_enabled = control_config['outlook'].get('plus', False)
    outlook_dot_variation_enabled = control_config['outlook'].get('dot_variation', False)
    outlook_plus_dot_combination_enabled = control_config['outlook'].get('plus_dot_combination', False)

    if gmail_total_count <= 10:
        gmail_plus_count = gmail_total_count
        gmail_dot_variation_count = 0
        gmail_plus_dot_combination_count = 0

    if outlook_total_count <= 10:
        outlook_plus_count = outlook_total_count
        outlook_dot_variation_count = 0
        outlook_plus_dot_combination_count = 0

    if control_config['gmail']['enabled']:
        gmail_emails = generate_emails(email_config['gmail'], name_types, add_numbers, gmail_total_count, gmail_plus_count, gmail_dot_variation_count, gmail_plus_dot_combination_count, "gmail.com", gmail_plus_enabled, gmail_dot_variation_enabled, gmail_plus_dot_combination_enabled)
        write_to_file("gmail_emails.txt", gmail_emails)

    if control_config['outlook']['enabled']:
        outlook_emails = generate_emails(email_config['outlook'], name_types, add_numbers, outlook_total_count, outlook_plus_count, outlook_dot_variation_count, outlook_plus_dot_combination_count, "outlook.com", outlook_plus_enabled, outlook_dot_variation_enabled, outlook_plus_dot_combination_enabled)
        write_to_file("outlook_emails.txt", outlook_emails)

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if control_config['notification']['message_to_discord']:
        send_to_discord(gmail_emails, outlook_emails, discord_webhook_url)

    if control_config['notification']['txt_file_to_discord']:
        send_txt_to_discord(gmail_emails + outlook_emails, discord_webhook_url)

if __name__ == "__main__":
    main()
