from downloader import get_file
from selector import selectVideoUrl

if __name__ == '__main__':
    urlList = selectVideoUrl('https://www.douyin.com/search/%E6%B2%B3%E5%8D%97%E8%AF%9D', # 抖音视频检索结果页连接
        10, # 爬取的视频数量(只会少，不会等于)
        30, # 登录所需要的时间(短信验证码登录)
        '17358766821') # 手机号
    
    for item in urlList:
        get_file(item,'./tars','mp4') # 保存的路径
