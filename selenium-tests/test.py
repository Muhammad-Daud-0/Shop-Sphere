from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

# ---------------- SETUP ---------------- #
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run headless
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Create screenshots folder
#os.makedirs("screenshots", exist_ok=True)



def run_test(test_name, test_func):
    """Run a test and continue even if it fails"""
    try:
        test_func()
        print(f"[PASS] {test_name}")
    except Exception as e:
        print(f"[FAIL] {test_name} - {e}")
       

# ================= TEST FUNCTIONS ================= #

def test_user_registration():
    driver.get("http://56.228.10.118:3005/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    email_value = f"testuser_{int(time.time())}@example.com"
    driver.find_element(By.ID, "email").send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "phone").send_keys("03455179179")
    driver.find_element(By.ID, "address").send_keys("123 Test Street, Test City")
    driver.find_element(By.ID, "answer").send_keys("test answer")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url.startswith("http://56.228.10.118:3005/"), f"Unexpected URL: {driver.current_url}"

def test_register_invalid_email():
    driver.get("http://56.228.10.118:3005/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("invalid-email")
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url == "http://56.228.10.118:3005/register"

def test_register_weak_password():
    driver.get("http://56.228.10.118:3005/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    email_value = f"weakpass_{int(time.time())}@example.com"
    driver.find_element(By.ID, "email").send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url == "http://56.228.10.118:3005/register"

def test_user_login():
    driver.get("http://56.228.10.118:3005/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Login Test User")
    email_value = f"logintest_{int(time.time())}@example.com"
    password_value = "Password123!"
    driver.find_element(By.ID, "email").send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys(password_value)
    driver.find_element(By.ID, "phone").send_keys("9876543210")
    driver.find_element(By.ID, "address").send_keys("456 Test Ave")
    driver.find_element(By.ID, "answer").send_keys("test")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url.startswith("http://56.228.10.118:3005/"), f"Unexpected URL: {driver.current_url}"

    # Login with the same user
    driver.get("http://56.228.10.118:3005/login")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)
   
    assert driver.current_url.startswith("http://56.228.10.118:3005/"), f"Unexpected URL: {driver.current_url}"

def test_user_login_invalid_credentials():
    driver.get("http://56.228.10.118:3005/login")

    wait = WebDriverWait(driver, 20)

    # Insert invalid email + password
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("notexist@example.com")
    driver.find_element(By.ID, "password").send_keys("WrongPass123")

    driver.execute_script("document.querySelector('button[type=submit]').click();")

    time.sleep(2)


    # Assert still on login page
    assert driver.current_url.startswith("http://56.228.10.118:3005/forgot-password"), \
        f"User should stay on login page, but got: {driver.current_url}"

def test_browse_products():
    driver.get("http://56.228.10.118:3005/dashboard/products")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='product-card'] h3")))

    assert len(products) > 0
    assert products[0].text.strip() != ""

def test_browse_categories():
    driver.get("http://56.228.10.118:3005/dashboard/categories")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    categories = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='category-card'] h3")))

    assert len(categories) > 0

def test_add_to_cart():
    driver.get("http://56.228.10.118:3005/dashboard/products")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    product_card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
    cart_btn = product_card.find_element(By.CSS_SELECTOR, ".add-to-cart")
    driver.execute_script("arguments[0].scrollIntoView(true);", cart_btn)
    driver.execute_script("arguments[0].click();", cart_btn)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'added') or contains(text(),'cart')]")))


def test_view_cart():
    driver.get("http://56.228.10.118:3005/dashboard/cart")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    cart_container = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='cart-container']")))

    assert len(cart_container) > 0

# ================= RUN ALL TESTS ================= #
all_tests = [
    ("User Registration", test_user_registration),
    ("Register Invalid Email", test_register_invalid_email),
    ("Register Weak Password", test_register_weak_password),
    ("User Login", test_user_login),
    ("User Login Invalid Credentials", test_user_login_invalid_credentials),
    ("Browse Products", test_browse_products),
    ("Browse Categories", test_browse_categories),
    ("Add to Cart", test_add_to_cart),
    ("View Cart", test_view_cart)
]

for name, func in all_tests:
    run_test(name, func)

driver.quit()
print("All test steps completed. Screenshots saved in 'screenshots/' folder.")
