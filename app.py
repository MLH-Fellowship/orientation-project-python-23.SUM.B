"""
   Flask Application
"""
from dataclasses import fields
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from dataclasses import fields


app = Flask(__name__)

data = {
    "experience": [
        Experience(
            "Software Developer",
            "A Cool Company",
            "October 2022",
            "Present",
            "Writing Python Code",
            "example-logo.png",
        )
    ],
    "education": [
        Education(
            "Computer Science",
            "University of Tech",
            "September 2019",
            "July 2022",
            "80%",
            "example-logo.png",
        )
    ],
    "skill": [Skill("Python", "1-2 Years", "example-logo.png")],
}


@app.route("/test")
def hello_world():
    """
    Returns a JSON test message
    """
    return jsonify({"message": "Hello, World!"})


@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handle experience requests
    """
    if request.method == "GET":
        return jsonify(data["experience"])

    if request.method == "POST":
        return add_experience()

    return jsonify({})


@app.route("/resume/education", methods=["GET", "POST", "PUT"])
def education():
    """
    Handles education requests
    """
    if request.method == "GET":
        return jsonify({})

    if request.method == "POST":
        return jsonify({})

    if request.method == "PUT":
        return edit_education()

    return jsonify({})


@app.route("/resume/education/<int:index>", methods=["GET"])
def get_education(index):
    """
    Handle get request for a single experience
    """
    edu = data["education"][index]
    return jsonify(edu)


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    """
    Handles skill requests
    """
    if request.method == "GET":
        return jsonify(data["skill"])

    if request.method == "POST":
        return add_skill()

    return jsonify({})


def add_skill():
    """
    Add a skill using POST method
    """
    req = request.get_json()

    required_fields = [field.name for field in fields(Skill)]

    missing_fields = [field for field in required_fields if field not in req]

    if missing_fields:
        error_message = "Missing required field(s): " + ", ".join(missing_fields)
        return jsonify({"error": error_message}), 400

    new_skill = Skill(req["name"], req["proficiency"], req["logo"])
    data["skill"].append(new_skill)

    return jsonify({"id": data["skill"].index(new_skill)})


def add_experience():
    """
    Add an experience using POST method
    """
    req = request.get_json()

    required_fields = [field.name for field in fields(Experience)]

    missing_fields = [field for field in required_fields if field not in req]

    if missing_fields:
        error_message = "Missing required field(s): " + ", ".join(missing_fields)
        return jsonify({"error": error_message}), 400

    new_experience = Experience(
        req["title"],
        req["company"],
        req["start_date"],
        req["end_date"],
        req["description"],
        req["logo"],
    )
    data["experience"].append(new_experience)

    return jsonify({"id": data["experience"].index(new_experience)})


def edit_education():
    """
    Edit an education using PUT method.
    """
    req = request.get_json()
    required_fields = [field.name for field in fields(Education)]
    if req is None or any(field not in req for field in required_fields):
        return jsonify({"error": "Invalid request data"})
    index = int(request.args.get("index", -1))
    if 0 <= index < len(data["education"]):
        data["education"].pop(index)
        data["education"].insert(
            index,
            {
                "course": req["course"],
                "school": req["school"],
                "start_date": req["start_date"],
                "end_date": req["end_date"],
                "grade": req["grade"],
                "logo": req["logo"],
            },
        )
        return jsonify(data["education"][index])
    return jsonify({"error": "Couldn't find the specified education"})
