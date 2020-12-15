from selenium import webdriver
import time

WEB_PAGE = "http://orteil.dashnet.org/experiments/cookie/"
DRIVER_PATH = "/home/nyxfox/Downloads/cdriver/chromedriver"

driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(WEB_PAGE)

game_over = time.time() + 60 * 5
five_sec = time.time() + 5

cookie = driver.find_element_by_id("cookie")

items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

game_on = True
while game_on:
    cookie.click()
    if time.time() > five_sec:
        prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []
        for price in prices:
            element_text = price.text
            if element_text != "":
                cookie_cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cookie_cost)

        baking_upgrades = {}
        for n in range(len(item_prices)):
            baking_upgrades[item_prices[n]] = item_ids[n]

        money = driver.find_element_by_id("money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_total = int(money)

        my_upgrades = {}
        for cookie_cost, elm_id in baking_upgrades.items():
            if cookie_total > cookie_cost:
                my_upgrades[cookie_cost] = elm_id
        best_upgrade = max(my_upgrades)
        purchase = my_upgrades[best_upgrade]

        driver.find_element_by_id(purchase).click()
        five_sec = time.time() + 5

        if game_over < time.time():
            game_on = False
