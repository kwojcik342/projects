import requests
import json

st_api_url = "http://127.0.0.1:5000/spendingstracker/api/"


def req_get_user_id(in_username):
    url = st_api_url + "/users/" + in_username

    resp = requests.get(url)
    # print(resp.status_code)
    # print(resp.json())
    json_resp = resp.json()
    # print("user id: " + str(json_resp["id_user"]))
    id_user = json_resp["id_user"]
    return id_user

# INCOMES HANDLING


def req_post_income(in_id_user, in_inc_amount, in_inc_tmst, in_inc_note):
    url = st_api_url + "incomes/addincome"
    js = {"id_user": in_id_user, 
        "inc_amount": in_inc_amount,
        "inc_tmst": in_inc_tmst,
        "inc_note": in_inc_note}
    resp = requests.post(url, json=js)

    print(resp.status_code)
    print(resp.json())


def req_put_income(in_id_income, in_inc_amount, in_inc_tmst, in_inc_note):
    url = st_api_url + "incomes/updateincome"
    js = {"id_income": in_id_income, 
        "inc_amount": in_inc_amount,
        "inc_tmst": in_inc_tmst,
        "inc_note": in_inc_note}
    resp = requests.put(url, json=js)

    print(resp.status_code)
    print(resp.json())

def req_get_user_incomes(in_id_user):
    url = st_api_url + "incomes/getincomes"
    js = {"id_user": in_id_user}
    resp = requests.get(url, json=js)

    print(resp.status_code)
    print(resp.json())

# SPENDINGS HANDLING


def req_post_spending(in_id_user, in_sp_amount, in_sp_tmst, in_sp_note):
    url = st_api_url + "spendings/addspending"
    js = {"id_user": in_id_user, 
        "sp_amount": in_sp_amount,
        "sp_tmst": in_sp_tmst,
        "sp_note": in_sp_note}
    resp = requests.post(url, json=js)

    print(resp.status_code)
    print(resp.json())


def req_put_spending(in_id_spending, in_sp_amount, in_sp_tmst, in_sp_note):
    url = st_api_url + "spendings/updatespending"
    js = {"id_spending": in_id_spending, 
        "sp_amount": in_sp_amount,
        "sp_tmst": in_sp_tmst,
        "sp_note": in_sp_note}
    resp = requests.put(url, json=js)

    print(resp.status_code)
    print(resp.json())


def req_get_user_spendings(in_id_user):
    url = st_api_url + "spendings/getspendings"
    js = {"id_user": in_id_user}
    resp = requests.get(url, json=js)

    print(resp.status_code)
    print(resp.json())


if __name__ == "__main__":
    usern = "k.wojcik"
    # print(req_get_user_id(usern))

    # req_post_income(3, 3500, "2020-07-30 09:10:30", "wyplata")
    # req_get_user_incomes(3)
    # req_put_income(5, 3333, "2020-07-30 09:10:30", "wyplata")

    # req_post_spending(3, 223.34, "2020-07-30 09:10:30", "zakup klawiatury")
    # req_put_spending(12, 255.12, "2020-07-30 09:10:30", "zakup myszy")
    req_get_user_spendings(3)