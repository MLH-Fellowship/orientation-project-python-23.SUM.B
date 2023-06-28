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

    Parameters:
    None

    Returns:
    - A JSON response containing a test message.

    """
    return jsonify({"message": "Hello, World!"})


@app.route("/resume/experience", methods=["GET", "POST"])
def experience():
    """
    Handle experience requests.

    Parameters:
    None

    Returns:
    - If the request method is GET, returns a JSON response containing the experience data.
    - If the request method is POST, calls the add_experience() function and returns the result.
    - If the request method is neither GET nor POST, returns an empty JSON response."""
    if request.method == "GET":
        return jsonify(data["experience"])

    if request.method == "POST":
        return add_experience()

    return jsonify({})


@app.route("/resume/education", methods=["GET", "POST", "PUT"])
def education():
    """
    Handle education requests.

    Parameters:
    None

    Returns:
    - If the request method is GET, returns an empty JSON response.
    - If the request method is POST, returns an empty JSON response.
    - If the request method is PUT, calls the edit_education() function and returns the result.
    - If the request method is neither GET, POST, nor PUT, returns an empty JSON response.
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
    Handle GET request for a single education entry.

    Parameters:
    - index (int): The index of the education entry to retrieve.

    Returns:
    - If the index is valid, returns a JSON response containing the requested education entry.
    - If the index is out of range or invalid, returns an empty JSON response.
    """
    edu = data["education"][index]
    return jsonify(edu)


@app.route("/resume/skill", methods=["GET", "POST"])
def skill():
    """
    Handle skill requests.

    Parameters:
    None

    Returns:
    - If the request method is GET, returns a JSON response containing the skill data.
    - If the request method is POST, calls the add_skill() function and returns the result.
    - If the request method is neither GET nor POST, returns an empty JSON response.
    """
    if request.method == "GET":
        return jsonify(data["skill"])

    if request.method == "POST":
        return add_skill()

    return jsonify({})


def add_skill():
    """
    Add a skill using the POST method.

    Parameters:
    None (reads request data from the request body)

    Returns:
    - If all required fields are provided in the request JSON data, adds the skill to the data store
      and returns a JSON response with the ID of the added skill.
    - If any required field is missing in the request JSON data,
    returns a JSON response with an error message
      indicating the missing fields and a 400 status code.
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
    Add a new experience using the POST method.

    Parameters:
    None (reads request data from the request body)

    Returns:
    - If all required fields are provided in the request JSON data,
      adds the experience to the data store
      and returns a JSON response with the ID of the added experience.
    - If any required field is missing in the request JSON data,
    returns a JSON response with an error message
      indicating the missing fields and a 400 status code.
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
    Edit an existing education using the PUT method.

    Parameters:
    None (reads request data from the request body)

    Returns:
    - If the request data is valid and the specified education index exists,
    edits the education entry in the data store
      and returns a JSON response with the updated education entry.
    - If the request data is invalid or the specified education index doesn't exist,
    returns a JSON response with an error message.
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
