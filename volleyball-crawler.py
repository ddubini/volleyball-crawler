from selenium import webdriver
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import pandas as pd

# 이중 리스트 -> 단순 리스트
def flatten(data):
    output = []
    for item in data:
        if type(item) == list:
            output += flatten(item)
        else:
            output += [item]
    return output

def process():
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    # driver 실행
    driver = webdriver.Chrome('/Users/hansubin/Downloads/chromedriver', options=options)

    driver.implicitly_wait(3)
    # 홈팀
    # https://www.kovo.co.kr/game/v-league/11141_game-summary.asp?season=017&g_part=201&r_round=4&g_num=113&
    # 원정팀
    # https://www.kovo.co.kr/game/v-league/11141_game-summary.asp?season=017&g_part=201&r_round=2&g_num=72&
    driver.get(e1.get())
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    no = soup.select("div.wrp_lst > table.lst_board.lst_fixed.w123 > tbody > tr > td.no")
    name = soup.select("div.wrp_lst > table.lst_board.lst_fixed.w123 > tbody > tr > td.name")
    page = []

    # 기초 정보(등 번호, 이름)를 제외하고 가져오기
    for i in range(5):
        page.append(soup.select("div.wrp_lst > table.lst_board.lst_scroll.w837.record_" + str(i + 1) + " > tbody > tr"))

    ours = int(e2.get())
    theirs = int(e3.get())
    fileName = e4.get()

    # 홈팀인 경우
    if int(radVar.get()) == 1:
        # 문자 전처리
        for i in range(5):
            for j in range(ours):
                page[i][j] = page[i][j].text.replace('\n', '', 1)  # 맨 처음에 나오는 \n은 그냥 없애줌
                page[i][j] = page[i][j].replace('\n', ' ')  # 그 다음에 나오는 \n은 스페이스 처리
                if i == 0:
                    page[i][j] = page[i][j].replace('O', '■')  # 출전세트 : 꽉 찬 네모로 만들어주기
                    page[i][j] = page[i][j].replace('\xa0', '-')  # 출전하지 않은 세트는 -로 표시

        temp_list = []
        for i in range(ours):
            temp_list.append(
                [
                    no[i].text,
                    name[i].text,
                    page[0][i].rstrip().split(' '),
                    page[1][i].rstrip().split(' '),
                    page[2][i].rstrip().split(' '),
                    page[3][i].rstrip().split(' '),
                    page[4][i].rstrip().split(' ')
                ]
            )

        # 이중 리스트 -> 단순 리스트
        for i in range(ours):
            temp_list[i] = flatten(temp_list[i])
            temp_list[i] = [item for item in temp_list[i] if item != '']

    # 원정팀인 경우
    else:
        # 문자 전처리
        for i in range(5):
            for j in range(ours, ours+theirs):
                page[i][j] = page[i][j].text.replace('\n', '', 1)  # 맨 처음에 나오는 \n은 그냥 없애줌
                page[i][j] = page[i][j].replace('\n', ' ')  # 그 다음에 나오는 \n은 스페이스 처리
                if i == 0:
                    page[i][j] = page[i][j].replace('O', '■')  # 출전세트 : 꽉 찬 네모로 만들어주기
                    page[i][j] = page[i][j].replace('\xa0', '-')  # 출전하지 않은 세트는 -로 표시

        temp_list = []
        for i in range(ours, ours+theirs):
            temp_list.append(
                [
                    no[i].text,
                    name[i].text,
                    page[0][i].rstrip().split(' '),
                    page[1][i].rstrip().split(' '),
                    page[2][i].rstrip().split(' '),
                    page[3][i].rstrip().split(' '),
                    page[4][i].rstrip().split(' ')
                ]
            )

        # 이중 리스트 -> 단순 리스트
        for i in range(theirs):
            temp_list[i] = flatten(temp_list[i])
            temp_list[i] = [item for item in temp_list[i] if item != '']

    column_list = ['No.', '이름', '1set', '2set', '3set', '4set', '5set', '득점', '시도', '성공', '공격차단', '범실', '성공률', '점유율',
                   '시도', '성공', '공격차단', '범실', '성공률', '점유율', '시도', '성공', '공격차단', '범실', '성공률', '점유율', '시도', '성공', '공격차단',
                   '범실', '성공률', '점유율',
                   '시도', '성공', '공격차단', '범실', '성공률', '점유율', '시도', '성공', '공격차단', '범실', '성공률', '점유율', '시도', '성공', '공격차단',
                   '범실', '성공률', '점유율',
                   '시도', '성공', '범실', '성공률', '점유율', '시도', '성공', '실패', '범실', '세트당', '점유율', '시도', '성공', '범실', '세트당', '점유율',
                   '시도', '정확', '실패', '세트당', '점유율', '시도', '성공', '유효블락', '실패', '범실', '세트당', '점유율', '어시스트', '벌칙', '범실']
    data = pd.DataFrame(temp_list, columns=column_list)
    data.to_csv('/Users/hansubin/Downloads/'+fileName+'.csv', index=False, encoding="euc-kr")


#GUI 생성
root = Tk()
root.title("여자 배구 크롤러")

# 라디오 버튼
radVar = IntVar()
r1 = ttk.Radiobutton(root, text = "홈팀", variable = radVar, value = 1)
r1.grid(column = 0, row = 0)
r2 = ttk.Radiobutton(root, text = "원정팀", variable = radVar, value = 2)
r2.grid(column = 1, row = 0)

# URL, 선수 명수, 파일명 입력
l1 = Label(root, text = "URL")
l1.grid(row = 1, column = 0)
l2 = Label(root, text = "홈팀 선수 수")
l2.grid(row = 2, column = 0)
l3 = Label(root, text = "원정팀 선수 수")
l3.grid(row = 3, column = 0)
l4 = Label(root, text = "파일명")
l4.grid(row = 4, column = 0)

e1 = Entry(root)
e1.grid(row = 1, column = 1)
e2 = Entry(root)
e2.grid(row = 2, column = 1)
e3 = Entry(root)
e3.grid(row = 3, column = 1)
e4 = Entry(root)
e4.grid(row = 4, column = 1)

# 크롤링 버튼
b1 = Button(root, text = "크롤링", command = process)
b1.grid(row = 5, column = 0, columnspan = 2)

root.mainloop()