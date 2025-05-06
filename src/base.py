import json
from logging import config, getLogger


class BaseClass:

    def __init__(self):
        with open("./log/log_config.json") as f:
            log_conf = json.load(f)
            config.dictConfig(log_conf)
            self.logger = getLogger("mylogger")


if __name__=="__main__":
    obj = BaseClass()
    obj.logger.info("info")
