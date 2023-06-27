'''
Tests in Pytest
'''
from app import app


def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


def test_education():
    '''
    Add a new education and then get all educations. 
    
    Check that it returns the new education in that list
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/education',
                                     json=example_education).json['id']

    response = app.test_client().get('/resume/education')
    assert response.json[item_id] == example_education


def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill

def test_contact():
    '''
    Add a new contact and then get all contacts. 
    
    Check that it returns the new contact in that list
    '''
    example_contact = {
        "name": "John Doe",
        "phone": "1234567890",
        "email": "johndoe@gmail.com"}

    post_response = app.test_client().post('/resume/contact', json=example_contact)
    assert post_response.status_code == 200

    get_response = app.test_client().get('/resume/contact')
    assert get_response.status_code == 200
    # Check that the response is not empty
    contact = get_response.json["contact"]
    assert contact != {}
    assert len(contact) > 0

def test_contact_update():
    '''
    Add a new contact and then update it. 
    Check that the appropriate fields have been updated
    '''
    example_contact = {
        "name": "John Doe",
        "phone": "1234567890",
        "email": "johndoe@gmail.com"}
    update_contact = {
        "old_name": "John Doe",
        "name": "Jane Doe",
        "phone": "0987654321",
        "email": "johndoer@yahoo.com"}

    post_response = app.test_client().post('/resume/contact', json=example_contact)
    assert post_response.status_code == 200


    put_response = app.test_client().put('/resume/contact', json=update_contact)
    assert put_response.status_code == 200

    get_response = app.test_client().get('/resume/contact')


    # Check that the response is the same as the updated contact
    contact_index = None
    contact_index = [index for index, contact in enumerate(get_response.json["contact"])
                     if contact["name"] == update_contact["name"]][0]

    del update_contact["old_name"]
    update_contact["phone"] = "+" + update_contact["phone"]

    assert get_response.json["contact"][contact_index] == update_contact
