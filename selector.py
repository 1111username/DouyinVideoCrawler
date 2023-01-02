from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import time
from jsonoperator import JSONOperator


class Selector:
    '''
    选择器类，用于获取页面中视频的url
    接受参数：pageurl页面url，
            number获取的url数量(不要大于150)，
            logincosttime登录所等待的最大时间(秒),
            phonenumber手机号
    输出：将获取的url都保存在output.json里
    '''
    def __init__(self, pageurl: str, number: int, logincosttime: int, phonenumber: str):
        # 使用谷歌浏览器驱动
        self.browser = webdriver.Chrome()
        self.jsonOperator = JSONOperator('./output.json')

        # 这里应该检查输出文件outputjson.json是否为空
        self.jsonOperator.clear()

        # 开始打开浏览器到指定页面
        self.browser.get(pageurl)

        # 这里开始进行运行选择逻辑
        # 先进行登录
        self._login(phonenumber, logincosttime)
        # 对页面进行滑动，知道当前页面有足够多的视频数
        self._swipe(number)
        # 开始收集视频链接
        result = self._load_collect(number)
        # 在这里对result进行输出
        self.jsonOperator.save({'urls': result})

        # 关闭浏览器
        self.browser.quit()
        pass

    @staticmethod
    def select_elem(arggs: tuple, driver):
        return WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (arggs[0], arggs[1])
            )
        )

    @staticmethod
    def select_elems(arggs: tuple, driver):
        return WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_all_elements_located(
                (arggs[0], arggs[1])
            )
        )

    def _login(self, phonenumber: str, logincosttime: int) -> None:
        # 先点击“登录”按钮
        self.select_elem((By.ID, 'qdblhsHs'), self.browser).click()

        # 点击弹出框的"验证码登录"按钮
        # 首选获取无序列表的元素集合
        ulList = self.select_elems((By.CLASS_NAME, 'web-login-tab-list__item'), self.browser)
        # 点击第二个，也就是验证码登录
        ulList[1].click()

        # 获取手机号输入框元素
        inputPhoneNumberArea = self.select_elem((By.CLASS_NAME, 'web-login-normal-input__input'), self.browser)
        # 输入手机号
        inputPhoneNumberArea.send_keys(phonenumber)
        # 点击获取验证码
        self.select_elem((By.CLASS_NAME, 'send-input'), self.browser).click()
        # 等待填写验证码并提交
        time.sleep(logincosttime)

        pass

    def _swipe(self, number: int) -> None:
        videoNumberInPage = 0  # 用于保存当前页面的视频总数
        while videoNumberInPage < number:
            # 首先下划加载新视频
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 划到页面最底部
            # 首先获取当前页面的包含视频的li标签元素
            liContentVideo = self.browser.find_elements(By.CLASS_NAME, 'AwIKR2fG')
            videoNumberInPage = len(liContentVideo)
        pass

    def _load_collect(self, number: int) -> list:
        urlList = []  # 存储视频链接
        # 首先获取所有带视频的li标签元素
        liContentVideo = self.browser.find_elements(By.CLASS_NAME, 'hdm9e05T')
        # 对元素进行遍历
        for index, item in enumerate(liContentVideo):
            # 先进行聚焦，以加载视频
            ActionChains(self.browser).move_to_element(item).perform()
            # 等待出现视频元素，获取该标签元素
            elemsOfTagVideo = WebDriverWait(item, 30, 0.1).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, 'xg-video-container')
                )
            )
            # 定位到含有视频视频链接的元素
            elemsOfTagSource = elemsOfTagVideo.find_elements(By.TAG_NAME, 'source')
            # 获取视频链接到数组里
            urlList.append(elemsOfTagSource[2].get_attribute('src'))
            # 当满足视频数量时，停止
            if index == number - 1:
                break
        return urlList
