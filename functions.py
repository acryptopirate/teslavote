import time
from datetime import datetime
import string
import random
from helium import *
from names import *
from selenium.webdriver.common.by import By
from python_anticaptcha import AnticaptchaClient, ImageToTextTask

captcha_api_key = '0c42abc950395a7fdded4e3a74516cf2'
male_percentage = 80

def navigate_to_create_account():
    # click('Vote on Proposed Locations')
    # time.sleep(1)
    # if Text('Middle-East').exists():
    #     click('Region & Language')
    # time.sleep(1)
    click('Log In To Vote')
    time.sleep(2)
    click('Create Account')
    time.sleep(1)


def select_region():
    click('Select Region')
    time.sleep(1)
    write('Other Europe')
    time.sleep(1)
    click('Other Europe')
    time.sleep(1)


def save_captcha_image():
    image_element = Image(alt='Type in the code above')
    image_png = image_element.web_element.screenshot_as_png

    with open("image.png", "wb") as fh:
        fh.write(image_png)


def resolve_captcha():
    captcha_fp = open('image.png', 'rb')
    client = AnticaptchaClient(captcha_api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()

    return job.get_captcha_text()


def create_account_first_step(first_name, last_name, captcha_text):
    click('First Name')
    write(first_name)
    click('Last Name')
    write(last_name)
    click('Enter the characters in the image')
    write(captcha_text)
    click('Next')


def pick_random_gender():
    if random.random() < male_percentage / 100:
        return "m"
    return "f"


def pick_random_first_name(gender):
    if gender == 'm':
        return random.choice(names['men'])
    if gender == 'f':
        return random.choice(names['woman'])

    return False


def pick_random_last_name(gender):
    if gender == 'm':
        return random.choice(names['lasts'])
    if gender == 'f':
        return random.choice(names['lasts']) + "a"

    return False


def generate_email_finish():
    return random.choice(string.ascii_lowercase) + random.choice(string.digits) + random.choice(string.digits)


def generate_password():
    # Define the character sets
    letters = string.ascii_letters  # a-zA-Z
    numbers = string.digits         # 0-9
    special_chars = "!@#$%^&*()_-+={}[]|\:;\"'<>,.?/~`"  # Special characters

    # Ensure at least one character from each set
    password = [
        random.choice(letters),
        random.choice(numbers),
        random.choice(special_chars)
    ]

    # Fill the rest of the password length with random choices from all character sets
    remaining_length = max(10, len(password)) - len(password)
    password.extend(random.choices(letters + numbers + special_chars, k=remaining_length))

    # Shuffle the password list to mix up character types
    random.shuffle(password)

    # Convert the list to a string and return
    return ''.join(password)


def generate_email(first_name, last_name):
    # Simplify names (remove spaces, convert to lowercase)
    simple_first = first_name.lower().replace(' ', '')
    simple_last = last_name.lower().replace(' ', '')

    # Define common email domains and their relative frequencies
    domains = {
        'gmail.com': 60,  # example percentage
        'yahoo.com': 20,
        'hotmail.com': 10,
        'dir.bg': 5,
        'abv.bg': 5
    }

    # Choose a domain based on the provided frequencies
    domain_list = [domain for domain in domains for _ in range(domains[domain])]
    domain = random.choice(domain_list)
    email_finish = generate_email_finish()
    # Generate the email format
    email_formats = [
        f"{simple_first}.{simple_last}{email_finish}@{domain}",
        f"{simple_first}{simple_last[0]}{email_finish}@{domain}",
        f"{simple_first[0]}{simple_last}{email_finish}@{domain}"
    ]
    email = random.choice(email_formats)

    return email


def create_account_second_step(email, password):
    click('Email')
    write(email)
    time.sleep(1)
    click('Password')
    write(password)
    time.sleep(1)
    click('Confirm Password')
    write(password)
    time.sleep(1)
    click('Create Account')
    time.sleep(3)


def vote():
    max_retries = 6
    current_retries = 1

    while current_retries < max_retries:
        print(current_retries)

        if Text('Log In To Vote').exists():
            click('Log In To Vote')
            time.sleep(3)

        if Text('Something went wrong, try again later'):
            refresh()
            time.sleep(3)

        if Text('Veliko Tarnovo, Bulgaria').exists():
            click('Veliko Tarnovo, Bulgaria')
            time.sleep(3)

        if Text('Vote').exists():
            click('Vote')
            time.sleep(3)

        if Text('Voted On ' + datetime.now().strftime("%b %d, %Y")).exists():
            print('VOTED')
            current_retries = max_retries

        current_retries = current_retries + 1



