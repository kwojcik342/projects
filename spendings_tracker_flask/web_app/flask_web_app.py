from flask import Flask, render_template, request, redirect, url_for, session
import db_opers as dbo
import pygal as pg
import bcrypt
from datetime import date, datetime


app = Flask(__name__)
app.secret_key = "test1"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "inputLogin" in request.values and "inputPassword" in request.values:
            usern = request.values["inputLogin"]
            # id_usr = dbo.get_user_id(usern)
            db_resp = dbo.get_user_id_pwd(usern)
            id_usr = int(db_resp["id_user"])
            if id_usr > 0:
                is_pwd_valid = bcrypt.checkpw(request.values["inputPassword"].encode('utf-8'), db_resp["hashed_pwd"].encode('utf-8'))
                if is_pwd_valid:
                    session["id_user"] = id_usr
                    return redirect(url_for("user_page"))
                else:
                    return redirect(url_for("home"))
            else:
                return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    else:
        if "id_user" in session:
            return redirect(url_for("user_page"))
        else:
            return render_template("index.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if request.method == "GET":
        return render_template("create_account.html")
    elif request.method == "POST":
        if "inputNewLogin" in request.values and "inputNewPassword" in request.values:
            pwd_hash = bcrypt.hashpw(request.values["inputNewPassword"].encode('utf-8'), bcrypt.gensalt())
            password_hashed = pwd_hash.decode('utf-8')
            id_user = dbo.insert_user_w_pwd(request.values["inputNewLogin"], password_hashed)
            if id_user > 0:
                return redirect(url_for("home"))
            else:
                return redirect(url_for("create_account"))
        else:
            return redirect(url_for("create_account"))


@app.route("/user_page", methods=["POST", "GET"])
def user_page():
    if "id_user" in session:
        id_user = session["id_user"]

        # handling deletes and inserts
        if request.method == "POST":
            if "fin_inc_tmst" in request.values:
                tmp_tmst = request.values["fin_inc_tmst"]
                tmp_tmst = tmp_tmst[0:10] + " " + tmp_tmst[11:] + ":00"
                res = dbo.insert_income(id_user, request.values["fin_inc_am"], tmp_tmst, request.values["fin_inc_usr_note"])
                if res < 0:
                    pass
            if "fin_id_inc_del" in request.values:
                l_id_inc_del = []
                l_id_inc_del.append(int(request.values["fin_id_inc_del"]))
                res = dbo.delete_incomes(l_id_inc_del)
                if res < 0:
                    pass   
            if "fin_sp_tmst" in request.values:
                tmp_tmst = request.values["fin_sp_tmst"]
                tmp_tmst = tmp_tmst[0:10] + " " + tmp_tmst[11:] + ":00"
                res = dbo.insert_spending(id_user, request.values["fin_sp_am"], tmp_tmst, request.values["fin_sp_usr_note"])
                if res < 0:
                    pass
            if "fin_id_sp_del" in request.values:
                l_id_inc_del = []
                l_id_inc_del.append(int(request.values["fin_id_sp_del"]))
                res = dbo.delete_spendings(l_id_inc_del)
                if res < 0:
                    pass     

        # we always get some data from db so the page doesn't appear empty 
        usr_inc = dbo.get_user_incomes(id_user)

        # getting data for chart comparing spendings to incomes in past 12 months
        max_inc_num = 11
        start_date = ""
        end_date = ""
        l_months =[]
        l_inc = []
        l_sp_sum = []
        for index, inc in enumerate(usr_inc):
            if index > max_inc_num:
                break
            # print(index, inc) 
            inc_amount = 0
            sp_sum = 0
            end_date = start_date
            start_date = inc["inc_tmst"]
            month = int(start_date[5:7])+1
            if month == 13:
                month = 1
            inc_amount = inc["inc_amount"] 
            d_sp = dbo.get_user_spendings(id_user, start_date, end_date)
            for sp in d_sp:
                sp_sum += sp["sp_amount"]

            l_months.append(month)
            l_inc.append(inc_amount)
            l_sp_sum.append(sp_sum)

        monthly_chart = pg.Bar()
        monthly_chart.x_labels = map(str, l_months)
        monthly_chart.add("income", l_inc)
        monthly_chart.add("spendings", l_sp_sum)
        chart_m_data = monthly_chart.render_data_uri()

        # getting data for chart comparing spendings to incomes
        # if user selected incomes from table we compare spendings between min and max date of selected incomes
        # if only one date was selected by user we show comparison between that date and current date
        # if no date is selected or it's GET request we show spendings after latest income and compare them to latest income
        if request.method == "POST" and "spCheckbox" in request.form:
            boxSelected = request.form.getlist("spCheckbox")
            if len(boxSelected) == 1:
                for inc in usr_inc:
                    if inc["id_income"] == int(boxSelected[0]):
                        sp_st_date = inc["inc_tmst"]
                        session["sp_st_date"] = sp_st_date
                        sp_end_date = ""
                        session["sp_end_date"] = sp_end_date
                        break
            elif len(boxSelected) > 1:
                l_sel_inc_dates = []
                for chb in boxSelected:
                    for inc in usr_inc:
                        if inc["id_income"] == int(chb):
                            l_sel_inc_dates.append(datetime.strptime(inc["inc_tmst"], "%Y-%m-%d %H:%M:%S"))
                l_sel_inc_dates.sort()
                sp_st_date = str(l_sel_inc_dates[0])
                session["sp_st_date"] = sp_st_date
                sp_end_date = str(l_sel_inc_dates[-1])
                session["sp_end_date"] = sp_end_date
        elif request.method == "GET" or (request.method == "POST" and "spCheckbox" not in request.form):
            if "sp_st_date" in session:
                sp_st_date = session["sp_st_date"]
            else:
                if len(usr_inc) > 0:
                    sp_st_date = usr_inc[0]["inc_tmst"]
                else:
                    sp_st_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

            if "sp_end_date" in session:
                sp_end_date = session["sp_end_date"]
            else:
                sp_end_date = ""

        l_usr_spendings = dbo.get_user_spendings(id_user, sp_st_date, sp_end_date)

        # summing up spendings amounts
        sum_sp = 0.00
        l_sum_sp = []
        for spd in l_usr_spendings:
            sum_sp += spd["sp_amount"]
        l_sum_sp.append(sum_sp)

        # if user selected only one date we set end date as today so the label on the chart isn't empty
        if sp_end_date == "":
            sp_end_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

        # summing up incomes between selected dates
        sum_inc = 0.00
        l_sum_inc = []
        dt_start = datetime.strptime(sp_st_date, "%Y-%m-%d %H:%M:%S")
        dt_end = datetime.strptime(sp_end_date, "%Y-%m-%d %H:%M:%S")
        for inc in usr_inc:
            dt_inc = datetime.strptime(inc["inc_tmst"], "%Y-%m-%d %H:%M:%S")
            if dt_inc >= dt_start and dt_inc < dt_end:
                sum_inc += inc["inc_amount"]
        l_sum_inc.append(sum_inc)

        sp2inc_chart = pg.Bar()
        sp2inc_chart.x_labels = [sp_st_date + " - " + sp_end_date]
        sp2inc_chart.add("incomes", l_sum_inc)
        sp2inc_chart.add("spendings", l_sum_sp)
        chart_sp2inc_data = sp2inc_chart.render_data_uri()

        return render_template("user_page.html"
                                , chartinc=chart_m_data
                                , j_incomes=usr_inc
                                , j_spendings=l_usr_spendings
                                , chartsp2inc=chart_sp2inc_data)
    else:
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("id_user", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()