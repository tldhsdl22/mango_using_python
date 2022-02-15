import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from src.data.EmulationInfo import EmulationInfo

class SeleniumHelper:
    def __init__(self, ud_path, emulation_info:EmulationInfo):
        self.ud_path = ud_path
        self.emulation_info = emulation_info


    def open_browser(self):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--lang=ko-KR')  # 언어 설정
        chrome_options.add_argument('--disk-cache-size=0')  # 캐시 최대 용량 설정 ( 0MB )
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 문구 제거 1
        chrome_options.add_experimental_option("useAutomationExtension", False)  # 자동화 문구 제거 2
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 문구 제거 3
        chrome_options.add_argument('--user-agent=' + self.emulation_info.user_agent)  # User-Agent 설정
        chrome_options.add_argument("--user-data-dir=" + self.ud_path)  # 유저 데이터 경로 설정

        self.driver = webdriver.Chrome(executable_path='selenium_helper/chromedriver.exe', options=chrome_options)
        self.set_device_detail()

    # Device 세부 설정
    def set_device_detail(self):
        # Device 설정 값
        prefs = {
            'width': self.emulation_info.width,
            'height': self.emulation_info.height,
            'screenWidth': self.emulation_info.width,
            'screenHeight': self.emulation_info.height,
            'deviceScaleFactor': self.emulation_info.pixel_ratio,
            'platform': self.emulation_info.platform,
            'mobile': True,
        }

        self.driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
            'enabled': True,
            'maxTouchPoints': 5
        })

        # Device 정보 설정
        self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", prefs)

        # Platform 설정
        self.driver.execute_cdp_cmd("Emulation.setNavigatorOverrides", {'platform': prefs['platform']})


    def close_browser(self):
        self.driver.quit()

    def find_element(self, css:str) -> WebElement:
        return self.driver.find_element_by_css_selector(css)

    def click_element(self, ele:WebElement):
        ActionChains(self.driver).move_to_element(ele).click().perform()

    def send_keys(self, content:str):
        ActionChains(self.driver).send_keys(content).perform()

    def scroll_to_element(self, ele:WebElement):
        self.driver.execute_script(f"window.scrollTo(0, {ele.location['y']} + 200);")
        time.sleep(3)

    def go_to_url(self, url:str):
        self.driver.get(url)
