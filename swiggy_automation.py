from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


def take_screenshot(driver, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    driver.save_screenshot(file_path)


def main():
    options = Options()
    options.add_argument("--start-maximized")  # Optional: Start maximized
    # options.add_argument("--headless")  # Optional: Run headless

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 15)

    driver.get("https://www.shine.com")
    print("Page Title:", driver.title)
    print("Current URL:", driver.current_url)

    # Click Login
    top_login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
    top_login_btn.click()

    # Login form
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "id_email_login")))
    email_field.send_keys("22pa1a4269@vishnu.edu.in")

    password_field = driver.find_element(By.ID, "id_password")
    password_field.send_keys("25jxu!#$fWB9sCD")

    final_login_btn = driver.find_element(By.XPATH, "//*[@id='cndidate_login_widget']/div[1]/form[5]/ul[1]/li[4]/div/button")
    final_login_btn.click()

    wait.until(EC.url_contains("shine.com"))
    take_screenshot(driver, "screenshots/1_login_success.png")
    print("✅ Logged in successfully")

    # Open Search form
    search_container = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ReactContainer']/div[1]/div/div/div[1]/div[1]/div/div/div")))
    search_container.click()
    time.sleep(1.5)

    # Job and location input
    job_input = wait.until(EC.visibility_of_element_located((By.ID, "id_q")))
    job_input.clear()
    job_input.send_keys("Software Tester")

    location_input = wait.until(EC.visibility_of_element_located((By.ID, "id_loc")))
    location_input.clear()
    location_input.send_keys("Hyderabad")

    # Experience selection
    exp_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='search_exp_div']")))
    exp_dropdown.click()
    two_years = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='item-key-2']/label")))
    two_years.click()

    # Search
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frm_adv_srch']/div[2]")))
    search_button.click()
    take_screenshot(driver, "screenshots/2_search_filled.png")
    print("✅ Search submitted")

    time.sleep(4)

    # Click second job card
    second_job_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div[3]/div[2]/div[2]/div/div/div[2]/div[5]")))
    second_job_card.click()

    # Extract job title and company
    job_title_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='jdCardNova']/div[1]/div[1]/div[1]/h1")))
    company_name_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='jdCardNova']/div[1]/div[1]/div[1]/span")))

    print("🧾 Job Title:", job_title_elem.text)
    print("🏢 Company Name:", company_name_elem.text)
    take_screenshot(driver, "screenshots/3_job_detail.png")

    # Apply to the job
    apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id, 'id_apply_')]")))
    apply_btn.click()
    print("✅ Apply button clicked")

    time.sleep(3)

    # Confirm application
    applied_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'id_apply_')]")))
    button_text = applied_btn.text.strip()
    disabled_attr = applied_btn.get_attribute("disabled")
    is_disabled = disabled_attr is not None

    if (button_text.lower() in ["applied", "already applied"]) and is_disabled:
        print(f"✅ Application confirmed. Button shows: {button_text}")
        take_screenshot(driver, "screenshots/4_applied_status_confirmed.png")
    else:
        print(f"⚠ Application status unclear. Button text: {button_text}, disabled: {disabled_attr}")

    driver.quit()


if __name__ == "__main__":
    main()
