class EmulationInfo:
    def __init__(self, width, height, pixel_ratio, user_agent, platform):
        self.width = width
        self.height = height
        self.pixel_ratio = pixel_ratio
        self.user_agent = user_agent
        self.platform = platform

    @staticmethod
    def get_test_data():
        emulation = EmulationInfo(width=384, height=854, pixel_ratio=2.8125, platform="Linux aarch64",
                                  user_agent="Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G998N/KSU3BVA2) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/90.0.4430.210 Mobile Safari/537.36")
        return emulation
