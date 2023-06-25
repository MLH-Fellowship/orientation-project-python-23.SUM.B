'''
Flask Application
'''
from dataclasses import fields
from flask import Flask, jsonify, request
from models import Experience, Education, Skill


app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST', 'DELETE'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify(data["experience"])

    if request.method == 'POST':
        return jsonify({})

    if request.method == "DELETE":
        experience_index = int(request.json.get("id"))
        if 0 <= experience_index < len(data["experience"]):
            deleted_experience = data["experience"].pop(experience_index)
            return jsonify(
                {
                    "message": "experience deleted successfully",
                    "deleted_experience": deleted_experience.__dict__,
                }
            )

        return jsonify({"error": "Invalid experience index"})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST', 'DELETE'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        return jsonify(data["skill"])

    if request.method == 'POST':
        return add_skill()

    if request.method == "DELETE":
        skill_index = int(request.json.get("id"))
        if 0 <= skill_index < len(data["skill"]):
            deleted_skill = data["skill"].pop(skill_index)
            return jsonify(
                {
                    "message": "Skill deleted successfully",
                    "deleted_skill": deleted_skill.__dict__,
                }
            )

        return jsonify({"error": "Invalid skill index"})

    return jsonify({})


def add_skill():
    '''
     Add a skill using POST method
    '''
    req = request.get_json()

    required_fields = [field.name for field in fields(Skill)]

    missing_fields = [field for field in required_fields if field not in req]

    if missing_fields:
        error_message = "Missing required field(s): " + ", ".join(missing_fields)
        return jsonify({"error": error_message}), 400

    new_skill = Skill(req["name"], req["proficiency"], req["logo"])
    data["skill"].append(new_skill)

    return jsonify({"id": data["skill"].index(new_skill)})
