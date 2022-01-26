import logging
import logging as mylogger

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# print("pathni koriw un ", path.dirname(path.dirname(path.abspath(__file__))))
from util.config_utils import config_util
# from util.utils import string_util
# from utils import data_crawler
from modules import work as data_crawler
import multiprocessing as mp
import time
import os
from apscheduler.schedulers.background import BlockingScheduler


class CLS:
    def __init__(self):
        self.cfg = config_util.CLS()
        self.cfg_config = self.cfg.setinit("../../properties/config/config.json")

        # cfg_logging = self.cfg.setMplogging('../../properties/config/img_logging.json', file_type='check', pid=os.getpid())  # 로깅 설정
        logging.info('###############################################################################')
        logging.info('> start ---- main !!!!!!!!!!!!!!!')

        logging.info('#'*15)
        logging.info('facebook data crawler')
        self.isRunning = False
        self.l_path, self.s_path = self.cfg.scp_path()



    def main(self):
        data_crawler.crawler(cfg=self.cfg,
                             db_conn=self.cfg.db_conn,
                             l_path=self.l_path)


if __name__ == '__main__':

    cls = CLS()
    # cls.main()
    while True:
        cls.main()
        time.sleep(30)

# import multiprocessing as mp
# from fb_gath_data import main
# from img.auto_bg_crop.util.config_utils import com_util
#
# def facebook_crawler():
#     cls = main.CLS()
#     cls.main()
#
# if __name__ == '__main__':
#
#     cls = CLS()
#     # cls.main()
#     while True:
#         cls.main()
#         time.sleep(30)
