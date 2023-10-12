import os


fs = os.listdir("/home/aman/drst/pngs")
for i in range(20000):
    if f"doc{i}.png" not in fs:
        print(f"wtf man {i}")