import os
from datetime import datetime
from config_loader import load_config
from email_generator import generate_emails, write_to_file
from notification_sender import send_to_discord, send_txt_to_discord
import subprocess

def push_to_github():
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add generated emails [skip ci]"])
    subprocess.run(["git", "push"])

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
    outlook_plus_dot_combination_count = 0
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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if control_config['gmail']['enabled']:
        gmail_emails = generate_emails(email_config['gmail'], name_types, add_numbers, gmail_total_count, gmail_plus_count, gmail_dot_variation_count, gmail_plus_dot_combination_count, "gmail.com", gmail_plus_enabled, gmail_dot_variation_enabled, gmail_plus_dot_combination_enabled)
        if not os.path.exists('gmail'):
            os.makedirs('gmail')
        gmail_filename = f"gmail/{email_config['gmail'].split('@')[0]}_{timestamp}.txt"
        write_to_file(gmail_filename, gmail_emails)

    if control_config['outlook']['enabled']:
        outlook_emails = generate_emails(email_config['outlook'], name_types, add_numbers, outlook_total_count, outlook_plus_count, outlook_dot_variation_count, outlook_plus_dot_combination_count, "outlook.com", outlook_plus_enabled, outlook_dot_variation_enabled, outlook_plus_dot_combination_enabled)
        if not os.path.exists('outlook'):
            os.makedirs('outlook')
        outlook_filename = f"outlook/{email_config['outlook'].split('@')[0]}_{timestamp}.txt"
        write_to_file(outlook_filename, outlook_emails)

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if control_config['notification']['message_to_discord']:
        send_to_discord(gmail_emails, outlook_emails, discord_webhook_url)

    if control_config['notification']['txt_file_to_discord']:
        send_txt_to_discord(gmail_emails + outlook_emails, discord_webhook_url)

    print(f"github_action enabled: {control_config['github_action']['enabled']}")
    if control_config.get('github_action', {}).get('enabled', False):
        push_to_github()

if __name__ == "__main__":
    main()
