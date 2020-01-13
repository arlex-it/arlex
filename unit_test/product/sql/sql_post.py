# with engine.connect() as con:
#     rs = con.execute("INSERT INTO log (date_insert, code, data) VALUES (\'"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\', 1, \'blabla\')")

# with engine.connect() as con:
#     rs = con.execute('SELECT * FROM log')
#     for row in rs:
#         print(row)

import datetime


def create_product(engine):
    with engine.connect() as con:
        rs = con.execute("INSERT INTO log (date_insert, code, data) VALUES (\'"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\', 1, \'blabla\')")

    with engine.connect() as con:
        rs = con.execute('SELECT * FROM log')
        for row in rs:
            print(row)
