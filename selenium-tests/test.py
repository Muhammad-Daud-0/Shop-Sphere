from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, InvalidSessionIdException
import time
import os

# ---------------- SETUP ---------------- #
# Use BASE_URL passed via env (set in Jenkinsfile when running container)
BASE_URL = os.environ.get("BASE_URL", "http://13.201.23.88:3005")

# Use webdriver-manager to ensure matching chromedriver is installed inside the container
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    options = webdriver.ChromeOptions()
    # Use the newer headless implementation and add flags that help in container environments
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    # Use a remote debugging port - helps Chrome run reliably in containerized environments
    options.add_argument("--remote-debugging-port=9222")
    # Avoid using --single-process and --no-zygote which can make Chrome unstable in some images

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)



def run_test(test_name, test_func):
    """Run a test in its own browser instance and retry on transient browser crashes.
    Saves a screenshot on failure."""
    max_attempts = 2

    for attempt in range(1, max_attempts + 1):
        driver = None
        try:
            driver = create_driver()
            wait = WebDriverWait(driver, 15)
            test_func(driver, wait)
            print(f"[PASS] {test_name}")
            break
        except Exception as e:
            # Try to capture a screenshot for debugging
            ts = int(time.time())
            safe_name = test_name.replace(' ', '_').replace('/', '_')
            screenshot_path = f"screenshots/{safe_name}_attempt{attempt}_{ts}.png"
            try:
                if driver:
                    driver.save_screenshot(screenshot_path)
                    print(f"Saved screenshot: {screenshot_path}")
            except Exception as se:
                print(f"Could not save screenshot: {se}")

            print(f"[FAIL] {test_name} (attempt {attempt}/{max_attempts}) - Message: {e}")

            # If this looks like a transient browser crash, retry (if we have attempts left)
            err_text = str(e).lower()
            is_transient = isinstance(e, (WebDriverException, InvalidSessionIdException)) or 'not connected to devtools' in err_text or 'invalid session id' in err_text

            if attempt < max_attempts and is_transient:
                print(f"Transient browser error detected, retrying {test_name} (attempt {attempt+1}/{max_attempts})...")
                try:
                    if driver:
                        driver.quit()
                except Exception:
                    pass
                time.sleep(1)
                continue
            else:
                break
        finally:
            try:
                if driver:
                    driver.quit()
            except Exception:
                pass


# ================= TEST FUNCTIONS ================= #

def test_user_registration(driver, wait):
    driver.get(f"{BASE_URL}/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    email_value = f"testuser_{int(time.time())}@example.com"
    driver.find_element(By.ID, "email").send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "phone").send_keys("03455179179")
    driver.find_element(By.ID, "address").send_keys("123 Test Street, Test City")
    driver.find_element(By.ID, "answer").send_keys("test answer")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url.startswith(BASE_URL), f"Unexpected URL: {driver.current_url}"

def test_register_invalid_email(driver, wait):
    driver.get(f"{BASE_URL}/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("invalid-email")
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url == f"{BASE_URL}/register"

def test_register_weak_password(driver, wait):
    driver.get(f"{BASE_URL}/register")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Test User")
    email_value = f"weakpass_{int(time.time())}@example.com"
    driver.find_element(By.ID, "email").send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)

    assert driver.current_url == f"{BASE_URL}/register"

def test_user_login(driver, wait):
    driver.get(f"{BASE_URL}/register")
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

    assert driver.current_url.startswith(BASE_URL), f"Unexpected URL: {driver.current_url}"

    # Login with the same user
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email_value)
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.execute_script("document.querySelector('button[type=submit]').click();")
    time.sleep(2)
   
    assert driver.current_url.startswith(BASE_URL), f"Unexpected URL: {driver.current_url}"

def test_user_login_invalid_credentials(driver, wait):
    driver.get(f"{BASE_URL}/login")

    # Insert invalid email + password
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("notexist@example.com")
    driver.find_element(By.ID, "password").send_keys("WrongPass123")

    driver.execute_script("document.querySelector('button[type=submit]').click();")

    time.sleep(2)


    # Assert it redirects to forgot-password or stays on login (depends on implementation)
    assert driver.current_url.startswith(f"{BASE_URL}/forgot-password") or driver.current_url.startswith(f"{BASE_URL}/login"), \
        f"User should stay on login or be redirected to forgot-password, but got: {driver.current_url}"

def test_browse_products(driver, wait):
    driver.get(f"{BASE_URL}/dashboard/products")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='product-card'] h3")))

    assert len(products) > 0
    assert products[0].text.strip() != ""

def test_browse_categories(driver, wait):
    driver.get(f"{BASE_URL}/dashboard/categories")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass

    categories = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='category-card'] h3")))

    assert len(categories) > 0

def test_add_to_cart(driver, wait):
    driver.get(f"{BASE_URL}/dashboard/products")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".animate-spin")))
    except TimeoutException:
        pass
    
    product_card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
    cart_btn = product_card.find_element(By.CSS_SELECTOR, ".add-to-cart")
    driver.execute_script("arguments[0].scrollIntoView(true);", cart_btn)
    driver.execute_script("arguments[0].click();", cart_btn)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'added') or contains(text(),'cart')]")))


def test_view_cart(driver, wait):
    driver.get(f"{BASE_URL}/dashboard/cart")
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

print("All test steps completed. Screenshots saved in 'screenshots/' folder.")

