from flask import Flask

app = Flask(__name__)
app.users_by_id = {}
class User:
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name
    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}

    # accept either "id" or "user_id"
    user_id = data.get("id", data.get("user_id"))
    name = data.get("name")
    new_user = User(user_id=user_id, name=str(name))

    if user_id in app.users_by_id:
        return jsonify({"error": f"User with id={user_id} already exists."}), 409

    app.users_by_id[user_id] = new_user
    
    return jsonify({"created": user.to_dict(), "total_users": len(app.users_by_id)}), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify([u.to_dict() for u in app.users_by_id.values()]), 200



if __name__ == '__main__':
    app.run(debug=True)
    