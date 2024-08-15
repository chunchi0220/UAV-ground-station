# UAV-ground-station
這項專案主要是透過 socket UDP 來實現，由PC的地面站發送封包指令到樹梅派，並經由樹梅派中的MAVProxy.py處理 MAVLink 協定的通訊再透過USB傳處理過後的資料給無人機達到控制無人機的效果。 接著再透過 socket UDP 的方式，將無人機回傳的資料寫入txt後，回傳給 PC 的地面站作呈現。
## 實作工具
C#、Python、socket(C#)、raspberry pi 、自組無人機、MAVProxy
## Project 概述
這項專案主要是透過 **socket UDP** 來實現，由PC的地面站發送封包指令到樹梅派，並經由樹梅派中的**MAVProxy.py處理 MAVLink 協定的通訊**再透過USB傳處理過後的資料給無人機達到**控制無人機**的效果。
接著再透過 socket UDP 的方式，將無人機回傳的資料寫入txt後，回傳給 PC 的地面站作呈現。

## 功能
### PC(client)
* UAV Ground Control Station(地面站)
    * 使用者介面，負責控制無人機動作以及顯示無人機當前狀態的畫面，透過UDP 發送/接收 MAVLink 封包。
Button
* ARM(解鎖): 解鎖飛行控制器以啟動無人機馬達進行怠速。
* Stabilize(穩定模式): 穩定模式可以讓操作者透過遙控器操作並且自動調整 roll 跟 pitch。
* Altitude Hold(高度保持): 在這種模式下，無人機會自動控制其高度，保持特定的海拔高度。
* Guided(導航模式): 導航模式允許飛行者指定目標點( ex:GPS 座標)，無人機會自動導航到該目標點。
* Loiter(滯留模式): 無人機停在一個特定的點。
* RTL(返航模式): 返航模式允許無人機返回其起飛點，並且自動進行降落。
* Land(降落模式): 降落模式指示無人機進入降落程序，並在到達地面時安全地降落。

Dashboard value
* Drone Status: 無人機當下的電持電壓狀況。
* Mode: 無人機目前是上述的哪種模式。
* Compass: 無人機的羅盤狀況，通常小於0.2都算是健康的。
* Alt、Relative Alt: 無人機所在位置的海平面高度和海平面相對高度。
* Hdg: 無人機的面相角度，0度為面向正北方，順時針。
* Satellites Visible: 無人機收地的衛星訊號數量，因為在室內的關係收不到GPS所以為0。
* Lat: 無人機位置的緯度，因為在室內的關係收不到GPS所以為0。
* Lon: 無人機位置的經度，因為在室內的關係收不到GPS所以為0。
    
### Raspberry Pi(server)
* mavproxy2 .py
    * 負責管理 MAVLink 協定的通訊，作為地面站及無人機的橋樑，接收 PC 端的封包，透過 USB port將資料傳到無人機。
    * 這部分是修改官方給的 source code，新增記錄無人機的資訊到txt，並回傳給地面站的功能(Port 1888)
    * 透過`sudo python3 mavproxy2.py --master=/dev/ttyACM0 --out=tcpin:0.0.0.0:14550 --out=udpin:0.0.0.0:14551`開啟 UDP(Port 14550)、TCP(Port 14551)服務。
        * 我們這段指令寫在樹梅派的bashrc中，這樣只要一開啟樹梅派就會直接啟動mavproxy2程式。
* responser .py
    * 接收無人機發送的 status 資料，將其轉成txt 格式並發送到地面站顯示。
    * 這個py檔算是一個library 有在mavproxy2 .py中引用。
#### Pi + 飛控
MAVProxy是作轉包處理的，將封包轉為飛控(ArduPilot)可以接受的格式
* 安裝MAVProxy
```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3-pip
sudo apt-get install python3-dev
sudo pip3 install future
sudo apt-get install screen python3-wxgtk4.0 python3-lxml
sudo pip3 install pyserial
sudo pip3 install MAVProx
```
* 關閉藍芽
```
sudo nano /boot/config.txt

```
在/boot/config.txt的最下面加入`dtoverlay=disable-bt
`
* 重新開機
```
sudo reboot

```
* 執行mavproxy.py(我們直接將這段寫入bashrc中)
```
sudo python3 mavproxy2.py --master=/dev/ttyACM0 --out=tcpin:0.0.0.0:14550 --out=udpin:0.0.0.0:14551
```
## MAVCommand封包協議
[https://mavlink.io/en/guide/serialization.html
](https://mavlink.io/en/guide/serialization.html
)
### MAVLink 封包組成
MAVLink (Micro Air Vehicle Link) :是一種用於與小型無人機通訊的協定，包含一個標頭（Header）、一個有效載荷（Payload）以及校驗和(Checksum)，其封包的格式是hex。
![image](https://hackmd.io/_uploads/rks_Ac9OT.png)
#### 完整的HEX
Loiter mode：fd0600005effbe0b00000500000001011403
Guided mode：fd06000023ffbe0b0000040000000101912e
Land mode：fd0600002dffbe0b00000900000001015830
RTL mode：fd06000067ffbe0b0000060000000101cf6c
#### HEADER
ex：fd06000045ffbe0b0000
![image](https://hackmd.io/_uploads/BkL-giq_a.png)
* STX：封包格式
    * 0xFE：MAVLINK1
    * 0xFD：MAVLINK2
* LEN：PAYLOAD封包長度
* INC FLAGS：不相容性標記
* CMP FLAGS：相容性標記
* SEQ： heartbeat，檢測通訊品質
* SYS ID：系統ID，用於區分載具(看是飛機、船、車子)
* COMP：發送端組件的ID(像是無人機的鏡頭，可以想成是載具設備中對應的感測器)
* MSG ID：訊息ID，用於定義PAYLOAD類型
#### PAYLOAD
ex：090000000101
![image](https://hackmd.io/_uploads/Hyfi7oqO6.png)
* target_system：設定目標系統mode
    * 04：Guided mode
    * 09：Land mode
    * [https://mavlink.io/zh/messages/ardupilotmega.html#COPTER_MODE](https://mavlink.io/zh/messages/ardupilotmega.html#COPTER_MODE)
* base_mode：基礎mode
* custom_mode：自定義mode
* SYS ID：載具系統ID，用於設定載具編號(看是飛機、船、車子)
* COMP：發送端組件的ID(像是無人機的鏡頭，可以想成是載具設備中對應的感測器)
#### CRC
ex：c1cb
![image](https://hackmd.io/_uploads/B1AfEoc_T.png)
* CRC：用於校驗發送端與接收端的指令
    * 運算範例：
        * [C#](https://github.com/ArduPilot/MissionPlanner/blob/1233399910349feb2e346b84d0b8e51e1c0361ad/ExtLibs/Mavlink/MavlinkCRC.cs)
        * [Python](https://mavlink.io/zh/guide/serialization.html#checksum)
