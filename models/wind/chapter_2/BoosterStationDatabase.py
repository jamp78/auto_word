import pandas as pd
from connect_sql import connect_sql_pandas

import numpy as np


# from RoundUp import round_up, round_dict
# from docxtpl import DocxTemplate
# import math, os

def averagenum(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)


class WindExcel:
    def __init__(self):
        # ===========selecting parameters=============

        # ===========basic parameters==============
        self.Speed_num, self.Direction_num, self.Temperature_num, self.Pressure_num, self.columns_name = 0, 0, 0, 0, []
        self.Speed_col_num, self.Direction_col_num, self.Temperature_col_num, self.Pressure_col_num = 0, 0, 0, 0
        # ===========Calculated parameters==============
        self.DataWind, self.DataWind_speed, self.DataWind_deg = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        self.DataWind_temperature, self.DataWind_pressure = pd.DataFrame(), pd.DataFrame()

        self.wrong_speed_list, self.nan_speed_list = [], []
        self.wrong_deg_list, self.nan_deg_list = [], []
        self.wrong_tem_list, self.nan_tem_list, self.tem_list = [], [], []
        self.tem_avg_vaule, self.reinforcement_booster_station = 0, 0

    def extraction_wind_excel(self, path):
        self.path = path
        col_name = ['Date/Time', 'Speed 70 m A [m/s]', 'Capacity', 'Long', 'Width', 'InnerWallArea', 'WallLength',
                    'StoneMasonryFoot',
                    'StoneMasonryDrainageDitch', 'RoadArea', 'GreenArea', 'ComprehensiveBuilding', 'EquipmentBuilding',
                    'AffiliatedBuilding', 'C30Concrete', 'C15ConcreteCushion', 'MainTransformerFoundation',
                    'AccidentOilPoolC30Concrete', 'AccidentOilPoolC15Cushion', 'AccidentOilPoolReinforcement',
                    'FoundationC25Concrete', 'OutdoorStructure', 'PrecastConcretePole', 'LightningRod'
                    ]

        self.DataWind = pd.read_excel(self.path, header=12, sheet_name='Sheet1')
        self.columns_name = list(self.DataWind.columns.values)

        for i in range(0, len(self.columns_name)):
            name = self.columns_name[i]
            if 'Speed' in name:
                self.Speed_num = self.Speed_num + 1
            if 'Direction' in name:
                self.Direction_num = self.Direction_num + 1
            if 'Temperature' in name:
                self.Temperature_num = self.Temperature_num + 1
            if 'Pressure' in name:
                self.Pressure_num = self.Pressure_num + 1

        list_speed = list(i for i in range(1, self.Speed_num, 4))
        list_speed.insert(0, 0)

        list_deg = list(i for i in range(self.Speed_num + 1, self.Speed_num + self.Direction_num, 4))
        list_deg.insert(0, 0)

        list_temperature = list(i for i in range(self.Speed_num + self.Direction_num + 1,
                                                 self.Speed_num + self.Direction_num + self.Temperature_num, 4))
        list_temperature.insert(0, 0)

        list_pressure = list(i for i in range(self.Speed_num + self.Direction_num + self.Temperature_num + 1,
                                              self.Speed_num + self.Direction_num + self.Temperature_num + self.Pressure_num,
                                              4))
        list_pressure.insert(0, 0)

        self.Speed_col_num = self.Speed_num / 4
        self.Direction_col_num = self.Direction_num / 4
        self.Temperature_col_num = self.Temperature_num / 4
        self.Pressure_col_num = self.Pressure_num / 4

        self.DataWind_speed = self.DataWind.iloc[:, list_speed]
        self.DataWind_deg = self.DataWind.iloc[:, list_deg]
        self.DataWind_temperature = self.DataWind.iloc[:, list_temperature]
        self.DataWind_pressure = self.DataWind.iloc[:, list_pressure]

        return self.DataWind, self.DataWind_speed, self.DataWind_deg, self.DataWind_temperature, self.DataWind_pressure

    def criteria(self, DataWind_speed, DataWind_deg, DataWind_temperature, DataWind_pressure):
        speed_np = np.array(DataWind_speed)
        deg_np = np.array(DataWind_deg)
        tem_np = np.array(DataWind_temperature)
        pres_np = np.array(DataWind_pressure)

        # 风速合理参考值范围为 0,40
        for i in range(1, int(self.Speed_col_num + 1)):
            speed_np_float = speed_np[:, i].astype(float)
            # wrong_wind_num = wrong_wind[(wrong_wind.ix[:, i] > 40) | (wrong_wind.ix[:, i] < 0)].ix[:, i].shape[0]
            # wrong_wind[(wrong_wind.ix[:, i] > 40) | (wrong_wind.ix[:, i] < 0)].ix[:, i]= np.nan

            wrong_speed_num = speed_np_float[np.where((speed_np_float > 40) | (speed_np_float < 0))].shape[0]
            speed_np_float[np.where((speed_np_float > 40) | (speed_np_float < 0))] = np.nan

            nan_speed_num = np.isnan(speed_np_float).sum()

            self.wrong_speed_list.append(wrong_speed_num)
            self.nan_speed_list.append(nan_speed_num)

        # 风向合理参考值范围为 0,360
        for i in range(1, int(self.Direction_col_num + 1)):
            deg_np_float = deg_np[:, i].astype(float)

            wrong_deg_num = deg_np_float[np.where((deg_np_float > 360) | (deg_np_float < 0))].shape[0]
            deg_np_float[np.where((deg_np_float > 360) | (deg_np_float < 0))] = np.nan

            nan_deg_num = np.isnan(deg_np_float).sum()

            self.wrong_deg_list.append(wrong_deg_num)
            self.nan_deg_list.append(nan_deg_num)

        # 温度的合理参考值范围为 -40,50
        for i in range(1, int(self.Temperature_col_num + 1)):
            tem_np_float = tem_np[:, i].astype(float)
            print(tem_np_float)

            wrong_tem_num = tem_np_float[np.where((tem_np_float > 50) | (tem_np_float < -40))].shape[0]
            tem_np_float[np.where((tem_np_float > 50) | (tem_np_float < -40))] = np.nan

            nan_tem_num = np.isnan(tem_np_float).sum()

            tem_avg = tem_np_float[np.where(~np.isnan(tem_np_float))].mean()

            self.wrong_tem_list.append(wrong_tem_num)
            self.nan_tem_list.append(nan_tem_num)
            self.tem_list.append(tem_avg)

        self.tem_avg_vaule = averagenum(self.tem_list)

        # 水汽压合理范围

        # Plow = 94 / (10 ^ (X_HB / 18400 * (1 + (1 / 273) * (X_Tem + X_HB / 200 * 0.6))))
        # '气压最小值kPa， 假设海拔升高100米气温降低0.6℃，压高公式
        # Ptop = 106 / (10 ^ (X_HB / 18400 * (1 + (1 / 273) * (X_Tem + X_HB / 200 * 0.6))))
        # '气压最大值kPa

        # for i in range(1, int(self.Direction_col_num + 1)):
        #     deg_np_float = deg_np[:, i].astype(float)
        #     # wrong_wind_num = wrong_wind[(wrong_wind.ix[:, i] > 40) | (wrong_wind.ix[:, i] < 0)].ix[:, i].shape[0]
        #     # wrong_wind[(wrong_wind.ix[:, i] > 40) | (wrong_wind.ix[:, i] < 0)].ix[:, i]= np.nan
        #
        #     wrong_deg_num = deg_np_float[np.where((deg_np_float > 360) | (deg_np_float < 0))].shape[0]
        #     deg_np_float[np.where((deg_np_float > 360) | (deg_np_float < 0))] = np.nan
        #
        #     nan_deg_num = np.isnan(deg_np_float).sum()
        #
        #     self.wrong_deg_list.append(wrong_deg_num)
        #     self.nan_deg_list.append(nan_deg_num)

        return self.wrong_speed_list, self.nan_speed_list, self.wrong_deg_list, self.nan_deg_list


