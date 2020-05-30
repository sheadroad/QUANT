import pymysql
import webreader

def insertStockInfo(df_stock_code):
    conn = pymysql.connect(host='localhost', user='quantadmin', password='quantadmin$01',
                           db='quant', charset='utf8')

    curs = conn.cursor()
    sql = """insert into STOCK_INFO(stock_code,stock_name,stock_type,use_yn)
             values (%s, %s, %s, %s)"""

    print("종목 정보 INSERT 시작. 전체 건수" + str(len(df_stock_code)))

    for i, row in df_stock_code.iterrows():
        curs.execute(sql, (row['code'], row['name'], '', 'Y'))

        if (i % 100 == 0):
            print("{}번째 완료".format(i))

    print("종목 정보 INSERT 끝")

    conn.commit()
    conn.close()

def select_all_stock_info():
    conn = pymysql.connect(host='localhost', user='quantadmin', password='quantadmin$01',
                           db='quant', charset='utf8')

    # Connection 으로부터 Dictoionary Cursor 생성
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = """select stock_code, stock_name
               from STOCK_INFO
          """

    # SQL문 실행
    curs.execute(sql)
    all_stock_list = curs.fetchall()
    conn.close()

    return all_stock_list

def insert_stock_history(stock_code, stock_history):
    conn = pymysql.connect(host='localhost', user='quantadmin', password='quantadmin$01',
                           db='quant', charset='utf8')
    curs = conn.cursor()
    sql = """insert into STOCK_HISTORY(stock_code,date,open,high,low,close,volume)
             values (%s, %s, %s, %s, %s, %s, %s)"""

    for row in stock_history:
        # print(row)
        curs.execute(sql, (stock_code, row[0], row[1], row[2], row[3], row[4], row[5]))

    print("{} ::: 종목 히스토리 INSERT 끝".format(str(stock_code)))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # df_stock_code = webreader.get_stock_code()
    # insertStockInfo(df_stock_code)

    all_stock_list = select_all_stock_info()

    for stock in all_stock_list:
        # 일별 주가 데이터 가져오기(1주 = 5일, 1년 = 260일, 10년 = 2600일)
        stock_history = webreader.get_stock_history(stock['stock_code'], 2600)
        insert_stock_history(stock['stock_code'], stock_history)


    # storckHistory = webreader.get_stock_history('307950',1)
    # print(storckHistory)