from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Task, KanbanColumn


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kanban_board.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    CORS(app)
    with app.app_context():
        db.create_all()

        if KanbanColumn.query.count() == 0:
            columns = [
                KanbanColumn(id=1, title="To Do"),
                KanbanColumn(id=2, title="In Progress"),
                KanbanColumn(id=3, title="Done"),
            ]
            db.session.bulk_save_objects(columns)
            db.session.commit()
            print("Seeded columns!")

        @app.route("/kanban_board", methods=["GET"])
        def get_board():
            columns = db.session.query(KanbanColumn).all()
            return jsonify([column.to_dict() for column in columns])

        @app.route("/kanban_board", methods=["POST"])
        def create_task():
            data = request.json
            new_task = Task(
                id=data["id"],
                title=data["title"],
                description=data["description"],
                status=data["status"],
            )
            db.session.add(new_task)
            db.session.commit()
            db.session.refresh(new_task)
            return jsonify(new_task.to_dict()), 201

        @app.route("/kanban_board/<int:task_id>", methods=["PUT"])
        def update_task(task_id):
            data = request.json
            task = db.session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            task.title = data["title"]
            task.description = data["description"]
            task.status = data["status"]
            db.session.commit()
            return jsonify(task.to_dict())

        @app.route("/kanban_board/<int:task_id>", methods=["DELETE"])
        def delete_task(task_id):
            task = db.session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted successfully"}), 204

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
