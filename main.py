import requests, json, os

userjson = open("config/user.json").read()
username = json.loads(userjson)['user'][0]
userpwd = json.loads(userjson)['user'][1]
site = json.loads(open("config/global.json").read())['site']

while True:
    try:
        bash = input(">>> ")
        lbash = bash.split()
        if bash == "exit":
            print("Exit icmt...")
            break
        elif "upload" == lbash[0]:
            print(f"[Info]: Upload file {lbash[1]}")
            filename = lbash[1]
            size = 1024*1024

            def mk_SubFile(srcName, sub, buf):
                filename = srcName + "_" + str(sub)
                with open(filename, 'wb') as fout:
                    fout.write(buf)
                    return sub + 1


            def split_By_size(filename, size):
                with open(filename, 'rb') as fin:
                    buf = fin.read(size)
                    sub = 1
                    i = 1
                    while len(buf) > 0:
                        sub = mk_SubFile(filename, sub, buf)
                        buf = fin.read(size)
                        i+=1
                return i
            ai = split_By_size(filename, size)
            for i in range(1, ai):
                f = open(lbash[1]+"_"+str(i), 'rb')
                file = {'file': f}
                requests.post(site + "/api/upload.php", data={"username": username, "password": userpwd, 'file_this': i}, files=file,
                                    timeout=1000)
                f.close()
            print(requests.post(site + "/api/mergefile.php", data={"username": username, "password": userpwd, 'totel': ai-1, "filename": filename},
                                timeout=1000).text)

            for i in range(1, ai):
                os.remove(lbash[1] + "_" + str(i))
        elif "new" == lbash[0]:
            print(f"[Info]: Create new repository {lbash[1]}")
            print(requests.post(site + "/api/newrepo.php", data={"username": username, "password": userpwd,
                                                                 "reponame": lbash[1]}, timeout=1000).text)
        elif "clone" == lbash[0]:
            print(f"[Info]: Clone repository {lbash[1]}")
            files = requests.post(site + "/api/lsrepo.php",
                                  data={"username": lbash[1].split('/')[0], "reponame": lbash[1].split("/")[1]}).text.split(
                "\n")

            for filename in files:
                if not filename:
                    continue
                if filename.find("/") != -1:
                    filedir = '/'.join(filename.split("/")[0:-1])
                    if not os.path.isdir(lbash[1].split('/')[1] + "/" + filedir):
                        os.mkdir(lbash[1].split('/')[1] + "/" + filedir)
                res = requests.post(site + "/api/clone.php",
                                    data={"username": lbash[1].split('/')[0], "reponame": lbash[1].split("/")[1], 'filename': filename, 'repo': 'true'},
                                    timeout=5000)
                if not os.path.isdir(lbash[1].split('/')[1]):
                    os.mkdir(lbash[1].split('/')[1])
                if res.text:
                    with open(lbash[1].split('/')[1] + "/" + filename, 'wb') as f:
                        f.write(res.content)
                else:
                    print(f"Not has {lbash[1]} in {site} icmt server.")

        elif "pull" == lbash[0]:
            print(f"[Info]: Pull request at file {lbash[1]}")
            res = requests.post(site + "/api/clone.php",
                                data={"username": lbash[1].split('/')[0], "filename": lbash[1].split("/")[1], 'repo': 'false'}, timeout=5000)
            if res.text:
                with open(lbash[1].split('/')[1], 'wb') as f:
                    f.write(res.content)
            else:
                print(f"Not has {lbash[1]} in {site} icmt server.")

        elif "merge" == lbash[0]:
            print(f"[Info]: Merge request to repository {lbash[1]}")
            k = 0
            for filepath,dirnames,filenames in os.walk(lbash[1]):
                for filename in filenames:
                    file = {'file': open(os.path.join(filepath, filename), 'rb')}
                    print(requests.post(site + "/api/upload.php",
                                        data={"username": username, "password": userpwd, 'reponame': lbash[1], 'repo': 'true', 'totel': str(k), 'filepath': lbash[1].join(filepath.split(lbash[1])[1:]).lstrip("\\").replace("\\","/")},
                                        files=file,
                                        timeout=1000).text, end='')
                    k += 1
        elif "del" == lbash[0]:
            print(f"[Info]: Delete file {lbash[1]}")
            print(requests.post(site + "/api/delfile.php", data={"username": username, "password": userpwd, "filename": lbash[1]}).text)
        elif "delrepo" == lbash[0]:
            print(f"[Info]: Delete repository {lbash[1]}")
            print(requests.post(site + "/api/delrepo.php",
                                data={"username": username, "password": userpwd, "reponame": lbash[1]}).text)
        elif "ls" == lbash[0]:
            print(f"[Info]: List index at repository {lbash[1]}")
            print(requests.post(site + "/api/lsrepo.php",
                                data={"username": lbash[1].split("/")[0], "reponame": lbash[1].split("/")[1]}).text)
    except Exception as e:
        print("Error:", e)
        continue
