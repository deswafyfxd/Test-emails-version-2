from faker import Faker
import random

fake = Faker()

def generate_name(name_types, add_numbers):
    if name_types['personal_given_names']['indian']:
        fake = Faker('en_IN')
    elif name_types['personal_given_names']['western']:
        fake = Faker('en_US')
    elif name_types['personal_given_names']['japanese']:
        fake = Faker('en_US')
    elif name_types['personal_given_names']['chinese']:
        fake = Faker('en_US')
    elif name_types['personal_given_names']['other']:
        fake = Faker('en_US')
    elif name_types['surnames']:
        return fake.last_name().lower()
    elif name_types['nicknames']:
        return fake.first_name().lower()
    elif name_types['brand_names']:
        return fake.company().lower().replace(' ', '')
    elif name_types['place_names']:
        return fake.city().lower()
    elif name_types['pen_names']:
        return f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    elif name_types['stage_names']:
        return f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    elif name_types['usernames']:
        return fake.user_name().lower()
    elif name_types['scientific_names']:
        return f"species_{fake.word()}".lower()
    else:
        name = fake.first_name().lower()  # Default to personal names if all false

    if add_numbers['enabled']:
        digits = add_numbers.get('digits', 2)
        number = ''.join(random.choices('0123456789', k=digits))
        name = f"{name}{number}"

    return name

def generate_dot_variations(username):
    variations = set()
    for i in range(1, len(username)):
        variations.add(username[:i] + '.' + username[i:])
    return variations
