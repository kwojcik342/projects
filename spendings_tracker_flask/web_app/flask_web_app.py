from flask import Flask, render_template, request, redirect, url_for, session
import db_opers as dbo
import pygal as pg


app = Flask(__name__)
app.secret_key = "test1"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        usern = request.values["inputLogin"]
        id_usr = dbo.get_user_id(usern)
        session["id_user"] = id_usr
        if id_usr < 0:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("user_page"))
    else:
        if "id_user" in session:
            return redirect(url_for("user_page"))
        else:
            return render_template("index.html")


@app.route("/user_page", methods=["POST", "GET"])
def user_page():
    if "id_user" in session:
        id_user = session["id_user"]

        if request.method == "POST":
            if "fin_inc_tmst" in request.values:
                tmp_tmst = request.values["fin_inc_tmst"]
                tmp_tmst = tmp_tmst[0:10] + " " + tmp_tmst[11:] + ":00"
                res = dbo.insert_income(id_user, request.values["fin_inc_am"], tmp_tmst, request.values["fin_inc_usr_note"])
                if res < 0:
                    pass
            if "id_inc_del" in request.values:
                l_id_inc_del = []
                l_id_inc_del.append(int(request.values["id_inc_del"]))
                res = dbo.delete_incomes(l_id_inc_del)
                if res < 0:
                    pass

        usr_inc = dbo.get_user_incomes(id_user)

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
            d_sp = dbo.get_user_spendings(3, start_date, end_date)
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

        return render_template("user_page.html"
                                , chart=chart_m_data
                                , j_incomes=usr_inc)
    else:
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("id_user", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()