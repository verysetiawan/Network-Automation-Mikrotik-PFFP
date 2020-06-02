from flask import Flask, request, jsonify, render_template
import paramiko
import time


app = Flask(__name__,template_folder='template')

@app.route("/conf", methods=["POST"])
def config():
    #menangkap ip mikrotik client
    data = request.get_json()
    ip_mik = data["ip_router"]
    username = "admin"
    password = ""
    

    # Cetak ip Mikrotik
    print (f"IP Address Mikrotik adalah : {ip_mik}")

    #Menyimpan informasi ip ke file ip_address.txt
    file_write = open ("template/ip_address.txt","a")
    file_write.write (ip_mik)
    file_write.write ("\n")
    file_write.close()

    #perintah untuk melakukan koneksi ssh client ke mikrotik
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_mik,username=username,password=password)
    print (f"sukses login to {ip_mik}")
    ssh_client.exec_command(f"/system identity set name=R-{ip_mik}")
    return jsonify(data)

@app.route("/")
def indexku():
    file_open = open ("template/ip_address.txt","r")
    baca_file = file_open.readlines()

    return render_template ("index.html", var=baca_file)  



if __name__ == "__main__":
    app.run (host='192.168.122.1', debug=True, port=5005)