import re

# 打開檔案，讀取內容
with open('status.txt', 'r') as file:
    content = file.read()

# 使用正規表達式匹配SYS_STATUS中的voltage_battery值
match = re.search(r'SYS_STATUS {.*?voltage_battery : (\d+).*?}', content)

if match:
    # print(match.group(0))
    voltage_battery_value = int(match.group(1))
    print(f'Voltage Battery: {voltage_battery_value}')
else:
    print('未找到 voltage_battery 值')