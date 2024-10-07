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
    else:
        fake = Faker()

    if name_types['surnames']:
        name = fake.last_name().lower()
    elif name_types['nicknames']:
        name = fake.first_name().lower()
    elif name_types['brand_names']:
        name = fake.company().lower().replace(' ', '')
    elif name_types['place_names']:
        name = fake.city().lower()
    elif name_types['pen_names']:
        name = f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    elif name_types['stage_names']:
        name = f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    elif name_types['usernames']:
        name = fake.user_name().lower()
    elif name_types['scientific_names']:
        name = f"species_{fake.word()}".lower()
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
