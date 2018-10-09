import sys
import fnmatch
import os
import json
import time
import fire
import subprocess

basepath = os.path.dirname(os.path.realpath(__file__))


class ZeroJudgeSetup(object):
    ''' ZeroJudge Setup
    搭配參數如下：
    install: 直接安裝並進行必要設定
    '''

    def __init__(self, offset=1):
        self._offset = offset

    def _exec(self, cmd):
        print("cmd= " + cmd)
        os.system(cmd)

    def install(self, dbpass, warname=None, dbuser='root', githost='github.com', version="latestversion", clean=True, SSL=False):
        ''' 安裝/設定 ZeroJudge 系統 
        '''
        # appname = input("請輸入 git host 上的應用程式名稱: ")  # ex: ZeroJudge
        appname = "ZeroJudge"
        dbname = appname.lower()
        apptmpdir = os.path.join("/tmp", appname)
        self._exec('rm -rf ' + apptmpdir)
        self._exec('mkdir ' + apptmpdir)
        gituri = "https://"+githost+"/jiangsir/" + appname + ".git " + apptmpdir
        self._exec('git clone ' + gituri)

        #choose4 = input("["+appname+"] 請問要取出 1.tag 或者 2. branch：(1, 2) ")
        if version == "latestversion":
            cmd = 'git --git-dir=' + apptmpdir + '/.git --work-tree=' + apptmpdir + ' tag '
            print("cmd=" + cmd)
            tags = subprocess.check_output(cmd.split()).decode(
                'utf-8').rstrip().split('\n')
            latest_tag = 0
            for tag in tags:
                print("tag=" + tag)
                latest_tag = tag
            #tagindex = input("請問要取出哪一個 tag 版本？ ")
            self._exec('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
                       apptmpdir + ' checkout -b branch_'+latest_tag + ' ' + latest_tag)
            # self._exec('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
            #           apptmpdir + ' checkout branch_' + latest_tag)
            open(apptmpdir + '/WebContent/META-INF/Version.txt',
                 mode='w', encoding='utf-8').write(latest_tag)

        elif version == "tag":
            cmd = 'git --git-dir=' + apptmpdir + '/.git --work-tree=' + apptmpdir + ' tag '
            print("cmd=" + cmd)
            tags = subprocess.check_output(cmd.split()).decode(
                'utf-8').rstrip().split('\n')
            count = 0
            for tag in tags:
                print(str(count) + ". tag=" + tag)
                count = count + 1
            tagindex = input("請問要取出哪一個 tag 版本？ ")
            self._exec('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
                       apptmpdir + ' checkout ' + tags[int(tagindex)])
            open(apptmpdir + '/WebContent/META-INF/Version.txt',
                 mode='w', encoding='utf-8').write(tags[int(tagindex)])
        elif version == "branch":
            cmd = 'git --git-dir=' + apptmpdir + \
                '/.git --work-tree=' + apptmpdir + ' branch -a'
            print("cmd=" + cmd)
            branchs = subprocess.check_output(
                cmd.split()).decode('utf-8').rstrip().split('\n')
            count = 0
            for branch in branchs:
                print(str(count) + ". " + branch)
                count = count + 1
            index = input("請問要取出哪一個 branch？ ")
            branchname = branchs[int(index)].split(
                '/')[len(branchs[int(index)].split('/')) - 1]
            self._exec('git --git-dir=' + apptmpdir + '/.git --work-tree=' +
                       apptmpdir + ' checkout ' + branchname)
            cmd = 'git --git-dir=' + apptmpdir + \
                '/.git --work-tree=' + apptmpdir + ' show-branch -g'
            message = subprocess.check_output(cmd.split()).decode('utf-8')
            print('message= ' + message)
            open(apptmpdir + '/WebContent/META-INF/Version.txt',
                 mode='w', encoding='utf-8').write(message)
        else:
            print('version 的參數只能為 ("latestversion", "branch", "tag") ')
            sys.exit()

        # 清除所有的 BOM
        for root, dirs, files in os.walk(apptmpdir + "/src/"):
            for file in files:
                if file.endswith(".java"):
                    # print(os.path.join(root, file))
                    s = open(os.path.join(root, file), mode='r',
                             encoding='utf-8-sig').read()
                    open(os.path.join(root, file), mode='w',
                         encoding='utf-8').write(s)

        if warname == None:
            warname = 'ROOT'
        else:
            warname = input(
                "開始打包 war, 請輸入 所要使用的 App Name 。(不輸入則預設為 ROOT.war): ")
            if warname == '':
                warname = 'ROOT'

        for file in os.listdir('/etc/init.d/'):
            if fnmatch.fnmatch(file, 'tomcat*'):
                tomcatN = file
        if clean == True:
            target = 'clean makewar callpy'
        else:
            target = 'makewar callpy'

        self._exec('ant -f ' + apptmpdir + '/build.xml ' + target + ' -Dappname=' +
                   warname + ' -DTOMCAT_HOME=/usr/share/' + tomcatN + '/')
        self._exec("clear")

        while int(subprocess.call("mysql -u "+dbuser+" -p'"+dbpass+"' -e \"USE "+dbname+";\"", shell=True)) != 0:
            dbpass = input("輸入資料庫 "+dbuser+" 密碼：")

        self._exec("python3 " + apptmpdir +
                   "/build.py build --warname '" + warname + "' --dbuser '" + dbuser + "' --dbpass '" + dbpass+"' --SSL " + str(SSL))

    def build(self):
        pass


if __name__ == '__main__':
    fire.Fire(ZeroJudgeSetup)
