'''
Flask Application
'''
from dataclasses import fields
from flask import Flask, jsonify, request
from models import Experience, Education, Skill, Contact


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
    ],

    "contact": [
        Contact("John Doe",
                "+123456789",
                "johndoe@mail.com")
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


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
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


@app.route('/resume/contact', methods=['GET', 'POST'])
def contact():
    '''
    Handles Contact requests
    '''
    if request.method == 'GET':
        return jsonify(data)

    if request.method == 'POST':
        api_data = request.get_json()

        if api_data is not None:
            name = api_data.get('name')
            phone = api_data.get('phone')
            email = api_data.get('email')

            # Ensure phone number starts with +
            if not phone.startswith('+'):
                phone = '+' + phone

            _contact = Contact(name, phone, email)
            data['contact'].append(_contact)
    return jsonify(data)


@app.route('/resume/contact', methods=['PUT'])
def update_contact():
    '''
    Update a contact with the given ID
    '''
    api_data = request.get_json()
    contacts = data['contact']

    if 'old_name' not in api_data:
        return jsonify({'error': 'Old Name is required'}), 400

    old_name = api_data.get('old_name')
    contact_index = None

    for index, contact in enumerate(contacts): # pylint: disable=W0621
        if contact.name == old_name:
            contact_index = index
            break

    if contact_index is not None:
        updated_contact = contacts[contact_index]
        updated_contact.name = api_data.get('name')
        updated_contact.email = api_data.get('email')

        if not api_data.get('phone').startswith('+'):
            updated_contact.phone = '+' + api_data.get('phone')


        return jsonify({'message': 'Contact updated successfully',
                        'Updated contact': updated_contact}), 200
    return jsonify({'error': 'Contact not found'}), 400
