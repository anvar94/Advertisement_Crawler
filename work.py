from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging

from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlretrieve
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import time
# from util.db import mysql_img_db as mysql
import sys
from os import path
# print("config pathni koriw un ", path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from util.db_utils import mysql_img_db as mysql
from datetime import datetime
import emoji
import unicodedata

def crawler(cfg=None, db_conn=None, l_path=None):

    # print("local pathni koriw un  ", l_path)
    if cfg is None or db_conn is None:
        logging.warning("[image_info] 디비 연결 상태를 확인해 주세요.")
        return None

    today_data = datetime.now().strftime('%Y-%m-%d-%H')
    folder_path = l_path
    search_key = "건강차"          #=========================================> Search Key


    option = Options()
    # option.add_argument('--headless')
    # option.add_argument('--no-sandbox')
    # option.add_argument('lang=ko-kr')
    # option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
    option.add_argument('disable-gpu')


    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
    # driver = webdriver.Chrome(executable_path='/app-dml/FictionAFiles/google-driver/chromedriver', chrome_options=option)   # server driver path

    # driver = webdriver.Chrome()
    time.sleep(1)

    driver.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=KR&media_type=all")
    time.sleep(2)

    elem = driver.find_element_by_xpath("//*[text()=\"Ad Category\"]")
    elem.click()
    time.sleep(5)

    elem2 = driver.find_element_by_xpath("//*[text()=\"All Ads\"]")
    elem2.click()
    time.sleep(3)

    elem3 = driver.find_element_by_xpath("//*[@id=\"content\"]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div/div[1]/div/input")
    elem3.click()
    elem3.send_keys(search_key)
    time.sleep(7)
    elem3.send_keys(Keys.RETURN)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    # print("last heghtni koriw un ", last_height)

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(6)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(10)
            break
        last_height = new_height
        # print("last heightni koriw un ", last_height)


    # fb_ad = driver.find_elements_by_css_selector('._9ccv._9raa')
    fb_ad = driver.find_elements_by_xpath('//*[contains(@class, \'_99s5\')]')
    # print("fb adni koriw un ", len(fb_ad)) #1487

    # TITLE = []  # 광고 게시일자
    # ID = []  # 광고 아이디
    # CONTENT = []  # 광고 글(내용)
    # HREF = []  # 광고 랜딩페이지
    # img_src = []  # 이미지 소스
    # video_src = []  # 동영상 소스

    # name = "gretgerwtges"

    for i in range(len(fb_ad)):

        ####################################################
        #
        ####################################################

        #     print("ad infoni koriw un ", ad_info[1].text)
        try:
            ad_text = fb_ad[i].find_element_by_css_selector('.rxo4gu2c.fij28k4b')
            #         print("ad_textni koriw un ", ad_text.text)
            ad_id = ad_text.text
            ad_id_number = int(ad_id.split(' ')[1])      # ===============================> Reklama ID

            # ID.append(ad_text.text)  # 광고 글

        except:
            ad_id_number = " "
            # ID.append("")

        ####################################################
        try:
            ad_info1 = fb_ad[i].find_elements_by_css_selector(
                '.qku1pbnj.j8otv06s.cu1gti5y.a1itoznt.te7ihjl9.svz86pwt.a53abz89')
            #         print("ad infoni1ni koriw un ", ad_info1[0].text)

            brand_name = ad_info1[0].text      #==============================> Brand name
            brand_name = emoji.demojize((brand_name))
            brand_name = unicodedata.normalize('NFC', brand_name)
            # TITLE.append(ad_info1[0].text)

        except:
            brand_name = ("No Brand Name")
            # TITLE.append("")
        ####################################################

        try:
            ad_info = fb_ad[i].find_elements_by_css_selector('._4ik4._4ik5')
            # CONTENT.append(ad_info[1].text)
            full_content = ad_info[1].text          ##========================> CONTENT
            full_content = emoji.demojize(full_content)
            full_content = unicodedata.normalize('NFC', full_content)

        except:
            full_content=("")
            # CONTENT.append("")
        ####################################################

        try:
            ad_href = fb_ad[i].find_element_by_css_selector('.d5rc5kzv.chuaj5k6.qku1pbnj.j8otv06s.jrvjs1jy.a1itoznt.fvlrrmdj.svz86pwt.aa8h9o0m.jrkk970q').get_attribute('href')
            #         ad_href = fb_ad[0].find_element_by_tag_name('a').get_attribute('href')  # 랜딩페이지 주소 찾기
            # print("adhrefni koriw un ", ad_href)
            ad_url = ad_href                       # ===========================> AD URL
            # HREF.append(ad_href)

        except:
            ad_href = fb_ad[i].find_element_by_css_selector(
                '.d5rc5kzv.iz6v9oso.qku1pbnj.j8otv06s.jrvjs1jy.a1itoznt.fvlrrmdj.svz86pwt.aa8h9o0m').get_attribute('href')
            # print("adhref videoni koriw un", ad_href)
            ad_url = ad_href              # =====================================> AD URL
            # HREF.append(ad_href)
        ####################################################

        image_name = (str(ad_id_number)+"/"+today_data)

        # print("ALL information", search_key, ad_id_number, brand_name, full_content, ad_url, image_name)
        # print(type(ad_id_number))
        # print(ad_id_number)

        query_ad_id = {"DATA_ID": ad_id_number}

        check_ad_id = mysql.get_data_one(db_conn=db_conn,
                                    query_xml=cfg.sql_xml_path('MK_FB_AD_GATH_DATA'),
                                    query_id='check_insert_id',
                                    query_params=query_ad_id)

        # print("check image resultni koriw ", check_ad_id)


        query_datas = {"DATA_CATE": search_key, "DATA_ID": ad_id_number, "BRAND_NAME": brand_name, "AD_CNTS": full_content, "AD_CNTS_URL": ad_url, "AD_IMG_NAME": image_name}

        if check_ad_id is None:
            mysql.db_commit(db_conn=db_conn,
                            query_xml=cfg.sql_xml_path('MK_FB_AD_GATH_DATA'),
                            query_id='insert_datas',
                            query_params=query_datas)
        else:
            pass

        try:
            ad_img = fb_ad[i].find_element_by_css_selector('._7jys.img').get_attribute('src')  # 이미지 소스 찾기
            # print("ad_imgni nameni koriw un ", ad_img)
            # print("imageni otini koriw un ", folder_path + '{}.jpg'.format(ad_id_number))
            # img_src.append(ad_img)
            urlretrieve(ad_img, folder_path + '{}.jpg'.format(ad_id_number))

        except:
            pass

        try:
            ad_img = fb_ad[i].find_element_by_tag_name('video').get_attribute('src')  # 동영상 소스 찾기
            #         print("ad image videoni koriw uchun", ad_img)
            urlretrieve(ad_img, folder_path + '{}.mp4'.format(ad_id_number))
            # video_src.append(ad_img)
        except:
            pass





        # print("all image listni koriw un ", img_src)
    ####################################################
        #
        # try:
        #     urlretrieve(ad_img, folder_path + '{}_{}.jpg'.format(ad_id_number))
        #     # print("imageni download qiliw un ", image)
        # except:
        #     pass
        # try:
        #     urlretrieve(ad_img, folder_path + '{}_{}.mp4'.format(ad_id_number))
        # except:
        #     pass


    # print("image crcni koriw un ", img_src)
    # for index, link in enumerate(img_src):
    #     #     print("indexni koriw un ", index)
    #     # print("linkni koriw un ", link)
    #     # print("indexni koriw un ", index)
    #     try:
    #         urlretrieve(link, folder_path + '{}_{}.jpg'.format(ad_id_number, index + 1))
    #         # print("imageni download qiliw un ", image)
    #     except:
    #         pass
    #
    # for index, link in enumerate(video_src):
    #     try:
    #         urlretrieve(link, folder_path + '{}_{}.mp4'.format(ad_id_number, index + 1))
    #     except:
    #         pass
    #
    # driver.quit()



    # try:
    #     data = {'ID': ID, 'TITLE': TITLE, 'CONTENT': CONTENT, 'HREF': HREF}
    # except:
    #     pass
    #
    # data = pd.DataFrame(data)
    #
    # try:
    #     data.to_csv(folder_path + '{}.csv'.format(name), index=False, encoding="utf-8-sig")
    # except:
    #     pass

    # print("hrefni nmaligini koriw un ", HREF)


    # https://scontent-gmp1-1.xx.fbcdn.net/v/t39.35426-6/s600x600/241352716_4592702427447971_6796914305750585409_n.jpg?_nc_cat=109&ccb=1-5&_nc_sid=cf96c8&_nc_ohc=8C3Nhqmtn7kAX9_kmPM&_nc_ht=scontent-gmp1-1.xx&oh=55078220a62f6f947f0d157143bb19ad&oe=616E6335

# crawler()