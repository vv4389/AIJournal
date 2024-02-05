import random
from PIL import Image


class User:
    def __init__(self, img):
        self.uid = random.randrange(start=100000000, stop=999999999)
        self.img = img

    def get_userid(self):
        return self.uid

    def __str__(self):
        return f'User: {self.uid}'


if __name__ == "__main__":
    img = Image.open("FamilyCamping-2021-GettyImages-948512452-2.webp")
    user = User(random.randrange(start=100000000, stop=999999999), img)
    print(user)
