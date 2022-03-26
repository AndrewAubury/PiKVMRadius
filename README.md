# PiKVMRadius



## Setup
Please ensure you update the below line to match your Radius server IP/Port, the secret is passed in from within the KVM config, see below. 

    r = radius.Radius(post_data["secret"], host='10.0.0.150', port=1812)

By default this server runs on port 6930 you can update this in the code if you wish for this to be active on another port.

You can then run the server via `python ./server.py` however you may wish to add this as a service or use some type of daemon to ensure the server does not go offline.

Update your firewall to allow all connections from your KVM IP/IP Range to access this new port. 

ssh on to your PiKVM via `ssh root@ip` once logged in run `rw` this will put the PiKVM in to Read/Write mode.

Pop open `/etc/kvmd/auth.yaml` in nano or vim
`vi /etc/kvmd/auth.yaml`

Replace the content of the file with below, again ensuring that the IP/Port is correct and the secret matches what your Radius server is expecting.

    internal:
        force_users: admin
    external:
        type: http
        url: http://10.0.0.69:6930/
        secret: PiKVM1 # KVM ID

Next run `ro` and `reboot now` this will reboot your PiKVM, once it comes back up try to login with your new Radius login!
