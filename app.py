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
              "example-logo.png"),
        Skill("C",
              "3-4 Years",
              "example-logo.png"),
        Skill("Java",
              "2-3 Years",
              "example-logo.png"),
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

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


@app.route('/resume/skill/', methods=['GET', 'POST'])
@app.route('/resume/skill/<index>', methods=['GET', 'POST'])
def skill(index=None):
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        if index is not None:
            try:
                return jsonify(data['skill'][int(index)])
            except IndexError:
                return jsonify({'error': f'No skill with index {index} was found'})
        return jsonify(data["skill"])

    if request.method == 'POST':
        return add_skill()

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
