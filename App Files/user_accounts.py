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
    db.modifydatabase(sqlcode, ['240517', 'fcba8051ec9c89dfa788d2e093b54765629bc153237a2a4d26c0ae959500b4c5', 'manager', False]) # Password01
    db.modifydatabase(sqlcode, ['240518', '246a023c642223fd23de36646b8af24e26573010b4ca0b1c6e2c44630a744440', 'pj_ic', False]) # Password02
    db.modifydatabase(sqlcode, ['240519', 'af43e7c0b34ff2b49bb5f83fccd4405b3e3d1e376714fd97fac60d3ff603d079', 'pj_ic', False]) # Pasword03
    db.modifydatabase(sqlcode, ['240520', '574a14bdbb39813e68cf9de4fc163586cc6491bf34d9ceac7e89378af66c496c', 'pj_ic', False]) # Password04

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

