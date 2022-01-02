from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
from collections import Counter
import requests
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


title_keyword=[]
okt= Okt()

def google_news(keyword):
    '''=======================구글======================='''
    url="https://news.google.com/topstories?hl=ko&gl=KR&ceid=KR:ko"
    browser.get(url)
    elem = browser.find_element_by_xpath("//*[@id='gb']/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]")
    elem.clear()
    elem.send_keys(keyword) #키워드를 구글 뉴스에 입력 
    elem.send_keys(Keys.ENTER) 
    '''웹 스크래핑 중'''
    url = browser.current_url
    res = requests.get(url)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'lxml')
    titles = soup.find_all("h3", attrs={"class":"ipQwMb ekueJc RD0gLb"})
    for title in titles:
        news_title = title.find("a").get_text()
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        title_keyword.append(news_title)
    
    print("\n구글 뉴스 웹 스크래핑을 완료하였습니다.")



def daum_news(keyword):
    '''=======================다음======================='''
    for i in range(1,21,1):
        url=(f"https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&q={keyword}&p={i}")
        browser.get(url)
        '''웹 스크래핑 중'''
        url = browser.current_url
        res = requests.get(url)
        res.raise_for_status()
        soup=BeautifulSoup(res.text, 'lxml')
        titles = soup.find_all("div", attrs={"class":"wrap_cont"})
        for title in titles:
            news_title = title.find("a").get_text()
            title_keyword.append(news_title)
            
    print("\n다음 뉴스 웹 스크래핑을 완료하였습니다.")

    
def naver_news(keyword):
    '''======================네이버======================='''
    for i in range(1,211,10):
        url=(f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i})")
        browser.get(url)
        '''웹 스크래핑 중'''
        url = browser.current_url
        res = requests.get(url)
        res.raise_for_status()
        soup=BeautifulSoup(res.text, 'lxml')
        titles= soup.find_all("a",attrs={"class":"news_tit"})
        for title in titles:
            news_title = title.get_text()
            title_keyword.append(news_title)
    
    print("\n네이버 뉴스 웹 스크래핑을 완료하였습니다.")

        

def delete_same(title_keyword):
    #중복제거
    global cnt #전역변수
    cnt = 0
    new_title_keyword=[]
    for i in title_keyword:
        if i not in new_title_keyword:
            new_title_keyword.append(i)
            cnt+=1
    
    return new_title_keyword

def find_noun(new_title_keyword):
    #리스트 합치고 단어 찾기(전치사 제거)
    Str_new_title_keyword=" ".join(new_title_keyword) #string형태
    main_keyword=okt.nouns(Str_new_title_keyword) #리스트 형태

    return main_keyword 

def user_keyword(keyword):
    #유저 검색 키워드 단어 나누기
    noun_user_keyword=okt.nouns(keyword) #리스트 형태

    return noun_user_keyword 

def delete_small(main_keyword):
    #2자리 이상 단어
    for i,v in enumerate(main_keyword):
        if len(v) < 2:
            main_keyword.pop(i)

    return main_keyword

def delete_user_keyword(noun_user_keyword,main_keyword):
    #유저 검색 키워드와 뉴스 키워드 비교 및 제거
    for i in range(0,len(noun_user_keyword),1):
        for j,v in enumerate(main_keyword):
            if noun_user_keyword[i] == v:
                main_keyword.pop(j)
    Str_main_keyword=" ".join(main_keyword)
    
    return Str_main_keyword

def wordcloud_keyword(Str_main_keyword):
    #워드클라우드 생성
    wordcloud=WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(Str_main_keyword)
    plt.figure(figsize=(10,10)) 
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis('off')
    plt.show()

def count_keyword(main_keyword):
    #글자 수 세기
    count = Counter(main_keyword)
    cnt_keyword = count.most_common(100)
    for i in range(0,len(cnt_keyword),1):
        print(cnt_keyword[i])



    

    
    






print("=======================주식 키워드 통계 프로그램=======================\n")


print("\n자신의 user-agent를 얻는 법")

user_know=input("\n알고 있다면 아무키나 모른다면 1을 입력하세요: ")
if (user_know=='1'):
    print("\n1. 구글에 user-agent검색")
    print("2. user-agent를 제공하는 사이트 접속")
    print("3. 자신의 user-agent 확인 및 복사")
    print("일반적인 user-agent  ex) 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/~~~~~'.")
    user_know=input("\n완료되었다면 아무키나 입력하세요")
    os.system('cls')

os.system('cls')

print("=======================주식 키워드 통계 프로그램 시작=======================")

print("\n이 프로그램은 구글(Google), 네이버(Naver), 다음(Daum)의 뉴스 데이터를 바탕으로 통계를 냅니다.")
user_agent= input("\n자신의 user-agent를 입력하시오: ")
while(1):
    keyword = input("\n자신이 검색하고 싶은 키워드를 입력하시오: ")
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument(user_agent)
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()


    google_news(keyword)
    naver_news(keyword)
    daum_news(keyword)

    new_title_keyword=delete_same(title_keyword)

    main_keyword=find_noun(new_title_keyword)

    noun_user_keyword=user_keyword(keyword)

    main_keyword=delete_small(main_keyword)

    Str_main_keyword=delete_user_keyword(noun_user_keyword, main_keyword)

    print(f"\n총 {cnt}개의 뉴스가 검색되었습니다.(중복 제거 완료)")

    print("\n1. 워드 클라우드 형태로 보기\n")
    print("2. (단어, 개수)형태로 보기(최대 빈도수 순 100개)\n")
    print("3. 모두 보기\n")
    while(1):
        value=input("다음 중 원하는 형태를 입력하시오(1,2,3 중 선택): ")
        if value == '1':
            wordcloud_keyword(Str_main_keyword)
            break
        elif value == '2':
            count_keyword(main_keyword)
            break
        elif value == '3':
            count_keyword(main_keyword)
            wordcloud_keyword(Str_main_keyword)
            break
        
        else:
            print("잘 못 입력하였습니다.\n")
    cnt = 0
    title_keyword=[]

    
    user_choice=input("다른 단어를 검색하고 싶다면 1을 제외한 아무키나 누르시오: ")
    if user_choice=='1':
        print("프로그램을 종료합니다.")
        break
    os.system('cls')










