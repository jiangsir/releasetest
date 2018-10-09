#!/usr/bin/python3
import os
import fnmatch
import time
import subprocess
import datetime
import sys
from bs4 import BeautifulSoup

appname = "ZeroJudge"
webappname = "ROOT"
# appname = "ROOT" # tomcat 根目錄
dbname = appname.lower()
gitrepo = "ssh://git@git.nknush.kh.edu.tw/home/git/repository/" + appname + ".git"
#gitrepo = "https://github.com/githubaccount/" + appname + ".git"


def printFile(path):
    print('--------------------------------------------------------')
    f = open(path, 'r')
    lines = f.read()
    print(lines)
    print('--------------------------------------------------------')
    f.close()


def run(cmd):
    print("run> " + cmd)
    outputs = subprocess.check_output(cmd.split()).decode(
        'utf-8').rstrip().split('\n')
    for output in outputs:
        print("output=" + output)
    return outputs


def os_exec(cmd):
    print('cmd=' + cmd)
    os.system(cmd)


def importSQL(dbname):
    print("sqlfile 列表：")
    sqllist = []
    for sqlfile in os.listdir(apptmpdir):
        if fnmatch.fnmatch(sqlfile, '*.sql'):
            sqllist.append(sqlfile)

    for sqlfile in sqllist:
        print(str(sqllist.index(sqlfile,)) + ". " + sqlfile)
    print(str(len(sqllist)) + ". exit")

    index = input("請選擇要匯入的資料庫檔案 *.sql？ ")
    if index == str(len(sqllist)):
        return False

    # dbname = input("準備匯入 " + sqllist[int(index)] + ", 請輸入資料庫名稱：")
    # cmd = 'cat ' + apptmpdir + '/' + sqlfile + ' | mysql -u root -p'
    # cmd = 'mysql -u root -p ' + dbname + ' < ' + apptmpdir + '/' + sqlfile
    # print(cmd)
    # os.system(cmd)

    #cmd = "mysql -uroot -p " + dbname + " < " + apptmpdir + "/" + sqlfile
    print("匯入資料表到此資料庫: ")
    os_exec("mysql -uroot -p " + dbname + " < " + apptmpdir + "/" + sqlfile)

    return True


##### MAIN #############
run("sudo apt-get install ant")
for file in os.listdir('/etc/init.d/'):
    if fnmatch.fnmatch(file, 'tomcat*'):
        tomcatN = file

apptmpdir = appname + "_" + datetime.datetime.now().strftime('%Y%m%d')


run('rm -rf ' + apptmpdir)
run("git clone " + gitrepo + " " + apptmpdir)

# 列出版本號
#cmd = 'git --git-dir=' + apptmpdir + '/.git --work-tree=' + apptmpdir + ' tag '
#print("cmd=" + cmd)
# tags = subprocess.check_output(cmd.split()).decode(
#    'utf-8').rstrip().split('\n')

choose = input("請問要取出 1.tag 或者 2. branch：(1, 2) ")
if choose == "1":
    tags = run('git --git-dir=' + apptmpdir +
               '/.git --work-tree=' + apptmpdir + ' tag ')
    for index, tag in enumerate(tags):
        print(str(index) + ". tag=" + tag)
    tagindex = input("請問要取出哪一個 tag 版本？ ")
    run('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
        apptmpdir + ' checkout ' + tags[int(tagindex)])
    open(apptmpdir + '/WebContent/META-INF/Version.txt',
         mode='w', encoding='utf-8').write(tags[int(tagindex)])
