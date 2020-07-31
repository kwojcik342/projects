import flask
import db_opers as dbo


app = flask.Flask(__name__)
# GET
# POST  - create new
# PUT   - update existing
# DELETE


@app.route("/")
def hello_world():
    return "Hello World!"


@app.errorhandler(400)
def bad_request(error):
    return flask.make_response((flask.jsonify({"error": "Bad Request"})), 400)


@app.errorhandler(404)
def not_found(error):
    return flask.make_response((flask.jsonify({"error": "Not found"})), 404)


@app.route("/spendingstracker/api/users/<string:username>", methods=["GET"])
def get_user_id(username):
    id_user = dbo.get_user_id(username)
    return flask.jsonify({"id_user": id_user})

# INCOMES HANDLING


@app.route("/spendingstracker/api/incomes", methods=["POST"])
def add_income():
    if not flask.request.json or "id_user" not in flask.request.json or "inc_amount" not in flask.request.json or "inc_tmst" not in flask.request.json:
        flask.abort(400)
    id_income = dbo.insert_income(flask.request.json["id_user"]
                                  , flask.request.json["inc_amount"]
                                  , flask.request.json["inc_tmst"]
                                  , flask.request.json.get("inc_note", ""))
    return flask.jsonify({"id_ncome": id_income})


@app.route("/spendingstracker/api/incomes", methods=["PUT"])
def upd_income():
    if not flask.request.json or "id_income" not in flask.request.json or "inc_amount" not in flask.request.json or "inc_tmst" not in flask.request.json:
        flask.abort(400)
    id_income = dbo.update_income(flask.request.json["id_income"]
                                  , flask.request.json["inc_amount"]
                                  , flask.request.json["inc_tmst"]
                                  , flask.request.json.get("inc_note", ""))
    return flask.jsonify({"id_ncome": id_income})


@app.route("/spendingstracker/api/incomes", methods=["GET"])
def get_user_incomes():
    if not flask.request.json or "id_user" not in flask.request.json:
        flask.abort(400)
    inc_list = dbo.get_user_incomes(flask.request.json["id_user"])
    return flask.jsonify({"incomes": inc_list})

# SPENDINGS HANDLING


@app.route("/spendingstracker/api/spendings", methods=["POST"])
def add_spending():
    if not flask.request.json or "id_user" not in flask.request.json or "sp_amount" not in flask.request.json or "sp_tmst" not in flask.request.json:
        flask.abort(400)
    id_spending = dbo.insert_spending(flask.request.json["id_user"]
                                        , flask.request.json["sp_amount"]
                                        , flask.request.json["sp_tmst"]
                                        , flask.request.json.get("sp_note", ""))
    return flask.jsonify({"id_spending": id_spending})


@app.route("/spendingstracker/api/spendings", methods=["PUT"])
def upd_spending():
    if not flask.request.json or "id_spending" not in flask.request.json or "sp_amount" not in flask.request.json or "sp_tmst" not in flask.request.json:
        flask.abort(400)
    id_spending = dbo.update_spending(flask.request.json["id_spending"]
                                  , flask.request.json["sp_amount"]
                                  , flask.request.json["sp_tmst"]
                                  , flask.request.json.get("sp_note", ""))
    return flask.jsonify({"id_spending": id_spending})


@app.route("/spendingstracker/api/spendings", methods=["GET"])
def get_user_spendings():
    if not flask.request.json or "id_user" not in flask.request.json:
        flask.abort(400)
    sp_list = dbo.get_user_spendings(flask.request.json["id_user"])
    return flask.jsonify({"spendings": sp_list})


if __name__ == "__main__":
    app.run()
