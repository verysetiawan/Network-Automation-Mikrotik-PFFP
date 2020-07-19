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
    ip_gate = data["ip_gateway"]

    # Cetak ip Mikrotik
    print (f"IP Address Mikrotik adalah : {ip_mik}")
    print (f"IP Gateway Router Klien Mikrotik adalah : {ip_gate[:13]}")
    print (f"host id nya adalah: {ip_mik[12:]}")

    #Menyimpan informasi ip ke file ip_address.txt
    file_write = open ("template/ip_address.txt","a")
    file_write.write (ip_mik)
    file_write.write ("\n")
    file_write.close()

    #perintah untuk melakukan koneksi ssh client ke mikrotik
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_mik,username=username,password=password, allow_agent=False, look_for_keys=False)
    print (f"sukses login to {ip_mik}")
    
    #Perintah konfigurasi router klien
     
    config_list = [
        f"/system identity set name=R-{ip_mik}",
        "/tool romon set enabled=yes secrets=kangphery",
        "ip service disable telnet,ftp,www,api-ssl",
        f"/ip dns set servers={ip_gate[:13]}",
        f"/ip address add address=172.16.{ip_mik[12:]}.1/24 interface=ether2 network=172.16.{ip_mik[12:]}.0",
        "/ip firewall nat add action=masquerade chain=srcnat out-interface=ether1",
        f"/ip pool add name=LAN ranges=172.16.{ip_mik[12:]}.11-172.16.{ip_mik[12:]}.100",
        "/ip dhcp-server add address-pool=LAN disabled=no interface=ether2 lease-time=30m name=LAN",
        f"/ip dhcp-server network add address=172.16.{ip_mik[12:]}.0/24 dns-server={ip_gate[:13]} gateway=172.16.{ip_mik[12:]}.1",
        "/ip neighbor discovery-settings set discover-interface-list=none",
        "/system ntp client set enabled=yes primary-ntp=202.162.32.12",
        "/system clock set time-zone-name=Asia/Jakarta",
        "tool bandwidth-server set enabled=no",
        "user add name=noc password=noc123 disabled=no group=read",
        "user add name=supervisor password=supervisor123 disabled=no group=write"
        ]
    #Konfigurasi router klien
    for config in config_list:
        ssh_client.exec_command(config)
        print (config)
        time.sleep(0.2)
       
    
    return jsonify(data)

@app.route("/")
def indexku():
    file_open = open ("template/ip_address.txt","r")
    baca_file = file_open.readlines()
    baca_file1 = set(baca_file)

    return render_template ("index.html", var=baca_file1)  



if __name__ == "__main__":
    app.run (host='192.168.122.1', debug=True, port=5005)