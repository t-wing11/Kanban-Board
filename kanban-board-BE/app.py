from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Task, KanbanColumn, User
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban_board.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.secret_key = "your_secret_key"

    with app.app_context():
        db.drop_all()
        db.create_all()

        if KanbanColumn.query.count() == 0:
            columns = [
                KanbanColumn(id=1, title="To Do"),
                KanbanColumn(id=2, title="In Progress"),
                KanbanColumn(id=3, title="Done"),
            ]
            db.session.bulk_save_objects(columns)
            db.session.commit()

        if User.query.count() == 0:
            admin = User(
                id=1,
                username="admin",
                password="admin123"
            )
            db.session.add(admin)
            db.session.commit()
        
        @app.route("/kanban_board", methods=["GET"])
        @login_required
        def get_board():
            columns = db.session.query(KanbanColumn).all()
            return jsonify([column.to_dict() for column in columns])

        @app.route("/kanban_board", methods=["POST"])
        @login_required
        def create_task():
            data = request.json
            new_task = Task(
                id=data["id"],
                title=data["title"],
                description=data["description"],
                status=data["status"],
                due_date=data.get("due_date", None),
                tags=",".join(data.get("tags", [])),
            )
            db.session.add(new_task)
            db.session.commit()
            db.session.refresh(new_task)
            return jsonify(new_task.to_dict()), 201

        @app.route("/kanban_board/<int:task_id>", methods=["PUT"])
        @login_required
        def update_task(task_id):
            data = request.json
            task = db.session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            task.title = data["title"]
            task.description = data["description"]
            task.status = data["status"]
            task.due_date = data.get("due_date", None)
            task.tags = ",".join(data.get("tags", []))
            db.session.commit()
            return jsonify(task.to_dict())

        @app.route("/kanban_board/<int:task_id>", methods=["DELETE"])
        @login_required
        def delete_task(task_id):
            task = db.session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted successfully"}), 204


        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route("/kanban_board/login", methods=["POST"])
        def login():
            data = request.json
            Username = data.get("username")
            Password = data.get("password")

            user = User.query.filter_by(username=Username, password=Password).first()
            if user and user.password == Password:
                login_user(user)
                return jsonify({"message": "Login successful"}), 200
            
            return jsonify({"error": "Invalid credentials"}), 401

        @app.route("/kanban_board/logout", methods=["POST"])
        @login_required
        def logout():
            logout_user()
            return jsonify({"message": "Logout successful"}), 200
            
        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
