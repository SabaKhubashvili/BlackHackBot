from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import pytesseract

import time

def main():

    # Set Firefox options
    firefox_options = Options()

    firefox_options.headless = False  # Optional: Run Firefox in headless mode (without GUI)
    
    # Pass Firefox options
    driver = webdriver.Firefox(options=firefox_options)
    driver.set_window_size(1200, 800)  
    # Navigate to the webpage
    driver.get('https://luckylandslots.com')

    # Wait for the consent banner to appear and click it
    try:
        consent_banner = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ConsentBanner_cookiesAcceptButton__XOS3d'))
        )
        consent_banner.click()
    except Exception as e:
        print("Consent banner not found or unable to click:", e)

    # Click on the header green button
    try:
        green_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Header_greenButton__2OXY2'))
        )
        green_button.click()
    except Exception as e:
        print("Header green button not found or unable to click:", e)

    # Wait until the download progress bar disappears
# Wait until the download progress bar appears
    try:
        progress_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'DownloadProgressBar_label__2v0vC'))
        )
        print("Download progress bar found.")
    except Exception as e:
        print("Download progress bar not found:", e)

    # Wait until the progress bar disappears
# Wait until the inside content of the progress bar is not equal to "Downloading 100%"
    try:
        while True:
            try:
                progress_bar_content = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'DownloadProgressBar_label__2v0vC'))
                ).text
            except NoSuchElementException:
                # Progress bar element not found, possibly due to redirection
                # print("Progress bar element not found. Redirection may have occurred.")
                break
            
            if progress_bar_content == "Downloading 100%":
                print("Progress bar content changed.")
                break
            else:
                print("Waiting for progress bar content to change...")
                time.sleep(2)  # Check every 2 seconds
    except Exception as e:
        print("Progress bar not found")

    # Wait for 5 seconds after the progress bar disappears
    print("sleeping")
    time.sleep(10)

    # Wait until the canvas appears with class name lls-main-canvas
    try:
        # Wait for the canvas element to be present
        body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'root')))
        canvas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'lls-main-canvas')))
        print('Canvas found')    
        body.click()
        # Perform clicks across the canvas in a grid pattern
        action_chains = ActionChains(driver)
        # action_chains.move_to_element_with_offset(canvas,10,10).click().click().perform()

        random_x = random.randint(378, 524)
        print("Clicking login")
        action_chains.move_by_offset(600, 560).click().perform()

        time.sleep(2)   
        action_chains.reset_actions()
        random_x_email = random.randint(410, 700)
        random_x_password = random.randint(410, 700)
        time.sleep(1)


        action_chains.move_by_offset(random_x_email, 266).click().perform()
        time.sleep(1)
        print("Writing Email")
        for key in "epicgames01357@gmail.com":
            action_chains.send_keys(key).perform()
            time.sleep(random.uniform(0.12, 0.33))
        
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Reseting cursor, Sleeping 1 sec")
        action_chains.reset_actions()
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Moving to password")
        action_chains.move_by_offset(random_x_password, 403).click().perform()

        print("Writing Password")
        for key in "sabuka111":
            action_chains.send_keys(key).perform()
            time.sleep(random.uniform(0.14, 0.43))
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Reseting cursor, Sleeping 1 sec")
        action_chains.reset_actions()
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        action_chains.move_by_offset(597, 484).click().perform()
        print('Clicked Login button, sleeping 5 seconds')
        time.sleep(5)

        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Reseting cursor, Sleeping 1 sec")
        action_chains.reset_actions()
        print("Done, Sleeping 1 Sec")

        print("Clicking on Tables:")
        tables_random_x = random.randint(63,137)
        tables_random_y = random.randint(405,451)
        action_chains.move_by_offset(tables_random_x, tables_random_y).click().perform()
        
        
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Reseting cursor, Sleeping 1 sec")
        action_chains.reset_actions()
        print("Done, Sleeping 1 Sec")

        blackjackEnter_random_x = random.randint(239,396)
        blackjackEnter_random_y = random.randint(143,266)
        action_chains.move_by_offset(blackjackEnter_random_x, blackjackEnter_random_y).click().perform()
        
        print("Done, Waiting to load, sleeping 10 sec")
        time.sleep(10)
        action_chains.reset_actions()
        time.sleep(2)
        print("Done, Entered Game")

        action_chains.move_by_offset(605, 619).click().perform()
        print("Done, Sleeping 1 Sec")
        time.sleep(1)
        print("Reseting cursor, Sleeping 1 sec")
        action_chains.reset_actions()
        print("Done, Sleeping 1 Sec")

        isFirstValueChoose = True
        while True:
            if isFirstValueChoose:
                currentbet = 0
                while True:    
                    print("Choose Bet:")
                    print("1) 1K")
                    print("2) 5K")
                    print("3) 10K")
                    print("4) 20K")
                    print("5) 50K")
                    bet = int(input("Choose Bet:"))
                    


    except Exception as e:
        print("Canvas not found or unable to click:", e)
if __name__ == "__main__":
    main()
