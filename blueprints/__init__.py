# To make it a python package

from .views import views
from .encrypt import encrypt
from .decrypt import decrypt
from .download import download

_=views,encrypt,decrypt,download


if __name__ =="__main__":
    print("Please run the main.py file.")