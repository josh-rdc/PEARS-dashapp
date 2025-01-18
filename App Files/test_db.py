import apps.dbconnect as db

def addfewgenres():
    sqlcode = """ INSERT INTO genres (
        genre_name,
        genre_modified_date,
        genre_delete_ind
        )

    VALUES (%s, %s, %s)"""
    from datetime import datetime

    # If the SQL has no placeholders, use an empty list (i.e. [])
    db.modifydatabase(sqlcode, ['Action', datetime.now(), False])
    db.modifydatabase(sqlcode, ['Horror', datetime.now(), False])

    print('done!')

addfewgenres()

sql_query = """ SELECT * FROM genres"""
values = []
# number of column names must match the attributes for table genres
columns = ['id', 'name', 'modified', 'is_deleted']

df = db.querydatafromdatabase(sql_query, values, columns)
print(df)

sql_resetgenres = """
 TRUNCATE TABLE genres RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetgenres, [])
addfewgenres()
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)