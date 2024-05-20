import apps.dbconnect as db

def add_user():
    sqlcode = """ INSERT INTO users (
        userid,
        password,
        user_type,
        user_del_ind
        )

    VALUES (%s, %s, %s, %s)"""

    # If the SQL has no placeholders, use an empty list (i.e. [])

    # Modify to add user account and passwords
    db.modifydatabase(sqlcode, ['240517', 'Password01', 'manager', False])
    db.modifydatabase(sqlcode, ['240518', 'Password02', 'pj_ic', False])
    db.modifydatabase(sqlcode, ['240519', 'Password03', 'pj_ic', False])
    db.modifydatabase(sqlcode, ['240520', 'Password04', 'pj_ic', False])

    print('done!')


sql_query = """ SELECT * FROM users"""
values = []
# number of column names must match the attributes for table 
columns = ['userid', 'password', 'user_type', 'user_del_ind']

df = db.querydatafromdatabase(sql_query, values, columns)

sql_resetusers = """
 TRUNCATE TABLE users RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetusers, [])
add_user()
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)

