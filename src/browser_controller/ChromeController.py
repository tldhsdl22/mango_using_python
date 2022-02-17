from src.browser_controller.selenium_helper.SelniumHelper import SeleniumHelper
from src.data.UserAgentInfo import UserAgentInfo


class ChromeController:
    def __init__(self):
        super().__init__()

    def open_browser(self, ud_path:str, ua_info:UserAgentInfo) -> bool:
        try:
            # 셀레니움 객체 생성
            self.selenium = SeleniumHelper(ud_path, ua_info)
            if self.selenium is not None:
                self.selenium.open_browser()
                return True

        except Exception as e:
            # 예외처리
            print(f'open_browser exception: {e}')

        return False

    def login_naver(self) -> bool:
        self.selenium.go_to_url("https://m.naver.com/")
        print("로그인")
        return True

    def enter_store(self):
        print("Chrome 1")

    def move_in_store(self):
        print("Chrome 2")
        
    def enter_place(self):
        print("Chrome 2")
        
    def move_in_place(self):
        print("Chrome 2")

    def go_to_naver(self):
        self.selenium.go_to_url("https://m.naver.com")
