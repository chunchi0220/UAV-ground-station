# UAV-ground-station
這項專案主要是透過 socket UDP 來實現，由PC的地面站發送封包指令到樹梅派，並經由樹梅派中的MAVProxy.py處理 MAVLink 協定的通訊再透過USB傳處理過後的資料給無人機達到控制無人機的效果。 接著再透過 socket UDP 的方式，將無人機回傳的資料寫入txt後，回傳給 PC 的地面站作呈現。
