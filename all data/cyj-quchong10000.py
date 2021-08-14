"""
数据去重
例如：共有十列，若有多行数据的前九列数据相同，则将第十行数据用均值代替，再使用excel去掉重复行
"""
import pandas as pd
ThePath = r"./quchong_prepare_input.xlsx"
df = pd.read_excel(ThePath)
# print(df)
print("-"*100)
print(len(df))  # 18911
list = []
dict = {}
if "color2" in dict.keys():
    print("ok")
for i in range(len(df)):
    # 前九列组成字符串
    name = str(df["一"][i]) + "-" + str(df["二"][i]) + "-" + str(df["三"][i]) + "-" + str(df["四"][i]) + "-" + str(df["五"][i]) + "-" + str(df["六"][i]) + "-" + str(df["七"][i]) + "-" + str(df["八"][i]) + "-" + str(df["九"][i])
    if name in dict.keys():
        index = dict[name]
        sum = int(index.split("-")[0])  # 分割出当前重复行的第十列值的求和sum
        num = int(index.split("-")[1])  # 分割出当前重复行的第十列值的次数num
        dict[name] = str(sum + df["十"][i]) + "-" + str(num + 1)     # 再次出现时，value为"第十列求和-总次数"
    else:
        dict[name] = str(df["十"][i]) + "-" + str(1)     # 初次出现时，value为“第十列值-1"
print(dict)
print(len(dict))
# 此处其实可以只对字典进行处理，那么将不再初次重复行
for i in range(len(df)):
    index = dict[str(df["一"][i]) + "-" + str(df["二"][i]) + "-" + str(df["三"][i]) + "-" + str(df["四"][i]) + "-" + str(
            df["五"][i]) + "-" + str(df["六"][i]) + "-" + str(df["七"][i]) + "-" + str(df["八"][i]) + "-" + str(
            df["九"][i])]
    list.append(int(index.split("-")[0])/int(index.split("-")[1]))  # 求出均值
print(list)
# print(list)
print("-"*100)
df["十"] = list  # 第十列均值代替
print(df)
df.to_excel(r"./tmp.xlsx")
print("写入成功！")