import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from src.data.EmulationInfo import EmulationInfo


class SeleniumHelper:
    def __init__(self, ud_path, emulation_info: EmulationInfo):
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

    def close_tab(self):
        self.driver.close()

    def find_element(self, css: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, css)

    def find_elements(self, css: str) -> WebElement:
        return self.driver.find_elements(By.CSS_SELECTOR, css)

    def click_element(self, ele: WebElement):
        ActionChains(self.driver).move_to_element(ele).click().perform()

    def send_keys(self, content: str):
        ActionChains(self.driver).send_keys(content).perform()

    def scroll_to_element(self, ele: WebElement):
        self.driver.execute_script(f"window.scrollTo(0, {ele.location['y']} + 200);")
        time.sleep(3)

    def go_to_url(self, url: str):
        self.driver.get(url)

    # element 의 속성 변경 ex) class, id, 등등 a<href='1' id='2> <>안에 있는 속성 수정
    def set_attributes(self, ele: WebElement, attributes_name: str, attributes_value: str):
        self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                                   ele, attributes_name, attributes_value)

    # element 의 속성 반환 ex) get_attributes(ele, "class") -> class 속성의 값 반환
    def get_attributes(self, ele: WebElement, attributes_name: str):
        return ele.get_attribute(attributes_name)

    # element 의 속성 제거 ex) remove_attributes(ele, "target") -> target 속성 제거
    def remove_attributes(self, ele: WebElement, attributes_name: str):
        self.driver.execute_script("arguments[0].removeAttribute(arguments[1]);",
                                   ele, attributes_name)

    # element 의 css 변경 ex) set_css(ele, "font-size", "14px")  지원 되는게 있고 안 되는게 있음 (jquery 필요?)
    def set_css(self, ele: WebElement, css_name: str, css_value: str):
        self.driver.execute_script("arguments[0].css(arguments[1], arguments[2]);",
                                   ele, css_name, css_value)

    # Frame 빠져 나오기
    def exit_frame(self):
        self.driver.switch_to.default_content()

    # Frame element 로 이동
    def go_to_frame(self, ele: WebElement):
        self.driver.switch_to.frame(element)

    # element 가 보이는 위치로 스크롤 이동
    def scroll_to_element_top(self, ele: WebElement):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', ele)

    # 새로운 탭 열기
    def open_new_tab(self, url: str):
        self.driver.execute_script("window.open('" + url + "');")

    # 가장 최근 윈도우 switch
    def switch_latest(self):
        self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles)-1])
        print("latest window switch - " + self.driver.current_url)

    # gps(geo_location) 설정
    def set_gps(self, latitude: int, longitude: int, accuracy: int = 100):
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        })
