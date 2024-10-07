from faker import Faker

fake = Faker()

def generate_name(name_types):
    if name_types['personal_given_names']['indian']:
        fake = Faker('en_IN')
        return fake.first_name().lower()
    if name_types['personal_given_names']['western']:
        fake = Faker('en_US')
        return fake.first_name().lower()
    if name_types['personal_given_names']['japanese']:
        fake = Faker('en_US')
        return fake.first_name().lower()
    if name_types['personal_given_names']['chinese']:
        fake = Faker('en_US')
        return fake.first_name().lower()
    if name_types['personal_given_names']['other']:
        fake = Faker('en_US')
        return fake.first_name().lower()
    if name_types['surnames']:
        return fake.last_name().lower()
    if name_types['nicknames']:
        return fake.first_name().lower()
    if name_types['brand_names']:
        return fake.company().lower().replace(' ', '')
    if name_types['place_names']:
        return fake.city().lower()
    if name_types['pen_names']:
        return f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    if name_types['stage_names']:
        return f"{fake.first_name().lower()}_{fake.last_name().lower()}"
    if name_types['usernames']:
        return fake.user_name().lower()
    if name_types['scientific_names']:
        return f"species_{fake.word()}".lower()
    return fake.first_name().lower()  # Default to personal names if all false

def generate_dot_variations(username):
    variations = set()
    for i in range(1, len(username)):
        variations.add(username[:i] + '.' + username[i:])
    return variations
