class User:
    def __init__(self, user_name, email, contact_number):
        self.username = user_name
        self.email = email
        self.contact_number = contact_number

    def get_username(self):
        return self.username

    def __str__(self):
        return f'User: {self.username}\nEmail: {self.email}\nContact: {self.contact_number}'
if __name__ == "__main__":
    user = User("Viraj","vv4389@gmail.com","+1 5855536727")
    print(user)