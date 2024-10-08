import os
from datetime import datetime

def create_and_move_file(emails, folder, base_filename, label):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/{base_filename}_{label}_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        for email in emails:
            file.write(f"{email}\n")
    
    return filename

# Example usage
if __name__ == "__main__":
    # Dummy data for testing
    example_emails = ["test1@example.com", "test2@example.com"]
    create_and_move_file(example_emails, "gmail", "test_gmail", "gmail")
    create_and_move_file(example_emails, "outlook", "test_outlook", "outlook")
