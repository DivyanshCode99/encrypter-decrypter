from flask import Blueprint ,render_template, send_file ,flash ,redirect
import os
import shutil

download=Blueprint("download",__name__)
 
UPLOAD_FOLDER = '/tmp/Enc Dec/uploads'




@download.route("/download/<_id>/<filename>")
def downloader(_id,filename):
    if _id == "OFFLINEVERSION":
        file_path=os.path.join("static","EXE","Encrypter&Decrypter.exe")
        return send_file(file_path, as_attachment=True)
    file_path=os.path.join(UPLOAD_FOLDER,_id,filename)
    return send_file(file_path, as_attachment=True)


@download.route("/clean-up/<_id>/<mode>")
def clean_up(_id,mode):
    shutil.rmtree(os.path.join(UPLOAD_FOLDER,_id))
    return redirect(f"/file_{mode}")




if __name__ =="__main__":
    print("Please run the main.py file.")