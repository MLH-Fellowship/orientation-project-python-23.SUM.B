"""
   Flask Application
"""
from dataclasses import fields
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

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

@app.route('/resume/experience/<int:index>', methods = ['GET'])
def get_experience(index):
    """
    Handle get request for a single experience
    """
    total_length = len(data["experience"])
    if 0 <= index < total_length:
        return jsonify(data["experience"][index])
    return jsonify(
        "Error: index input can only be 0 to " + str(total_length) + "inclusively"
    )


@app.route("/resume/education", methods=["GET", "POST", "PUT"])
def education():
    """
    Handles education requests
    """
    if request.method == 'GET':
        return jsonify(data['education'])
    if request.method == "POST":
        return jsonify({})
    if request.method == "PUT":
        return edit_education()
    return jsonify({})




@app.route("/resume/skill/<index>", methods=["GET", "POST"])
def skill(index=None):
    """
    Handles Skill requests
    """
    if request.method == "GET":
        if index is not None:
            try:
                return jsonify(data["skill"][int(index)])
            except IndexError:
                return jsonify({'error': f'No skill with index {index} was found'})

        return jsonify(data["skill"])

    if request.method == "POST":
        return add_skill()
    if request.method == 'PUT':
        return edit_skill()
    return jsonify({})


def add_skill():
    """
    Add a new skill
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
    Add a new experience
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


def edit_skill():
    """
    Edit an existing skill.
    """
    req = request.get_json()
    required_fields = [field.name for field in fields(Skill)]
    if req is None or any(field not in req for field in required_fields):
        return jsonify({"error": "Invalid request data"})
    index = int(request.args.get("index", -1))
    if 0 <= index < len(data["skill"]):
        data["skill"].pop(index)
        data["skill"].insert(
            index,
            {
                "name": req["name"],
                "proficiency": req["proficiency"],
                "logo": req["logo"],
            },
        )
        return jsonify(data["skill"][index])
    return jsonify({"error": "Couldn't find the specified skill"})
