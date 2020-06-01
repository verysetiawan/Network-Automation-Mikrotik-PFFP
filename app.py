from flask import Flask, request, jsonify, render_template


app = Flask(__name__,template_folder='template')

@app.route("/conf", methods=["POST"])
def config():
    #menangkap ip mikrotik client
    data = request.get_json()
    ip_mik = data["ip_router"]

    # Cetak ip Mikrotik
    print (f"IP Address Mikrotik adalah : {ip_mik}")

    #Menyimpan informasi ip ke file ip_address.txt
    file_write = open ("template/ip_address.txt","a")
    file_write.write (ip_mik)
    file_write.write ("\n")
    file_write.close()

    return jsonify(data)

@app.route("/")
def indexku():
    file_open = open ("template/ip_address.txt","r")
    baca_file = file_open.readlines()

    return render_template ("index.html", var=baca_file)  



if __name__ == "__main__":
    app.run (host='192.168.122.1', debug=True, port=5005)