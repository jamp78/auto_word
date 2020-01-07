import pandas as pd
import os
import numpy as np


def get_dict_economy(data, sheet_name):
    Dict_e = {}
    data_np = np.array(data)
    for i in range(0, data_np.shape[0]):
        key = str(data_np[i, 0]) + "_" + sheet_name

        value = data_np[i, 1:].tolist()
        value = [str(i) for i in value]
        Dict_e[key] = value
    return Dict_e


economy_images = r"D:\GOdoo12_community\myaddons\auto_word\demo\导表"

t = '01 华润偏关120MW风电场项目可研概算'
suffix_in = ".xls"
suffix_out = ".docx"
inputfile = t + suffix_in
outputfile = 'result_chapter12' + suffix_out
Pathinput = os.path.join(economy_images, '%s') % inputfile
Pathoutput = os.path.join(economy_images, '%s') % outputfile

pd.set_option('display.max_columns', None)
col_name_2 = ['项目名称', '设备购置费(万元)', '建安工程费(万元)', '其他费用(万元)', '合计(万元)', '占总投资比例(%)']
col_name_3 = ['项目名称', '单位', '数量', '单价(元)', '合计(万元)']
col_name_4 = ['名称及规格', '单位', '数量', '设备费（单价）', '安装费（单价）', '设备费（合计）', '安装费（合计）']
col_name_5 = ['工程或费用名称', '单位', '数量', '单价(元)', '合计(万元)']
col_name_6 = ['工程或费用名称', '单位', '数量', '单价(万元)', '合计(万元)']
col_name_7 = ['工程名称', '工程投资', '第1年', '第2年']
col_name_8 = ['工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '装置性材料费',
              '措施费', '间接费', '利润', '税金']
col_name_9 = ['工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '中间单价',
              '措施费', '间接费', '利润', '税金']
col_name_10 = ['序号', '钢筋(t)', '水泥(t)', '桩(m)', '钢材(t)', '电缆(km)']
col_name_11 = ['名称及规格', '台时费', '折旧费', '修理费', '安装拆卸费', '人工费', '动力燃料费',
               '其他费用']
col_name_12 = ['名称及规格', '单位', '预算价格', '原价依据', '原价(元)', '运杂费(元)', '采购及保管费(元)']
col_name_13 = ['混凝土强度 水泥标号 级配', '水泥(kg)', '掺和料(kg)', '砂(m³)', '石子(m³)', '外加剂(kg)',
               '水(m³)', '单价(元)']

col_name_array = [col_name_2, col_name_3, col_name_4, col_name_5, col_name_6, col_name_7,
                  col_name_8, col_name_9, col_name_10, col_name_11, col_name_12, col_name_13]
sheet_name_array = ['工程总概算表', '施工辅助工程概算表', '设备及安装工程概算表', '建筑工程概算表',
                    '其他费用概算表', '分年度投资表', '安装工程单价汇总表', '建筑工程单价汇总表',
                    '主要材料用量汇总表', '施工机械台时费汇总表', '主要材料预算价格计算表',
                    '混凝土材料单价计算表']
dictMerged, Dict = {}, {}
for i in range(0, len(sheet_name_array)):
    # print(sheet_name_array[i], i)
    if i == 2 or i == 5 or i == 9 or i == 10 or i == 11:
        data = pd.read_excel(Pathinput, header=2, sheet_name=sheet_name_array[i], usecols=col_name_array[i])

    elif i == 6 or i == 7:
        data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i], usecols=col_name_array[i])
    else:
        data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i], usecols=col_name_array[i])
    data = data.replace(np.nan, '-', regex=True)
    Dict = get_dict_economy(data, sheet_name_array[i])
    dictMerged.update(Dict)
