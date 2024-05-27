from module1.jobs.base_job import BaseJob


class AmazonJob(BaseJob):
    
    def __init__(self, title, url, role_type, description, location, job_id,due_date=None, ):
        super().__init__(title, url, role_type,  description, location, due_date)
        self.title = title
        self.job_id = job_id
        self.role_type = role_type
        self.location = location
        self.description = description


    def display(self):
        base_info = super().display()
        return f"{base_info}"
