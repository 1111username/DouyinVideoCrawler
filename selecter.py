from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import time

def select_elem(arggs: tuple, driver):
    return WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located(
            (arggs[0], arggs[1])
        )
    )

def select_elems(arggs: tuple, driver):
    return WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_all_elements_located(
            (arggs[0], arggs[1])
        )
    )

def selectVideoUrl(pageUrl: str, number: int, loginCostTime: int, phoneNumber: str) -> list:
    # pageUrl:要爬取页面的url, number:爬取的数量(只会少), loginCostTime:等待登录的时间, phoneNumber:登录用的手机号 
    browser = webdriver.Chrome()
    browser.get(pageUrl)

    login_bt = select_elem((By.ID, 'qdblhsHs'), browser)
    login_bt.click()
    login_bt = select_elems((By.CLASS_NAME, 'web-login-tab-list__item'),
        browser)
    login_bt[1].click()
    login_area = select_elem((By.CLASS_NAME,'web-login-normal-input__input'),browser)
    login_area.send_keys(phoneNumber)
    login_area = select_elem((By.CLASS_NAME, 'send-input'),browser)
    login_area.click()
    time.sleep(loginCostTime)
    labels = None
    n = 0
    videoLink = []
    while n < number: # 计数，统计当前页面共有100个视频为止
        browser.execute_script( # 如果不够，就向下滚动页面加载更多视频
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        labels = browser.find_elements(By.CLASS_NAME, 'mZ4vbHBN') # 选择视频所在的元素
        n = len(labels)
    for index,item in enumerate(labels):
        ActionChains(browser).move_to_element(item).perform() # 聚焦到该视频处，以加载视频链接
        try:
            item.find_element(By.CLASS_NAME, 'AwIKR2fG') # 判断是否含有视频元素
        except:
            labels.pop(index)
            continue
        elemsOfTagVideo = WebDriverWait(item, 30, 0.1).until( # 对懒加载视频进行加载
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'xg-video-container')
            )
        )
        elemsOfTagSource = elemsOfTagVideo.find_elements(By.TAG_NAME, 'source') # 定位到含有视频链接的元素上
        try:
            videoLink.append(elemsOfTagSource[2].get_attribute('src')) # 获取视频链接
        except:
            continue

    for item in videoLink:
        print(item)

    browser.quit()
    return videoLink