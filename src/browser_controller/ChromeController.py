from src.browser_controller.SelniumHelper import SeleniumHelper
from src.data.EmulationInfo import EmulationInfo
class ChromeController():
    def open_browser(self, ud_path:str, emulation_info:EmulationInfo) -> bool:
        try:
            # 셀레니움 객체 생성
            self.selenium = SeleniumHelper(ud_path, emulation_info)
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
        

if __name__ == '__main__':
    for _ in range(0, 1):
        # 유저데이터 가져오기
        ud_path = "G:/userdata/3"
        
        # 에뮬레이션 정보 가져오기
        emulation_info = EmulationInfo.get_test_data()

        # 크롬 열기
        controller = ChromeController()
        if not controller.open_browser(ud_path, emulation_info):
            print("크롬 열기 실패")
            continue

        if not controller.login_naver():
            print("로그인 실패")
            continue
