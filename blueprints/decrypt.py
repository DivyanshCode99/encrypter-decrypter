from flask import Blueprint , render_template,send_file,redirect,url_for,flash,request
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
import bcrypt
import os
from cryptography.fernet import Fernet,InvalidToken

decrypt=Blueprint("decrypt",__name__)

UPLOAD_FOLDER = '/tmp/Enc Dec/uploads'



@decrypt.route("/text_decrypter",methods=['GET', 'POST'])
def text_decrypter():
    if request.method == 'POST':
        password= request.form.get("password").encode()
        text_to_decrypt=request.form.get("text").encode()

        try:
            salt = hashlib.sha256(password).digest()[:16]
            kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            decrypted_text = Fernet(key).decrypt(text_to_decrypt).decode()
            return render_template("text_decrypter.html",decrypted_text=decrypted_text,text_to_decrypt=text_to_decrypt.decode(),pwd=password.decode())
        except InvalidToken:
            flash("The password is incorrect. ","error")
            decrypted_text=''
            return render_template("text_decrypter.html",decrypted_text=decrypted_text,text_to_decrypt=text_to_decrypt.decode(),pwd=password.decode())
              
    return render_template("text_decrypter.html",decrypted_text='')





@decrypt.route("/file_decrypter")
def file_decrypter():           
    return render_template("file_decrypter.html")

@decrypt.route("/decrypt_file" , methods=['POST','GET'])
def decrypt_file():
    if request.method=='GET':
        return redirect("/")
    file = request.files['file_to_decrypt']
    pwd=request.form.get("password").encode()
    while True:
        _id=bcrypt.gensalt().decode()
        if "/" not in _id:break
    os.makedirs(os.path.join(UPLOAD_FOLDER,_id))
    file.filename = file.filename.replace("&", "_")
    filepath = os.path.join(UPLOAD_FOLDER,_id, file.filename)
    file.save(filepath)
    decrypted_filename="Dec_"+file.filename.removesuffix(".enc")
    decrypted_filepath=os.path.join(UPLOAD_FOLDER,_id, decrypted_filename)
    with open(filepath, 'rb') as f:
        data = f.read()
        try:
            salt = hashlib.sha256(pwd).digest()[:16]
            kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt, 
            iterations=100000,
            backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(pwd))
            decrypted_data = Fernet(key).decrypt(data)
        except InvalidToken:
            flash("The password is Invalid !","error")
            return redirect(f"/clean-up/{_id}/decrypter")

    with open(decrypted_filepath,"wb") as f:
        f.write(decrypted_data)
    #return redirect(f"download/{_id}/{file.filename+".enc"}")
    flash("The file has been decrypted successfully.","success")
    return redirect(f"/file_decrypter?result=true&id={_id}&filename={decrypted_filename}")
if __name__ =="__main__":
    print("Please run the main.py file.")