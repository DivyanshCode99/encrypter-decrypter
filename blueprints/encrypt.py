from flask import Blueprint , render_template,send_file,redirect,url_for,flash,request
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib 
from cryptography.fernet import Fernet,InvalidToken
import os
import bcrypt

encrypt=Blueprint("encrypt",__name__)

UPLOAD_FOLDER = '/tmp/Enc Dec/uploads'


@encrypt.route("/text_encrypter",methods=['GET', 'POST'])
def text_encrypter():
    if request.method == 'POST':
        password= request.form.get("password").encode()
        text_to_encrypt=request.form.get("text").encode()
     
        salt = hashlib.sha256(password).digest()[:16]
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        encrypted_text = Fernet(key).encrypt(text_to_encrypt).decode()

        return render_template("text_encrypter.html",encrypted_text=encrypted_text,text_to_encrypt=text_to_encrypt.decode(),pwd=password.decode())
           
    return render_template("text_encrypter.html",encrypted_text='')

@encrypt.route("/file_encrypter")
def file_encrypter():           
    return render_template("file_encrypter.html")

@encrypt.route("/encrypt_file" , methods=['POST','GET'])
def encrypt_file():
    if request.method=='GET':
        return redirect("/")
    file = request.files['file_to_encrypt']
    pwd=request.form.get("password").encode()
    while True:
        _id=bcrypt.gensalt().decode()
        if "/" not in _id:break
    os.makedirs(os.path.join(UPLOAD_FOLDER,_id))
    file.filename = file.filename.replace("&", "_")
    filename = os.path.join(UPLOAD_FOLDER,_id, file.filename)
    file.save(filename)
    with open(filename, 'rb') as f:
        data = f.read()
        salt = hashlib.sha256(pwd).digest()[:16]
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt, 
        iterations=100000,
        backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(pwd))
        encrypted_data = Fernet(key).encrypt(data)
    encrypted_filename=filename+".enc"
    with open(encrypted_filename,"wb") as f:
        f.write(encrypted_data)
    #return redirect(f"download/{_id}/{file.filename+".enc"}")
    flash("The file has been encrypted successfully.","success")
    file.filename+=".enc"
    return redirect(f"/file_encrypter?result=true&id={_id}&filename={file.filename}")
    
    
    




if __name__ =="__main__":
    print("Please run the main.py file.")