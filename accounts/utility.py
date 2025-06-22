import random 

def generate_username(first_name, last_name):
    """
    Generate a random username based on the user's first and last name.
    """
    random_number = random.randint(100, 999)
    username = f"{first_name + last_name}.".lower() + str(random_number)
    return username