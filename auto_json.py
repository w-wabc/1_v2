import uuid
import re
import os
import base64


# 生成vmess_url
def v_url():
    # 1.打开ip文件
    with open("/etc/v2ray/ip.txt", "r") as f:
        ip_txt = f.read()
        ip_txt = """\"%s\"""" % ip_txt
    f.close()
    # 2.设置一个生成vmess模板txt
    with open("/etc/v2ray/vmess_url.txt", "w") as f_1:
        f_1.write("""{
  "v": "2",
  "ps": "",
  "add": "",
  "port": "",
  "id": "",
  "aid": "64",
  "net": "tcp",
  "type": "none",
  "host": "",
  "path": "",
  "tls": ""
}""")
    f_1.close()
    # 3.设置一个list进行txt数据的反复写入
    vmess_list = list()
    f = open("/etc/v2ray/vmess_url.txt", "r")
    for line in f:
        vmess_list.append(line)
    f.close()
    # 4.从config中获取端口和uuid
    with open("/etc/v2ray/config.json", "r") as f:
        for temp in f:
            port = re.search(r""""port": (.*),""", temp)
            if port:
                break
        port = """\"%s\"""" % port.group(1)
        for temp in f:
            uuid = re.search(r""""id": (.*),""", temp)
            if uuid:
                break
        uuid = """%s""" % uuid.group(1)
    f.close()
    # 利用上述信息进行模板文件的配置
    with open("/etc/v2ray/vmess_url.txt", "w") as f:
        for line in vmess_list:
            if "add" in line:
                f.write("""  "add": %s,\n""" % ip_txt)
            elif "port" in line:
                f.write("""  "port": %s,\n""" % port)
            elif """\"id\"""" in line:
                f.write("""  "id": %s,\n""" % uuid)
            else:
                f.write(line)
    f.close()
    # 利用base64生成vmess链接
    with open("/etc/v2ray/vmess_url.txt", "r") as f:
        t = f.read()
    f.close()
    t = t.encode("utf-8")
    url = base64.b64encode(t)
    url = url.decode()
    url = "vmess://" + url
    return url


def menu():
    print("------------W.W的小脚本------------")
    print("运行完脚本后按4退出后链接才可用......")
    print("------------W.W的小脚本------------")
    print("1.一键设置v2ray")
    print("2.更改v2ray端口")
    print("3.更改v2rayuuid")
    print("4.退出脚本")
    print("----------------------------------")
    try:
        key = int(input("请输入您要使用的功能编号："))
    except Exception as ret:
        print("您的输入有误......")
        key = menu()
    if key == 1:
        set_port()
        set_uuid()
        url = v_url()
        print("设置成功！！！")
        print("vmess链接是：%s" % url)
    if key == 2:
        set_port()
        url = v_url()
        print("设置成功！！！")
        print("vmess链接是：%s" % url)
    if key == 3:
        set_uuid()
        url = v_url()
        print("设置成功！！！")
        print("vmess链接是：%s" % url)
    elif key == 4:
        exit()


def get_uuid():
    # 生成一个uuid并返回
    uuid_str = uuid.uuid4()
    return uuid_str


def get_port():
    # 用户自定义一个端口
    try:
        port = int(input("请输入您指定的连接端口:"))
        return port
    except Exception as ret:
        print("您的端口输入有误...")
        port = get_port()
        return port


def get_json_template():
    with open("/etc/v2ray/config_template.json", "w") as f:
        f.write("""{
      "inbounds": [
        {
          "port": 36666,
          "protocol": "vmess",
          "settings": {
            "clients": [
              {
                "id": "b831381d-6324-4d53-ad4f-8cda48b30811",
                "alterId": 64
              }
            ]
          }
        }
      ],
      "outbounds": [
        {
          "protocol": "freedom",
          "settings": {}
        }
      ]
    }"""
                )
        f.close()
    f = open("/etc/v2ray/config_template.json", 'r')
    with open("/etc/v2ray/config.json", "w") as f_n:
        for temp in f:
            f_n.write(temp)
    f_n.close()


def set_port():
    # 用户输入端口
    my_port = get_port()
    lines = list()
    flag = 0
    # 1.打开原有的模板写入列表中
    f = open("/etc/v2ray/config.json", 'r')
    for line in f:
        lines.append(line)
    f.close()
    # 2.新建根据规则更改json文件
    for temp in lines:
        if "port" in temp:
            lines[flag] = """          "port": %d,\n""" % my_port
            flag += 1
        flag += 1
    with open("/etc/v2ray/config.json", "w") as f_n:
        for temp in lines:
            f_n.write(temp)
    f_n.close()


def set_uuid():
    # 获取一个新的uuid
    my_uuid = get_uuid()
    lines = list()
    flag = 0
    print("new_uuid:%s" % my_uuid)
    # 1.打开原有的模板写入列表中
    f = open("/etc/v2ray/config.json", 'r')
    for line in f:
        lines.append(line)
    f.close()
    # 2.新建根据规则更改json文件
    for temp in lines:
        if "id" in temp:
            lines[flag] = """                "id": "%s",\n""" % my_uuid
            flag += 1
        flag += 1
    with open("/etc/v2ray/config.json", "w") as f_n:
        for temp in lines:
            f_n.write(temp)
    f_n.close()


def main():
    # 首先生成一个json模板放在指定路径下
    if not os.path.exists("/etc/v2ray/config_template.json"):
        get_json_template()
    while True:
        menu()


if __name__ == "__main__":
    main()
