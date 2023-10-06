import sqlite3


def add_user(name):

    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
     select * from 
     users
     where name='{name}';
     """)

    res = a.fetchall()

    if not res:

        cur.execute(f"""
            insert into users (name)
            values('{name}');
            """)

        buy_skin(1, name, 0)

    bd.commit()
    bd.close()


def lb():
    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select * from users
        ORDER by best_score DESC 
        limit 3;
        """)

    res = a.fetchall()

    bd.commit()
    bd.close()

    return res


def user_info(name):
    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        SELECT * from users
        where name ='{name}';
            """)

    res = a.fetchall()

    bd.commit()
    bd.close()

    return res


def add_score(name, score):

    info = user_info(name)

    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    if score > info[0][3]:
        cur.execute(f"""
            update users 
            set best_score = {score}
            where name = '{name}';
            """)

    cur.execute(f"""
        update users 
        set balance = {score + info[0][2]}
        where name = '{name}';
                """)

    bd.commit()
    bd.close()


def user_hs(name, skin):

    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select * from users_skins
        join users on users.user_id = users_skins.user_id
        where name = '{name}' and skin_id = {skin};
                """)

    res = a.fetchall()

    bd.commit()
    bd.close()

    if not res:
        return False
    return True


def get_skin_info(skin_id):

    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        SELECT * from skins
        where skin_id = "{skin_id}";
                    """)

    res = a.fetchall()

    info = {"cost": res[0][1], "color1": res[0][2],
            "color2": res[0][3], "width": res[0][4]}

    bd.commit()
    bd.close()

    return info


def buy_skin(skin, name, cost):

    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    info = user_info(name)

    balance = info[0][2]
    user_id = info[0][0]

    if balance >= cost:
        cur.execute(f"""
            insert into users_skins (user_id, skin_id)
            VALUES ({user_id}, {skin})
                            """)
        cur.execute(f"""
            update users
            set balance = {balance - cost}
            where name = '{name}'
                            """)

    bd.commit()
    bd.close()

def user_skins(user_name):
    bd = sqlite3.connect("db.db")

    cur = bd.cursor()

    a = cur.execute(f"""
        select skin_id from users_skins
        WHERE user_id = {user_name};
                    """)

    res = a.fetchall()

    skin_list = []

    for i in res:
        skin_list.append(i[0])

    bd.commit()
    bd.close()

    return skin_list