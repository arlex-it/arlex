# with engine.connect() as con:
#     rs = con.execute("INSERT INTO log (date_insert, code, data) VALUES (\'"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\', 1, \'blabla\')")

# with engine.connect() as con:
#     rs = con.execute('SELECT * FROM log')
#     for row in rs:
#         print(row)

import datetime
from sqlalchemy.sql import text


def delete_all_products(engine):
    with engine.connect() as con:
        con.execute("delete from product;")
        # con.execute("ALTER TABLE product AUTO_INCREMENT = 1;")

def create_product(engine):
    with engine.connect() as con:
        query = text("INSERT INTO product (date_insert, date_update, expiration_date, status, id_rfid, id_ean, position, id_user) VALUES (:di, :du, :ed, :s, :idr, :ide, :pos, :idu)")
        rs = con.execute(query,
                         di=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         du=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         ed="2019-11-30 00:00:00",
                         s=0,
                         idr=123,
                         ide="3017620424403",
                         pos="Sous levier",
                         idu=1)
        rs = con.execute("select * from product")
        d, a = {}, []
        for rowproxy in rs:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        print("#####", d['id'], "#####")
        con.close()
        return d['id']
    # with engine.connect() as con:
    #     rs = con.execute('SELECT * FROM log')
    #     for row in rs:
    #         print(row)