def generate_dict_booster_station(self, data_booster_station):
    self.data_booster_station = data_booster_station
    self.dict_booster_station = {
        '变电站围墙内面积': self.data_booster_station.at[self.data_booster_station.index[0], 'InnerWallArea'],
        '含放坡面积': self.data_booster_station.at[self.data_booster_station.index[0], 'SlopeArea'],
        '道路面积': self.data_booster_station.at[self.data_booster_station.index[0], 'RoadArea'],
        '围墙长度': self.data_booster_station.at[self.data_booster_station.index[0], 'WallLength'],
        '绿化面积': self.data_booster_station.at[self.data_booster_station.index[0], 'GreenArea'],
        '土方开挖_升压站': self.data_booster_station.at[
            self.data_booster_station.index[0], 'EarthExcavation_BoosterStation'],
        '综合楼': self.data_booster_station.at[self.data_booster_station.index[0], 'ComprehensiveBuilding'],
        '石方开挖_升压站': self.data_booster_station.at[
            self.data_booster_station.index[0], 'StoneExcavation_BoosterStation'],
        '设备楼': self.data_booster_station.at[self.data_booster_station.index[0], 'EquipmentBuilding'],
        '土方回填_升压站': self.data_booster_station.at[
            self.data_booster_station.index[0], 'EarthWorkBackFill_BoosterStation'],
        '附属楼': self.data_booster_station.at[self.data_booster_station.index[0], 'AffiliatedBuilding'],
        '浆砌石护脚': self.data_booster_station.at[self.data_booster_station.index[0], 'StoneMasonryFoot'],
        '主变基础C30混凝土': self.data_booster_station.at[self.data_booster_station.index[0], 'C30Concrete'],
        '浆砌石排水沟': self.data_booster_station.at[self.data_booster_station.index[0], 'StoneMasonryDrainageDitch'],
        'C15混凝土垫层': self.data_booster_station.at[self.data_booster_station.index[0], 'C15ConcreteCushion'],
        '主变压器基础钢筋': self.data_booster_station.at[self.data_booster_station.index[0], 'MainTransformerFoundation'],
        '事故油池C15垫层': self.data_booster_station.at[self.data_booster_station.index[0], 'AccidentOilPoolC15Cushion'],
        '事故油池C30混凝土': self.data_booster_station.at[
            self.data_booster_station.index[0], 'AccidentOilPoolC30Concrete'],
        '事故油池钢筋': self.data_booster_station.at[self.data_booster_station.index[0], 'AccidentOilPoolReinforcement'],
        '设备及架构基础C25混凝土': self.data_booster_station.at[self.data_booster_station.index[0], 'FoundationC25Concrete'],
        '室外架构': self.data_booster_station.at[self.data_booster_station.index[0], 'OutdoorStructure'],
        '预制混凝土杆': self.data_booster_station.at[self.data_booster_station.index[0], 'PrecastConcretePole'],
        '避雷针': self.data_booster_station.at[self.data_booster_station.index[0], 'LightningRod'], }
    return self.dict_booster_station


