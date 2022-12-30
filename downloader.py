import requests
import datetime
import random
import string


def get_file(targetUrl: str, localAdd: str, extendName: str):
    # 下载文件, targetUrl:链接, localAdd:路径, extendName:文件后缀
    reqs = requests.get(targetUrl,stream=True)
    with open(localAdd+'/'+generate_time_now()+'.'+extendName, 'wb') as f:
        for chunk in reqs.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def generate_time_now() -> str:
    now = datetime.datetime.now()
    format_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return format_time+'_'+random_str

if __name__ == "__main__":
    get_file("https://www.douyin.com/aweme/v1/play/?video_id=v0d00fg10000c6750bjc77ucfcj50eeg&line=0&file_id=bf4a5843e86c414f887235f70563746a&sign=b1503b3226e905094719e44aed5a7222&is_play_url=1&source=PackSourceEnum_SEARCH&aid=6383",
    './',
    'mp4')