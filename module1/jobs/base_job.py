class BaseJob:
    def __init__(self, title, description, location, due_date):
        self.title = title
        self.descrption = description
        self.location = location
        self.due_date = due_date

    def display(self):
        print(f"{self.title} at {self.location} is due by {self.due_date}")
        return f"{self.title} at {self.location} is due by {self.due_date}"
