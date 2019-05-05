import pandas as pd
from connect_sql import connect_sql_pandas


# import numpy as np
# from RoundUp import round_up, round_dict
# from docxtpl import DocxTemplate
# import math, os

class WindExcel:
    def __init__(self):
        # ===========selecting parameters=============


        # ===========basic parameters==============
        self.Speed_num, self.Direction_num, self.columns_name = 0, 0, []
        self.dict_booster_station = {}
        # ===========Calculated parameters==============
        self.DataWind,self.DataWind_speed, self.DataWind_deg = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        self.slope_area, self.earth_excavation_booster_station, self.stone_excavation_booster_station = 0, 0, 0
        self.earthwork_back_fill_booster_station, self.c30_booster_station, self.c15_booster_station = 0, 0, 0
        self.c15_oil_pool_booster_station, self.c30_oil_pool_booster_station = 0, 0
        self.c25_foundation_booster_station, self.reinforcement_booster_station = 0, 0

    def extraction_wind_excel(self, path):
        a=[]
        self.path = path
        col_name = ['Date/Time', 'Speed 70 m A [m/s]', 'Capacity', 'Long', 'Width', 'InnerWallArea', 'WallLength',
                    'StoneMasonryFoot',
                    'StoneMasonryDrainageDitch', 'RoadArea', 'GreenArea', 'ComprehensiveBuilding', 'EquipmentBuilding',
                    'AffiliatedBuilding', 'C30Concrete', 'C15ConcreteCushion', 'MainTransformerFoundation',
                    'AccidentOilPoolC30Concrete', 'AccidentOilPoolC15Cushion', 'AccidentOilPoolReinforcement',
                    'FoundationC25Concrete', 'OutdoorStructure', 'PrecastConcretePole', 'LightningRod'
                    ]

        self.DataWind = pd.read_excel(self.path,
            header=12, sheet_name='Sheet1')
        self.columns_name=list(self.DataWind.columns.values)


        for i in range(0,len(self.columns_name)):
            name=self.columns_name[i]
            if 'Speed' in name:
                self.Speed_num=self.Speed_num+1
            if 'Direction' in name:
                self.Direction_num=self.Direction_num+1

        speed_col=list(i for i in range(1, self.Speed_num, 4))
        speed_col.insert(0,0)

        speed_deg = list(i for i in range(self.Speed_num+1, self.Speed_num+self.Direction_num, 4))
        speed_deg.insert(0, 0)

        self.DataWind_speed=self.DataWind.iloc[:, speed_col]
        self.DataWind_deg = self.DataWind.iloc[:, speed_deg]


        return self.DataWind,self.DataWind_speed,self.DataWind_deg

    def excavation_cal_booster_station(self, data_booster_station, road_basic_earthwork_ratio, road_basic_stone_ratio,
                                       terrain_type):
        self.data_booster_station = data_booster_station
        self.road_basic_earthwork_ratio = road_basic_earthwork_ratio
        self.road_basic_stone_ratio = road_basic_stone_ratio
        self.TerrainType = terrain_type

        if self.TerrainType == '平原':
            self.slope_area = (self.data_booster_station['Long'] + 5) * (self.data_booster_station['Width'] + 5)
            self.earth_excavation_booster_station = self.slope_area * 0.3 * self.road_basic_earthwork_ratio / 10
            self.stone_excavation_booster_station = self.slope_area * 0.3 * self.road_basic_stone_ratio / 10
            self.earthwork_back_fill_booster_station = self.slope_area * 2
        else:
            self.slope_area = (self.data_booster_station['Long'] + 10) * (self.data_booster_station['Width'] + 10)
            self.earth_excavation_booster_station = self.slope_area * 3 * self.road_basic_earthwork_ratio
            self.stone_excavation_booster_station = self.slope_area * 3 * self.road_basic_stone_ratio
            self.earthwork_back_fill_booster_station = self.slope_area * 0.5

        self.c30_booster_station = self.data_booster_station.at[self.data_booster_station.index[0], 'C30Concrete']

        self.c15_booster_station = \
            self.data_booster_station.at[self.data_booster_station.index[0], 'C15ConcreteCushion']

        self.c15_oil_pool_booster_station = \
            self.data_booster_station.at[self.data_booster_station.index[0], 'AccidentOilPoolC15Cushion']

        self.c30_oil_pool_booster_station = \
            self.data_booster_station.at[self.data_booster_station.index[0], 'AccidentOilPoolC30Concrete']

        self.c25_foundation_booster_station = \
            self.data_booster_station.at[self.data_booster_station.index[0], 'FoundationC25Concrete']

        self.reinforcement_booster_station = \
            self.data_booster_station.at[self.data_booster_station.index[0], 'MainTransformerFoundation'] + \
            self.data_booster_station.at[self.data_booster_station.index[0], 'AccidentOilPoolReinforcement'] + \
            self.data_booster_station.at[self.data_booster_station.index[0], 'LightningRod']

        self.data_booster_station['EarthExcavation_BoosterStation'] = self.earth_excavation_booster_station
        self.data_booster_station['StoneExcavation_BoosterStation'] = self.stone_excavation_booster_station
        self.data_booster_station['EarthWorkBackFill_BoosterStation'] = self.earthwork_back_fill_booster_station
        self.data_booster_station['SlopeArea'] = self.slope_area

        return self.data_booster_station

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


project03 = WindExcel()
data,speed,deg = project03.extraction_wind_excel(r'C:\Users\Administrator\Desktop\Mast_hour.xlsx')
print(data)
print(speed)
print(deg)
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
