import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class SeleniumHelper:
    def __init__(self, ud_path):
        self.ud_path = ud_path

    def openBrowser(self):
        options = Options()
        options.add_argument(f'--user-data-dir={self.ud_path}')
        self.driver = webdriver.Chrome('chromedriver.exe', options=options)

    def closeBrowser(self):
        self.driver.quit()

    def findElementByCss(self, css:str) -> WebElement:
        return self.driver.find_element_by_css_selector(css)

    def clickElement(self, ele:WebElement):
        ActionChains(self.driver).move_to_element(ele).click().perform()

    def sendKeysToElement(self, ele:WebElement, content:str):
        ActionChains(self.driver).send_keys(content).perform()



ud_path = "G:/userdata/3"
selenium = SeleniumHelper(ud_path)
selenium.openBrowser()

ele = selenium.findElementByCss("")

ele.click()

