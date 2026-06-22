from faker import Faker

fake = Faker()


def set_seed(seed: int):
    Faker.seed(seed)


def generate_user():
    return {
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "website": fake.domain_name(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "zipcode": fake.zipcode()
        },
        "company": {
            "name": fake.company()
        }
    }


def generate_post(user_id: int):
    return {
        "userId": user_id,
        "title": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3)
    }   