elif choose == "2":
    # cmd = 'git --git-dir=' + apptmpdir + \
    #    '/.git --work-tree=' + apptmpdir + ' branch -a'
    #print("cmd=" + cmd)
    # branchs = subprocess.check_output(
    #    cmd.split()).decode('utf-8').rstrip().split('\n')
    branchs = run('git --git-dir=' + apptmpdir +
                  '/.git --work-tree=' + apptmpdir + ' branch -a')
    for index, branch in enumerate(branchs):
        print(str(index) + ". " + branch)
    bindex = input("請問要取出哪一個 branch？ ")
    branchname = branchs[int(bindex)].split(
        '/')[len(branchs[int(bindex)].split('/')) - 1]
    run('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
        apptmpdir + ' checkout ' + branchname)

    cmd = 'git --git-dir=' + apptmpdir + \
        '/.git --work-tree=' + apptmpdir + ' show-branch -g'
    message = subprocess.check_output(cmd.split()).decode('utf-8')
    print('message= ' + message)
    #message = run('git --git-dir=' + apptmpdir + '/.git --work-tree=' + apptmpdir + ' show-branch -g')
    open(apptmpdir + '/WebContent/META-INF/Version.txt',
         mode='w', encoding='utf-8').write(message)
else:
    sys.exit()

# 清除所有的 BOM
for root, dirs, files in os.walk(apptmpdir + "/src/"):
    for file in files:
        if file.endswith(".java"):
            # print(os.path.join(root, file))
            s = open(os.path.join(root, file), mode='r',
                     encoding='utf-8-sig').read()
            open(os.path.join(root, file), mode='w', encoding='utf-8').write(s)


print("開始打包")
os_exec('ant -f ' + apptmpdir + '/build.xml -Dappname=' +
        webappname + ' -DTOMCAT_HOME=/usr/share/' + tomcatN + '/')
print("開始發布")
os_exec('/etc/init.d/' + tomcatN + ' restart')
os_exec('rm -rf /var/lib/' + tomcatN + '/webapps/' + webappname + '/')
os_exec('cp ' + apptmpdir + '/' + webappname + '.war /var/lib/' +
        tomcatN + '/webapps/')
print("111111111")
#os_exec('python3 /var/lib/' + tomcatN + '/webapps/' + appname + '/Setup.py')
contextpath = '/var/lib/' + tomcatN + '/webapps/' + webappname + '/META-INF/context.xml'
print("Waiting", end="")
while not os.path.isfile(contextpath):
    print(".", end="")
    time.sleep(3)
print()

print("開始升級資料庫.......")
dbpass = input("輸入資料庫 root 密碼：")
print("建立一個新資料庫(" + dbname + "): ")
os_exec("mysql -u root -p'" + dbpass +
        "' -e \"CREATE DATABASE " + dbname + ";\"")
# importSQL(dbname)

print("匯入  完整資料表到資料庫(" + dbname + "): ")
schemasql = ""
for filename in os.listdir(apptmpdir):
    if fnmatch.fnmatch(filename, 'Schema*.sql'):
        schemasql = filename
if schemasql != "":
    os_exec("mysql -uroot -p'" + dbpass + "' " +
            dbname + " < " + apptmpdir + "/" + schemasql)

schemaupdatesql = ""
for filename in os.listdir(apptmpdir):
    if fnmatch.fnmatch(filename, 'SchemaUpdate*.sql'):
        schemaupdatesql = filename
if schemaupdatesql != "":
    print("資料庫(" + dbname + ") 進行資料表升級: ")
    os_exec("mysql -uroot -p'" + dbpass + "' " + dbname + " < " + apptmpdir + "/" + schemaupdatesql)

print("開始設定資料庫.......")
context = open(contextpath, 'r+', encoding='UTF-8')
contextsoup = BeautifulSoup(context, 'xml')
resource = contextsoup.find('Resource')
#username = input("請輸入資料庫帳號(" + resource['username'] + ")：")
# if username != "":
#    resource['username'] = username
#password = input("請輸入資料庫密碼(" + resource['password'] + ")：")
# if password != "":
#    resource['password'] = password

resource['username'] = "root"
resource['password'] = dbpass

os_exec('true > ' + contextpath)
context.seek(0, 0)
context.write(str(contextsoup))
context.close()

os_exec('/etc/init.d/' + tomcatN + ' restart')
