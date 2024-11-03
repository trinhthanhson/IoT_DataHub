import MyWisepaas as myTest
import time

# Gửi dữ liệu 60 lần với các giá trị mẫu
for i in range(2):
    myTest.__sendData("Tag2", "222222", "Tag3", "3131", "TagDensity", "3131")
    time.sleep(1)  # Thời gian nghỉ 1 giây giữa các lần gửi
