from downloader import Downloader
from selector import Selector
from jsonoperator import JSONOperator
import urllib.parse

if __name__ == '__main__':
    # 读取输入参数
    inputData = JSONOperator('./input.json').read()

    # 执行选择器，获取所有视频的url，并输出在output.json中
    Selector(
        pageurl=urllib.parse.quote(inputData['search']),
        number=inputData['videoNumber'],
        logincosttime=inputData['loginCostTime'],
        phonenumber=inputData['phoneNumber']
    )
    # 获取输出的url
    outputData = JSONOperator('./output.json').read()

    # 对输出的视频url进行下载
    Downloader(
        data=outputData,
        path=inputData['savePath']
    )
