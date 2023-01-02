import json


class JSONOperator:
    def __init__(self, path: str):
        self.path = path

    # 清空json文件
    def clear(self):
        with open(self.path, 'w') as f:
            f.write('')
        pass

    # 保存json文件
    def save(self, data: dict):
        with open(self.path, 'w') as f:
            json.dump(data, f)
        pass

    # 读取json文件
    def read(self) -> dict:
        with open(self.path, 'r') as f:
            return json.load(f)
        pass

