from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import os
import csv


def find2_internet():

    list = ['10']

    for year in list:
        for sow in range(1, 3):
            xlex = open(f'Melon_data{year}년_{sow}월.csv', 'r', encoding='utf-8')
            f = csv.reader(xlex)
            print(f)
            print('-------------------------')
            next_page = []
            for line in f:
                next_page.append(line[4])
            xlex.close()
            print(next_page)
            driver = webdriver.Chrome()
            # 장르 리스트
            type = []
            # 댓글 수
            revu = []
            # 평점
            point = []
            for row in next_page[1:]:
                driver.get(f'https://www.melon.com/song/detail.htm?songId={row}')
                time.sleep(2)
                # 장르
                type_tag = driver.find_element_by_css_selector('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)')
                type.append(type_tag.text)

                # 댓글수
                revu_tag = driver.find_element_by_css_selector('#revCnt')
                revu.append(revu_tag.text)

                # 평점
                point_tag = driver.find_element_by_css_selector('#d_like_count')
                point.append(point_tag.text)

            dict1 = {'장르': type, '댓글수': revu , '평점': point}
            df2 = pd.DataFrame(dict1)




            if os.path.exists(f'Melon_data{year}년_{sow}월.csv') == False:
                df2.columns = ['장르', '댓글수', '평점']
                df2.to_csv(f'Melon_data{year}년_{sow}월.csv', index=False, encoding='utf-8-sig')
            else:
                df2.to_csv(f'Melon_data{year}년_{sow}월.csv', index=False, encoding='utf-8-sig', mode='a', header=False)



# 순위, 제목, 가수, 좋아요
def find_internet():
    driver = webdriver.Chrome()
    driver.get('https://www.melon.com/index.htm')

    # 멜론 차트
    chart_tag = driver.find_element_by_css_selector('#gnb_menu > ul:nth-child(1) > li.nth1 > a')
    chart_tag.click()
    time.sleep(1)

    # 차트 파인드
    chart_find_tag = driver.find_element_by_css_selector('#gnb_menu > ul:nth-child(1) > li.nth1.on > div > div > button')
    chart_find_tag.click()
    time.sleep(3)

    # 차트 검색
    ch_tag = driver.find_element_by_css_selector('#d_chart_search > div > h4.tab02 > a')
    ch_tag.click()
    time.sleep(2)

    # 연대선택
    yearda_tag = driver.find_element_by_css_selector('#d_chart_search > div > div > div.box_chic.nth1.view > div.list_value > ul > li:nth-child(2) > span > label')
    yearda_tag.click()

    time.sleep(2)

    
    # year_back = ['10','9','8','7','6','5','4','3','2','1']
    list = ['10']
    for year in list:
        year_tag = driver.find_element_by_css_selector(f'#d_chart_search > div > div > div.box_chic.nth2.view > div.list_value > ul > li:nth-child({year}) > span > label')
        year_tag.click()
        time.sleep(1)

        # range(1,13)
        for row in range(1,3):
            # 월간 선택
            month_tag = driver.find_element_by_css_selector(f'#d_chart_search > div > div > div.box_chic.nth3.view > div.list_value > ul > li:nth-child({row}) > span > label')
            month_tag.click()
            time.sleep(2)

            # 장르 선택
            gnr_tag = driver.find_element_by_css_selector('#d_chart_search > div > div > div.box_chic.last.view > div.list_value > ul > li:nth-child(1) > span > label')
            gnr_tag.click()
            time.sleep(1)

            # 검색
            button_tag = driver.find_element_by_css_selector('#d_srch_form > div.wrap_btn_serch > button')
            button_tag.click()
            time.sleep(2)

            lever_data = []
            name_data = []
            makename_data = []
            like_data = []
            address_data = []

            # 1~50위
            lever_tag1 = driver.find_elements_by_css_selector('#lst50')
            for lever in lever_tag1:
                Number = lever.find_element_by_css_selector('td:nth-child(2) > div > span')
                # 순위
                lever_data.append(Number.text)
                name = lever.find_element_by_css_selector('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > strong > a')
                # 제목
                name_data.append(name.text)
                # 가수
                makename = lever.find_element_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02')
                makename_data.append(makename.text)
                # 좋아요
                like = lever.find_element_by_css_selector('td:nth-child(5) > div > button > span.cnt')
                like_data.append(like.text)
                # 주소
                address_tag = lever.find_element_by_css_selector('td:nth-child(4) > div > a')
                address = address_tag.get_attribute('href')
                number1 = address.split('\'')[1]
                address_data.append(number1)


            # 50~100위 페이지 이동
            next_page = driver.find_element_by_css_selector('#frm > div.paginate.chart_page > span > a')
            next_page.click()
            time.sleep(3)

            # 50~100위
            lever_tag2 = driver.find_elements_by_css_selector('#lst100')
            for lever in lever_tag2 :
                Number = lever.find_element_by_css_selector('td:nth-child(2) > div > span')
                lever_data.append(Number.text)
                name = lever.find_element_by_css_selector('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > strong')
                name_data.append(name.text)
                makename = lever.find_element_by_css_selector('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02')
                makename_data.append(makename.text)
                like = lever.find_element_by_css_selector('td:nth-child(5) > div > button > span.cnt')
                like_data.append(like.text)
                address_tag = lever.find_element_by_css_selector('td:nth-child(4) > div > a')
                address = address_tag.get_attribute('href')
                number1 = address.split('\'')[1]
                address_data.append(number1)


            dict = {'순위':lever_data , '제목':name_data, '가수':makename_data, '좋아요':like_data, '주소':address_data}

            df1 = pd.DataFrame(dict)

            if os.path.exists(f'Melon_data{year}년_{row}월.csv') == False:
                df1.columns = ['순위', '제목', '가수','좋아요','주소']
                df1.to_csv(f'Melon_data{year}년_{row}월.csv', index=False, encoding='utf-8-sig')
            else:
                df1.to_csv(f'Melon_data{year}년_{row}월.csv', index=False, encoding='utf-8-sig', mode='a', header=False)



            print('종료')
            print('------------------------------')





#find_internet()


find2_internet()


