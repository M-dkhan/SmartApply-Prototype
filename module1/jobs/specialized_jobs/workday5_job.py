from module1.jobs.base_job import BaseJob


class Workday5Job(BaseJob):

    def __init__(self, title, description, location, due_date, serial_number):
        super().__init__(title, description, location, due_date)
        self.serial_number = serial_number


    def display(self):
        base_info = super().display()
        print(f"{base_info} with serial number =  {self.serial_number}")
