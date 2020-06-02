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
    ssh_client.connect(hostname=ip_mik,username=username,password=password, allow_agent=False, look_for_keys=False)
    print (f"sukses login to {ip_mik}")
    
    #Perintah konfigurasi router klien
    config_list = [
        f"/system identity set name=R-{ip_mik}",
        "/tool romon set enabled=yes secrets=kangphery",
        "ip service disable telnet,ftp,www,api-ssl",
        "/ip dns set servers=192.168.100.1",
        "/ip address add address=172.16.7.1/24 interface=ether2 network=172.16.7.0",
        "/ip firewall nat add action=masquerade chain=srcnat out-interface=ether1",
        "/ip pool add name=dhcp_pool0 ranges=172.16.7.11-172.16.7.100",
        "/ip dhcp-server add address-pool=dhcp_pool0 disabled=no interface=ether2 lease-time=30m name=LAN",
        "/ip dhcp-server network add address=172.16.7.0/24 dns-server=192.168.100.1 gateway=172.16.7.1",
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
        time.sleep(0.2)
        print (config)

    return jsonify(data)

@app.route("/")
def indexku():
    file_open = open ("template/ip_address.txt","r")
    baca_file = file_open.readlines()

    return render_template ("index.html", var=baca_file)  



if __name__ == "__main__":
    app.run (host='192.168.122.1', debug=True, port=5005)