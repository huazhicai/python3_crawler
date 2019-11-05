# -*- coding: gb2312 -*-
import pymssql

# pymssql==2.1.1

conn = pymssql.connect(host='10.0.30.3', port=1433, user='sa', password='Huamai521', database='master', charset='utf8')

cur = conn.cursor()

# cur.execute('select a from 新表名')
# cur.execute('select * from bbb')

cur.execute("""
IF OBJECT_ID('persons', 'U') IS NOT NULL
    DROP TABLE persons
CREATE TABLE persons (
    id INT NOT NULL,
    name VARCHAR(100),
    salesrep VARCHAR(100),
    PRIMARY KEY(id)
)
""")

cur.executemany(
    "insert into persons values (%d, %s, %s)",
    [(1, 'steven', 'John Doe'),
     (2, '杭州', '浙江'),
     (3, '北京', '中国'),
     (4, '温州', '浙江')]
)

conn.commit()

cur.execute('select %s, %s from persons' % tuple(['ID', 'Name']))
row = cur.fetchone()

while row:
    print('ID=%d, Name=%s' % (row[0], row[1].encode('latin-1').decode('gbk')))
    row = cur.fetchone()

# raw = cur.fetchall()
# print(raw)
#
# for i in raw:
#     print(i[0].encode('latin-1').decode('gbk'))

cur.close()
conn.close()
