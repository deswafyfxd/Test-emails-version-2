from name_generator import generate_name, generate_dot_variations

def generate_emails(base_email, name_types, add_numbers, total_count=10, plus_count=0, dot_variation_count=0, plus_dot_combination_count=0, domain="", plus_enabled=True, dot_enabled=True, plus_dot_combination_enabled=True):
    username, domain = base_email.split('@')
    plus_emails = set()
    dot_emails = set()
    plus_dot_emails = set()

    if total_count <= 10 or (plus_enabled and not plus_count and not dot_variation_count and not plus_dot_combination_count):
        plus_count = total_count

    count = 0
    while count < plus_count and plus_enabled:
        plus_emails.add(f"{username}+{generate_name(name_types)}@{domain}")
        count += 1

    count = 0
    while count < dot_variation_count and dot_enabled:
        variation = generate_dot_variations(username)
        for var in variation:
            if count >= dot_variation_count:
                break
            dot_emails.add(f"{var}@{domain}")
            count += 1

    count = 0
    while count < plus_dot_combination_count and plus_dot_combination_enabled:
        variation = generate_dot_variations(username)
        for var in variation:
            if count >= plus_dot_combination_count:
                break
            plus_dot_emails.add(f"{var}+{generate_name(name_types)}@{domain}")
            count += 1

    emails = list(plus_emails) + list(dot_emails) + list(plus_dot_emails)
    return emails[:total_count]

def write_to_file(filename, emails):
    with open(filename, 'w') as f:
        for email in emails:
            f.write(f"{email}\n")
