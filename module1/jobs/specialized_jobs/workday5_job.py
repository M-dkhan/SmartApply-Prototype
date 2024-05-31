from .base_job import BaseJob


class Workday5Job(BaseJob):
    def __init__(self, title, url, role_type, description, location, due_date, requisitionId):
        super().__init__(title, url, role_type,  description, location, due_date)
        self.requisitionId = requisitionId


    def display(self):
        base_info = super().display()
        return f"{base_info} with serial number =  {self.requisitionId}"
