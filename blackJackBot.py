import pytesseract
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
from PIL import ImageGrab
import re
import time
import cv2
strategy_chart = {
    '2/2': {'2': 'H', '3': 'SP', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'SP', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '3/3': {'2': 'H', '3': 'H', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'SP', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '4/4': {'2': 'H', '3': 'H', '4': 'H', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '5/5': {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'H', 'A': 'H'},
    '6/6': {'2': 'SP', '3': 'SP', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '7/7': {'2': 'SP', '3': 'SP', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'SP', '8': 'H', '9': 'H', '10': 'S', 'A': 'H'},
    '9/9': {'2': 'SP', '3': 'SP', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'S', '8': 'SP', '9': 'SP', '10': 'S', 'A': 'S'},
    '10/10': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},
    
    "A/A 8/8": {'2': 'SP', '3': 'SP', '4': 'SP', '5': 'SP', '6': 'SP', '7': 'SP', '8': 'SP', '9': 'SP', '10': 'SP', 'A': 'SP'},

    "A/2": {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "A/3": {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "A/4": {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "A/5": {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "A/6": {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "A/7": {'2': 'S', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'S', '8': 'S', '9': 'H', '10': 'H', 'A': 'S'},
    "A/8": {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'D', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},
    "A/9": {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},

    "4": {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "5": {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "6": {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    "7": {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},

    '8':  {'2': 'H', '3': 'H', '4': 'H', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '9':  {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '10': {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'H', 'A': 'H'},
    '11': {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'D', 'A': 'D'},
    '12': {'2': 'H', '3': 'H', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '13': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '14': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '15': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '16': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '17+': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},
}



def extract_integer(text):
    # Regular expression to match an integer
    pattern = r'\d+'
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    # If there are matches, return the first one as an integer
    if matches:
        return str(matches[0])
    else:
        return None
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
        consent_banner = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ConsentBanner_cookiesAcceptButton__XOS3d')))
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
        canvas_size = canvas.size
        canvas_width = canvas_size['width']
        canvas_height = canvas_size['height']


        print('Canvas found')    
        body.click()
        # Perform clicks across the canvas in a grid pattern
        action_chains = ActionChains(driver)
        # action_chains.move_to_element_with_offset(canvas,10,10).click().click().perform()

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
        for key in "khubashvili.saba12@gmail.com":
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
        tables_random_y = random.randint(425,451)
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

        currentbet = 0
        while True:
            action_chains.reset_actions()
            print("1) Choose Bet")
            print("2) Start Game")
            print("3) Clear Bet")
            bet = input("\n Welcome What you want to do:")
            if bet == "1":
                while True:    
                    print("\n Choose Bet:")
                    print("1) 1K")
                    print("2) 5K")
                    print("3) 10K")
                    print("4) 20K")
                    print("5) 50K")
                    print("6) Type play or exit to start playing")
                    bet = input("\nChoose Bet:")
                    if bet == "1":
                        currentbet += 1000
                        print("\nSetting bet:")
                        action_chains.move_by_offset(random.randint(420,468), random.randint(393,434)).click().perform()
                        time.sleep(1)
                        action_chains.reset_actions()
                        print("\nBet Set! Current Bet: ", currentbet)
                    elif bet == "2":
                        currentbet += 5000
                        print("Setting bet:")
                        action_chains.move_by_offset(random.randint(494,550), random.randint(393,434)).click().perform()
                        time.sleep(1)
                        action_chains.reset_actions()
                        print("\nBet Set! Current Bet: ", currentbet)
                    elif bet == "3":
                        currentbet += 10000
                        print("\nSetting bet:")
                        action_chains.move_by_offset(random.randint(569,624), random.randint(393,434)).click().perform()
                        time.sleep(1)
                        action_chains.reset_actions()
                        print("\nBet Set! Current Bet: ", currentbet)
                    elif bet == "4":
                        currentbet += 20000
                        print("\nSetting bet:")
                        action_chains.move_by_offset(random.randint(650,700), random.randint(393,434)).click().perform()
                        time.sleep(1)
                        action_chains.reset_actions()
                        print("\nBet Set! Current Bet: ", currentbet)
                    elif bet == "5":
                        currentbet += 50000
                        print("Setting bet:")
                        action_chains.move_by_offset(random.randint(724,783), random.randint(393,434)).click().perform()
                        time.sleep(1)
                        action_chains.reset_actions()
                        print("Bet Set! Current Bet: ", currentbet)
                    elif bet == '6' or bet.lower() == 'play' or bet.lower() == 'exit':
                         print("Breaking and starting game with: ", currentbet, " bet \n")
                         break
                    else:
                        print("\nCommand Not Supported!")
            elif bet == "2":
                    print("Starting Game")
                    time.sleep(1)
                    while True:
                        print("Game Started!")
                        cards = 0

                        # Take a screenshot of the browser viewport
                        while True:
                            print("cards: ", cards)
                            try:
                                screenshot_filename = "browser_screenshot.png"
                                driver.save_screenshot(screenshot_filename)
                            except Exception as e:
                                print("Failed to capture screenshot:", e)

                            try:
                                crop_width = canvas_width // 7
                                crop_height = canvas_height // 5

                                # Calculate the coordinates for cropping
                                left = canvas_width - crop_width  # Left coordinate starts from 1/8 from the right
                                top = canvas_height - crop_height  # Top coordinate starts from 1/4 from the bottom
                                right = canvas_width  # Right coordinate is the full width
                                bottom = canvas_height
                                cropping_box = (left, top, right, bottom)

                                deal_screenshot = Image.open(screenshot_filename)
                                cropped_deal_screenshot = deal_screenshot.crop(cropping_box)
                                cropped_deal_screenshot.save("cropped_deal_screenshot.png")

                                extracted_deal_text = pytesseract.image_to_string(cropped_deal_screenshot, lang='eng', config='--psm 10 --oem 3')
                            except Exception as e:
                                 print("Failed to crop deal screenshot:", e)

                            print("right text button: ", extracted_deal_text.strip())


                            if extracted_deal_text.strip() == "THE)":
                                cards = 0
                                action_chains.move_by_offset(random.randint(1035,1112), random.randint(570,648)).click().perform()
                                action_chains.reset_actions()
                            elif  extracted_deal_text.strip() == 'TAL)' or extracted_deal_text.strip() == 'oD)' or extracted_deal_text.strip() == """EPEAT PLAY )""":
                                cards = 0
                                print("Clicking On Deal!")
                                cards += 2
                                # ! Click on the Deal Button
                                action_chains.move_by_offset(random.randint(1035,1112), random.randint(570,648)).click().perform()
                                time.sleep(4)
                                action_chains.reset_actions()
                                time.sleep(5)
                                print("Cards Received!")
                            elif extracted_deal_text.strip() == "cir)": 
                                print("\nPlaying current game!")
                                if cards == 0:
                                    cards += 2
                                else:
                                    cards += 1
                                try:
                                    screenshot = Image.open("browser_screenshot.png")
                                    crop_coordinates = (525, 345, 600, 380)  # Example coordinates for cropping a region
                                    cropped_screenshot = screenshot.crop(crop_coordinates)
                                    cropped_screenshot.save("Cropped_Point_screenShot.png")
                                    extracted_points_text = pytesseract.image_to_string(cropped_screenshot, lang='eng', config='--psm 10 --oem 3')
                                    print("Extracted String:", extracted_points_text)
                                except Exception as e:
                                    print("Failed to extract text from screenshot:", e)
                                time.sleep(5)
                                print("extractedText: " ,extracted_points_text)
                                extracted_point_formatted = extract_integer(extracted_points_text)
                                print('Point: ', extracted_point_formatted)
                                if not  extracted_point_formatted:
                                    action_chains.move_by_offset(random.randint(35,141), random.randint(570,648)).click().perform()
                                    action_chains.reset_actions()
                                    print("Stand!")
                                    time.sleep(10)
                                elif '/' not in extracted_point_formatted and int(extracted_point_formatted) >= 17 and extracted_point_formatted:
                                    first_value = strategy_chart['17+'][str(cards)]
                                    if first_value == 'H':
                                        action_chains.move_by_offset(random.randint(1035,1112), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Hit!")
                                        time.sleep(10)
                                    elif first_value == "D":
                                        action_chains.move_by_offset(random.randint(879,971), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Double Down!")
                                        time.sleep(10)
                                    elif first_value == "S":
                                        action_chains.move_by_offset(random.randint(35,141), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Stand!")
                                        time.sleep(10)
                                    elif first_value == "SP":
                                        action_chains.move_by_offset(random.randint(221,303), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Split!")
                                        time.sleep(10)
                                    action_chains.reset_actions();
                                else:
                                    first_value = strategy_chart[extracted_point_formatted][str(cards)]
                                    if first_value == 'H':
                                        action_chains.move_by_offset(random.randint(1035,1112), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Hit!")
                                        time.sleep(10)
                                    elif first_value == "D":
                                        action_chains.move_by_offset(random.randint(879,971), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Double Down!")
                                        time.sleep(10)
                                    elif first_value == "S":
                                        action_chains.move_by_offset(random.randint(35,141), random.randint(570,648)).click().perform()
                                        action_chains.reset_actions()
                                        print("Stand!")
                                        time.sleep(10)
                                    elif first_value == "SP":
                                        action_chains.move_by_offset(random.randint(221,303), random.randint(570,648)).click().perform()
                                        print("Split!")
                                        action_chains.reset_actions()
                                        time.sleep(10)
                                time.sleep(5)
            elif bet == "3":
                    print("Clearing Bet:")
                    currentbet = 0
                    action_chains.move_by_offset(81, 620).click().perform()
                    time.sleep(1)
                    action_chains.reset_actions()
                    print("Bet Cleared! \n")
    except Exception as e:
        print(e)
if __name__ == "__main__":

    main()
