import requests
import datetime
import random
import string


class Downloader:
    def __init__(self, data: dict, path: str):
        for item in data['urls']:
            self._get_file(
                targeturl=item,
                localaddr=path,
                extendname='mp4'
            )

    # 下载文件, targetUrl:链接, localAdd:路径, extendName:文件后缀
    def _get_file(self, targeturl: str, localaddr: str, extendname: str):
        reqs = requests.get(targeturl, stream=True)
        with open(localaddr + '/' + self._generate_time_now() + '.' + extendname, 'wb') as f:
            for chunk in reqs.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    # 用于生成随机文件名
    @staticmethod
    def _generate_time_now() -> str:
        now = datetime.datetime.now()
        format_time = now.strftime("%Y_%m_%d_%H_%M_%S")
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return format_time + '_' + random_str
