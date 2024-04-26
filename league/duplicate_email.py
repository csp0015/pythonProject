class DuplicateEmail(Exception):
    def __init__(self, email):
        super().__init__(f"Duplicate Email: {email}")
        self.email = email