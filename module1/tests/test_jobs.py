import pytest
from module1.jobs.specialized_jobs.workday5_job import Workday5Job


def test_workday5_job_creation():
    
    job = Workday5Job(title="Test Title",description="This is a testing description",location="Testing location",due_date="April 9, 2024", serial_number="1254789")
    
    # Assertions to check if the job is correctly initialized 
    assert job.title == 'Test Title'
    assert job.descrption == 'This is a testing description'
    assert job.location == 'Testing location'
    assert job.due_date == 'April 9, 2024'
    assert job.serial_number == '1254789'


def test_workday_job_display():
    job = Workday5Job(title="Test Title",description="This is a testing description",location="Testing location",due_date="April 9, 2024", serial_number="1254789")

    display_text = job.display()
    assert display_text == "Test Title at Testing location is due by April 9, 2024 with serial number 1254789"