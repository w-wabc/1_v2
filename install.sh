curl ifconfig.me>>/etc/v2ray/ip.txt
mkdir /etc/json_test
cp auto_json.py /etc/json_test/auto_json.py
cp install.sh /etc/json_test/install.sh
python3 /etc/json_test/auto_json.py
systemctl start v2ray
systemctl restart v2ray
rm /etc/v2ray/ip.txt
chmod +x set.sh
cp ./set.sh /root/set.sh