np.seterr(divide='ignore', invalid='ignore')
wrong_wind_list, nan_wind_list = [], []
project03 = WindExcel()
data, speed, deg, tem, pres = project03.extraction_wind_excel(
    r'D:\GOdoo12_community\myaddons\auto_word\demo\导表\Mast_hour.xlsx')

# 风速不合理性的个数
wrong_speed_list, nan_speed_list, wrong_deg_list, nan_deg_list = project03.criteria(speed, deg, tem, pres)
# print(wrong_speed_list)
# print(nan_speed_list)
# print(wrong_deg_list)
# print(nan_deg_list)

print(project03.tem_avg_vaule)
# print(np.isnan(wind_np[:,1].astype(float)).sum())
# wrong_wind=speed.copy()


# print(data.iloc[:, 1])
# print(deg)
# print(project03.columns_name)
# print(project03.Speed_num)
# print(project03.Direction_num)
# data_cal = project03.excavation_cal_booster_station(data,0.8, 0.2, '陡坡低山')
#
# Dict = round_dict(project03.generate_dict_booster_station(data_cal))
# print(Dict)
# filename_box = ['cr8', 'result_chapter8']
# save_path = r'C:\Users\Administrator\PycharmProjects\Odoo_addons_NB\autocrword\models\chapter_8'
# read_path = os.path.join(save_path, '%s.docx') % filename_box[0]
# save_path = os.path.join(save_path, '%s.docx') % filename_box[1]
# tpl = DocxTemplate(read_path)
# tpl.render(Dict)
# tpl.save(save_path)
