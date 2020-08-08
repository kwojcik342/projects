import psycopg2


def get_user_id(in_username):
    q_select_user = "select id_user from users where username=(%s)"
    id_user = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_select_user, (in_username,))
        id_user = db_cur.fetchone()[0]
        print("selected user id: " + str(id_user))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_user


def insert_user(in_username):
    q_insert_usr = "insert into users (username) values (%s) returning id_user;"
    id_user = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_insert_usr, (in_username,))
        id_user = db_cur.fetchone()[0]
        db_con.commit()
        print("Added new user with id= " + str(id_user))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_user


def get_user_id_pwd(in_username):
    q_select_user = "select id_user, hashed_pwd from users where username=(%s)"
    l_user_data = []
    d_resp = {}
    db_con = None
    l_user_js_tags = ["id_user", "hashed_pwd"]
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_select_user, (in_username,))
        l_user_data = db_cur.fetchall()
        # print("selected user id: " + str(id_user))
        db_cur.close()
        if len(l_user_data) > 0:
            l_user_data = [l_user_data[0][0], l_user_data[0][1]]
            d_resp = dict(zip(l_user_js_tags, l_user_data))
        else:
            d_resp = {
                "id_user": -1
            }
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return d_resp
        

def insert_user_w_pwd(in_username, in_hash_pwd):
    q_insert_usr = "insert into users (username, hashed_pwd) values (%s,%s) returning id_user;"
    id_user = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_insert_usr, (in_username, in_hash_pwd,))
        id_user = db_cur.fetchone()[0]
        db_con.commit()
        print("Added new user with id= " + str(id_user))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_user


def insert_income(in_id_user, in_inc_amount, in_inc_tmstmp, in_income_note):
    q_insert_inc = "insert into user_incomes (id_user, income_amount, income_timestamp, income_user_note) values (%s,%s,%s,%s) returning id_income;"
    id_income = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_insert_inc, (in_id_user, in_inc_amount, in_inc_tmstmp, in_income_note,))
        id_income = db_cur.fetchone()[0]
        db_con.commit()
        print("Added new income with id= " + str(id_income))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_income


def update_income(in_id_income, in_inc_amount, in_inc_tmstmp, in_income_note):
    q_update_inc = "update user_incomes set income_amount=%s, income_timestamp=%s, income_user_note=%s where id_income=%s;"
    id_income = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_update_inc, (in_inc_amount, in_inc_tmstmp, in_income_note, in_id_income))
        id_income = 1
        db_con.commit()
        print("Updated income with id= " + str(in_id_income))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_income


def delete_incomes(in_inc_list):
    q_delete_inc = "delete from user_incomes where id_income =%s;"
    id_income = -1
    db_con = None
    inc_list = []
    for inc in in_inc_list:
        inc_list.append(tuple((inc, )))
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.executemany(q_delete_inc, inc_list)
        id_income = 1
        db_con.commit()
        print("Deleted incomes with id= " + str(in_inc_list))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_income


def get_user_incomes(in_id_user):
    q_sel_inc = "select id_income, income_amount, income_timestamp, income_user_note from user_incomes where id_user = %s order by income_timestamp desc;"
    incomes_list = []
    l_resp = []
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_sel_inc, (in_id_user,))
        incomes_list = db_cur.fetchall()

        l_inc_js_tags = ["id_income", "inc_amount", "inc_tmst", "inc_note"]
        for inc in incomes_list:
            l_tmp = [inc[0], float(inc[1]), inc[2].strftime("%Y-%m-%d %H:%M:%S"), inc[3]]
            d_tmp = dict(zip(l_inc_js_tags, l_tmp))
            l_resp.append(d_tmp)

        print("Selected " + str(db_cur.rowcount) + " incomes where id_user= " + str(in_id_user))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return l_resp


def insert_spending(in_id_user, in_sp_amount, in_sp_tmstmp, in_sp_note):
    q_insert_sp = "insert into user_spendings (id_user, spending_amount, spending_timestamp, spending_user_note) values (%s,%s,%s,%s) returning id_spending;"
    id_spending = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_insert_sp, (in_id_user, in_sp_amount, in_sp_tmstmp, in_sp_note,))
        id_spending = db_cur.fetchone()[0]
        db_con.commit()
        print("Added new spending with id= " + str(id_spending))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_spending


def update_spending(in_id_spending, in_sp_amount, in_sp_tmstmp, in_sp_note):
    q_update_sp = "update user_spendings set spending_amount=%s, spending_timestamp=%s, spending_user_note=%s where id_spending=%s;"
    id_spending = -1
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.execute(q_update_sp, (in_sp_amount, in_sp_tmstmp, in_sp_note, in_id_spending,))
        id_spending = 1
        db_con.commit()
        print("Updated spending with id= " + str(in_id_spending))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_spending


def delete_spendings(in_sp_list):
    q_delete_sp = "delete from user_spendings where id_spending =%s;"
    id_spending = -1
    db_con = None
    sp_list = []
    for sp in in_sp_list:
        sp_list.append(tuple((sp, )))
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()
        db_cur.executemany(q_delete_sp, sp_list)
        id_spending = 1
        db_con.commit()
        print("Deleted spendings with id= " + str(in_sp_list))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return id_spending


def get_user_spendings(in_id_user, in_start_date, in_end_date):
    q_sel_sp = "select id_spending, spending_amount, spending_timestamp, spending_user_note from user_spendings where id_user = %s order by spending_timestamp desc;"
    q_sel_sp_sd = "select id_spending, spending_amount, spending_timestamp, spending_user_note from user_spendings where id_user = %s and spending_timestamp >= %s order by spending_timestamp desc;"
    q_sel_sp_ed = "select id_spending, spending_amount, spending_timestamp, spending_user_note from user_spendings where id_user = %s and spending_timestamp <= %s order by spending_timestamp desc;"
    q_sel_sp_md = "select id_spending, spending_amount, spending_timestamp, spending_user_note from user_spendings where id_user = %s and spending_timestamp >= %s and spending_timestamp <= %s order by spending_timestamp desc;"

    spendings_list = []
    l_resp = []
    db_con = None
    try:
        db_con = psycopg2.connect(host="localhost", database="SpendingTracker_DB", user="st_server_db_user", password="user123")
        db_cur = db_con.cursor()

        if in_start_date != "" and in_end_date != "":
            db_cur.execute(q_sel_sp_md, (in_id_user, in_start_date, in_end_date,))
        elif in_start_date != "" and in_end_date == "":
            db_cur.execute(q_sel_sp_sd, (in_id_user, in_start_date,))
        elif in_start_date == "" and in_end_date != "":
            db_cur.execute(q_sel_sp_ed, (in_id_user, in_end_date,))
        else:
            db_cur.execute(q_sel_sp, (in_id_user,))

        spendings_list = db_cur.fetchall()

        l_sp_js_tags = ["id_spending", "sp_amount", "sp_tmst", "sp_note"]
        for sp in spendings_list:
            l_tmp = [sp[0], float(sp[1]), sp[2].strftime("%Y-%m-%d %H:%M:%S"), sp[3]]
            d_tmp = dict(zip(l_sp_js_tags, l_tmp))
            l_resp.append(d_tmp)

        # print("Selected " + str(db_cur.rowcount) + " spendings where id_user= " + str(in_id_user) + " between dates: " + str(in_start_date) + " and " + str(in_end_date))
        db_cur.close()
    except psycopg2.DatabaseError as err:
        print(err)
    finally:
        if db_con is not None:
            db_con.close()
        return l_resp
