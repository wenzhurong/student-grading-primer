from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this


def _is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""


def _valid_mark(value):
    return isinstance(value, int) and 0 <= value <= 100


@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students: {str(e)}"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.get_json(silent=True)
    if not isinstance(student_data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)

    if not _is_non_empty_string(name):
        return jsonify({"error": "name is required and must be a non-empty string"}), 404
    if not _is_non_empty_string(course):
        return jsonify({"error": "course is required and must be a non-empty string"}), 404
    if not _valid_mark(mark):
        return jsonify({"error": "mark must be an integer between 0 and 100"}), 404

    try:
        created = db.insert_student(name.strip(), course.strip(), mark)
        return jsonify(created), 200
    except Exception as e:
        return jsonify({"error": f"Failed to create student: {str(e)}"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.get_json(silent=True)
    if not isinstance(student_data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if name is None and course is None and mark is None:
        return jsonify({"error": "At least one field (name, course, mark) is required"}), 404

    if name is not None and not _is_non_empty_string(name):
        return jsonify({"error": "name must be a non-empty string when provided"}), 404
    if course is not None and not _is_non_empty_string(course):
        return jsonify({"error": "course must be a non-empty string when provided"}), 404
    if mark is not None and not _valid_mark(mark):
        return jsonify({"error": "mark must be an integer between 0 and 100"}), 404

    try:
        updated = db.update_student(
            student_id,
            name=name.strip() if isinstance(name, str) else None,
            course=course.strip() if isinstance(course, str) else None,
            mark=mark,
        )
        if updated is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update student: {str(e)}"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        deleted = db.delete_student(student_id)
        if deleted is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(deleted), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete student: {str(e)}"}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [s.get("mark") for s in students if isinstance(s.get("mark"), int)]

        if len(marks) == 0:
            stats = {"count": 0, "average": None, "min": None, "max": None}
        else:
            stats = {
                "count": len(marks),
                "average": sum(marks) / len(marks),
                "min": min(marks),
                "max": max(marks),
            }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to compute stats: {str(e)}"}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
