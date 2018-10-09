# ZeroJudge 安裝及設定

### 說明：

本計劃藉由將 ZeroJudge.tw 打包為一個虛擬機，將一切必要的設定均事先完成，讓使用者的安裝困難度降到最低，以方便更多人使用。並且藉由公開的題目交換格式使得題目可以更容易的互相流通。本系統適合用於程式教學以及 APCS 實作以及各種程式競賽，目前支援 C, C++, JAVA, Pascal, Python 等主要語言。

### 系統特色：
https://zerojudge.tw 公開上線(2007)已逾 10 年時間，是國內自主開發最早的 Online Judge 系統之一，也是目前國內最大的 Online Judge，已經評分超過 400 萬筆程式碼。過去的程式教育面臨著幾個顯著的問題，其一為教學時人力改作業必須耗費大量時間，並且容易出錯，也不精準。其次就是若是學生自學，做完題目也難以知道是否完全正確，必須借助國外類似系統，但語言隔閡又提高了學習門檻。ZeroJudge 具備了自動評分以及原生的中文系統，因而改變程式教育的面貌。本系統主要是著重於「學習」，因此許多錯誤訊息都儘可能提供最詳盡的資訊，不像部分以競賽為導向的系統，錯誤訊息過於精簡，不利學習者發現錯誤。另外，系統設計為不依賴外網資源，可以獨立於封閉環境內進行測驗、競賽，是程式教育的好幫手。

### 運作原理：
ZeroJudge 是一種 Online Judge 系統，Online Judge 系統顧名思義就是線上自動評分，使用者將自己的程式碼上傳到系統內，系統就可以幫忙判斷出這個程式是否正確，而且評分的結果是有權威性的，而非僅供參考，因此程式競賽的評審多半「不是人」。但對於同一個問題，程式的寫法有百百種，又要如何準確判斷是否正確呢？這就是軟體工程裡的「單元測試」的一種延伸運用，或稱為 TDD(Test-Driven Development, 測試驅動開發)。真正開始動手寫程式之前，就先設計 Test case(測試資料)，等到程式設計完成通過 Test case 並且在時限及記憶體要求內完成，就視為正確。

## 請先下載 [ZeroJudge VM](https://drive.google.com/open?id=0B0FdqDzt2OydR1ZVV3g3UUNUaXc) 安裝

虛擬機安裝:
ZeroJudge 虛擬機下載後為一 .ova 檔，請準備好 Virtual Box 並進行匯入。

![image1](images/image1.PNG)<br>
勾選 【重新初始化所有網路卡的MAC位址】

![image1](images/image2.PNG)

![image1](images/image3.PNG)<br>
由於打包虛擬機的環境跟您的環境肯定不一樣, 因此必須變更網路設定

![image1](images/image4.PNG)<br>
設定為橋接介面卡即可

![image1](images/image5.PNG)<br>
登入系統之後, 點開瀏覽器即可看到系統已順利運行。


-------------------------------------------------
### 版本資訊：

前端: ZeroJudge V3.0.1<br>
評分端: ZeroJudge_Server V3.0.1

其它系統資訊：

作業系統：ubuntu server 16.04 LTS<br>
資料庫：Mysql 5.7

webserver: tomcat 8<br>
java: 1.8<br>
g++: 5.4<br>
gcc: 5.4<br>
fpc: 3.0<br>
python: 3.5.2

#### 預設帳密：
OS: 帳號：zero  密碼：!@#$zerojudge<br>
DB: 帳號：root  密碼：!@#$zerojudge<br>
ZeroJudge: 帳號：zero  密碼：!@#$zerojudge<br>

若想更改資料庫密碼:

     mysqladmin -u root -p password

# 請立即修改預設密碼。
--------------------------------------------

### 使用方式：

請先進入虛擬機桌面系統，打開瀏覽器即可看到 http://127.0.0.1 ，即一個空的全新的 ZeroJudge 。

接下來請進入「解題動態」，檢查是否有 5 個 submissions 分別是五個不同的語言對 「a001. 哈囉」的解題，應為 AC。代表評分機也運作正常。

![image1](images/image7.PNG)


本系統預設使用 DHCP 獲取 IP ，若需要固定 IP 請自行修改 /etc/network/interfaces 即可。


    設定固定 IP: 
    nano /etc/network/interfaces 
    加入

    把 iface eth0 inet dhcp 註解掉
    加入
    auto eth0 
    iface eth0 inet static
    address 163.32.92.6
    #network 163.32.92.0
    netmask 255.255.255.0
    #broadcast 163.32.92.255
    gateway 163.32.92.254
    /etc/init.d/networking restart 即可.
    設定 dns
    nano /etc/resolv.conf #编辑配置文件
    nameserver 163.32.92.1 #设置首选dns
    nameserver 8.8.8.8 #设置备用dns


### 解除封印
首先，ZeroJudge 虛擬機預設密碼是公開的，因此，製作虛擬機之初，就考慮到，如果假設架起來，卻沒有適當的修改密碼，或許很迅速的就會被入侵了。因此預設值限制了一些使用範圍，若想開放則必須自行更改設定進行開放。

第一：ssh 連線，預設只有本機可以連線。
sudo nano /etc/hosts.allow
比如: 可以加入 163.32.92.0/24

第二：ZeroJudge 系統本身的管理權限。
預設: zero 這個身分就是管理者，但只有本機可以登入。
如果想要在外部電腦登入管理員，請在虛擬機內登入系統之後，進入「管理系統參數」，【允許管理員登入的子網域】設定管理者可以登入的網路範圍。

![image1](images/image6.PNG)<br>

最後，如果您只在本機進行管理，上兩項設定不動也不影響使用。

### 匯入題庫

感謝板橋高中郭兆平老師慷慨提供【板橋高中教學題】題庫，供大家自由使用，放置於本儲存庫 [problems](problems/) 資料夾檔中，共 42 個題目。

以管理員身分登入 ZeroJudge 系統, 於下拉選單【管理題目】-> 匯入題目 題目可多選，一次可匯入許多題目。

![image1](images/image8.PNG)


# 系統程式升級 - 一行升級

依賴包，安裝過一次即可:

    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install fire

抓取升級程式:
    
    git clone https://github.com/jiangsir/ZeroJudge


## 一行升級
--dbuser 參數指定資料庫使用者<br/>
--dbpass 參數指定資料庫密碼

    sudo python3 ZeroJudge/setup.py install --dbuser 'root' --dbpass 'DBPASSWORD'

![image1](images/image9.PNG)<br>

查看右下角版本資訊是否正確升級。
