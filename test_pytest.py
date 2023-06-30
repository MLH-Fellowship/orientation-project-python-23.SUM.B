"""
Tests in Pytest
"""
from app import app


def test_client():
    """
    Makes a request and checks the message received is the same
    """
    response = app.test_client().get("/test")
    assert response.status_code == 200
    assert response.json["message"] == "Hello, World!"


def test_experience():
    """
    Add a new experience and then get all experiences.
    Check that it returns the new experience in that list
    """
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png",
    }

    item_id = (
        app.test_client().post("/resume/experience", json=example_experience).json["id"]
    )
    response = app.test_client().get("/resume/experience")
    assert response.json[item_id] == example_experience


def test_education():
    """
    Add a new education and then get all educations.
    Check that it returns the new education in that list
    """
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png",
    }
    item_id = (
        app.test_client().post("/resume/education", json=example_education).json["id"]
    )

    response = app.test_client().get("/resume/education")
    assert response.json[item_id] == example_education


def test_skill():
    """
    Add a new skill and then get all skills.
    Check that it returns the new skill in that list
    """
    example_skill = {
        "name": "Javascript",
        "proficiency": "1-2 years",
        "logo": "example-logo.png",
    }

    item_id = app.test_client().post("/resume/skill/", json=example_skill).json["id"]

    response = app.test_client().get("/resume/skill/")
    assert response.json[item_id] == example_skill


def test_delete_skill():
    """
    Delete an existing skill by index position
    """
    # Add a skill for deletion
    example_skill = {
        "name": "Java",
        "proficiency": "3-5 years",
        "logo": "example-logo.png",
    }
    response = app.test_client().post("/resume/skill", json=example_skill)
    skill_id = response.json["id"]

    # Delete the skill
    delete_response = app.test_client().delete("/resume/skill", json={"id": skill_id})
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Skill deleted successfully"
    assert delete_response.json["deleted_skill"]["name"] == "Java"

    # Check if the deleted skill is no longer present
    get_response = app.test_client().get("/resume/skill")
    assert skill_id not in get_response.json


def test_delete_experience():
    """
    Delete an existing experience by index position
    """
    # Add a experience for deletion
    example_experience = {
        "title": "Software Developer",
        "company": "A Cool Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing Python Code",
        "logo": "example-logo.png",
    }
    response = app.test_client().post("/resume/experience", json=example_experience)
    experience_id = response.json["id"]

    # Delete the experience
    delete_response = app.test_client().delete(
        "/resume/experience", json={"id": experience_id}
    )
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "experience deleted successfully"
    assert delete_response.json["deleted_experience"]["title"] == "Software Developer"

    # Check if the deleted experience is no longer present
    get_response = app.test_client().get("/resume/experience")
    assert experience_id not in get_response.json


def test_skill_edit():
    """
    Update an existing skill and then get all skills.
    Check that it returns the updated skill in that list
    """
    # Add a new skill
    response = app.test_client().post(
        "/resume/skill",
        json={
            "name": "JavaScript",
            "proficiency": "2-4 years",
            "logo": "example-logo1.png",
        },
    )
    item_id = response.json["id"]

    # Update the skill
    app.test_client().put(
        f"/resume/skill?index={item_id}",
        json={"name": "Python", "proficiency": "1 year", "logo": "exam.png"},
    )

    # Get all skills
    response = app.test_client().get("/resume/skill")

    # Check if the updated skill exists in the list
    assert response.json[item_id] == {
        "name": "Python",
        "proficiency": "1 year",
        "logo": "exam.png",
    }
    print(item_id)
