from proxy import *
from functions import *
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = proxy_chrome("geo.iproyal.com", 12321, "ot2MmaCo2OWK913r", "0ea8mqNHv1B5MZH1")
driver.set_window_size(1920, 1080)
set_driver(driver)

try:
    go_to('https://www.tesla.com/en_eu/supercharger-voting')

    element = driver.find_element(By.XPATH, value="//a[@lang='en-EU']")
    time.sleep(1)
    ActionChains(get_driver()).move_to_element(element).perform()
    time.sleep(1)
    click(element)

    navigate_to_create_account()
    select_region()
    save_captcha_image()

    captcha_text = resolve_captcha()
    gender = pick_random_gender()
    first_name = pick_random_first_name(gender)
    last_name = pick_random_last_name(gender)

    create_account_first_step(first_name, last_name, captcha_text)
    password = generate_password()
    email = generate_email(first_name, last_name)

    create_account_second_step(email, password)

    vote()
    driver.quit()
    exit()
except Exception as e:
    print('EXCEPTION')
    print(e)
    driver.quit()
    exit()




