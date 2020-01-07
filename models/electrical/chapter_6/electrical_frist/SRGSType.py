import math
import pandas as pd
from connect_sql import connect_sql_pandas
import numpy as np


# from docxtpl import DocxTemplate
# from RoundUp import round_dict_numbers

# 6 小电阻成套接地装置
class SRGSType:

    def __init__(self):
        # ===========selecting parameters=============
        self.TypeID = 0
        # ===========basic parameters==============
        self.DataSRGSType = pd.DataFrame()
        self.TypeName, self.RatedVoltage, self.RatedCapacity = "", 0, 0
        self.EarthResistanceCurrent, self.ResistanceTolerance, self.FlowTime = 0, 0, 0
    

        # ===========Calculated parameters==============
        # self.earth_excavation_wind_resource, self.stone_excavation_wind_resource = 0, 0
        # self.earth_work_back_fill_wind_resource, self.earth_excavation_wind_resource_numbers = 0, 0
        # self.stone_excavation_wind_resource_numbers, self.earth_work_back_fill_wind_resource_numbers = 0, 0
        # self.c40_wind_resource_numbers, self.c15_wind_resource_numbers, self.c80_wind_resource_numbers = 0, 0, 0
        # self.c80_wind_resource_numbers, self.reinforcement_wind_resource_numbers = 0, 0

    def extraction_data_SRGSType_resource(self, TypeID):
        self.TypeID = TypeID

        sql = "SELECT * FROM auto_word_electrical_srgstype"
        self.DataSRGSType = connect_sql_pandas(sql)
        self.DataSRGSType = \
            self.DataSRGSType.loc[
                self.DataSRGSType['TypeID'] == self.TypeID]
        return self.DataSRGSType

    def excavation_cal_BoxVoltageType_resource(self, DataBoxVoltageType, basic_earthwork_ratio, basic_stone_ratio,
                                               turbine_num):
        self.DataBoxVoltageType = DataBoxVoltageType
        self.basic_earthwork_ratio = basic_earthwork_ratio
        self.basic_stone_ratio = basic_stone_ratio
        self.turbine_numbers = turbine_num

        self.earth_excavation_wind_resource = \
            math.pi * (self.DataBoxVoltageType['FloorRadiusR'] + 1.3) ** 2 * \
            (self.DataBoxVoltageType['H1'] + self.DataBoxVoltageType['H2'] + self.DataBoxVoltageType['H3'] + 0.15) \
            * self.basic_earthwork_ratio

        self.stone_excavation_wind_resource = \
            math.pi * (self.DataBoxVoltageType['FloorRadiusR'] + 1.3) ** 2 * \
            (self.DataBoxVoltageType['H1'] + self.DataBoxVoltageType['H2'] + self.DataBoxVoltageType['H3'] + 0.15) \
            * self.basic_stone_ratio

        self.earth_work_back_fill_wind_resource = \
            self.earth_excavation_wind_resource + self.stone_excavation_wind_resource - \
            self.DataBoxVoltageType['Volume'] - self.DataBoxVoltageType['Cushion']

        self.stone_excavation_wind_resource_numbers = self.stone_excavation_wind_resource * int(self.turbine_numbers)
        self.earth_excavation_wind_resource_numbers = self.earth_excavation_wind_resource * self.turbine_numbers
        self.earth_work_back_fill_wind_resource_numbers = self.earth_work_back_fill_wind_resource * self.turbine_numbers

        self.c40_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Volume'] * self.turbine_numbers
        self.c15_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Cushion'] * self.turbine_numbers
        self.c80_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'C80SecondaryGrouting'] * \
            self.turbine_numbers
        self.DataBoxVoltageType['EarthExcavation_WindResource'] = self.earth_excavation_wind_resource
        self.DataBoxVoltageType['StoneExcavation_WindResource'] = self.stone_excavation_wind_resource
        self.DataBoxVoltageType['EarthWorkBackFill_WindResource'] = self.earth_work_back_fill_wind_resource
        self.DataBoxVoltageType['Reinforcement'] = self.DataBoxVoltageType['Volume'] * 0.1
        self.reinforcement_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Reinforcement'] * self.turbine_numbers

        return self.DataBoxVoltageType

    def generate_dict_SRGSType_resource(self, data, num):
        self.DataSRGSType = data
        self.numbers = num
        self.TypeName = self.DataSRGSType.at[self.DataSRGSType.index[0], 'TypeName']
        self.RatedVoltage = self.DataSRGSType.at[self.DataSRGSType.index[0], 'RatedVoltage']
        self.RatedCapacity = self.DataSRGSType.at[self.DataSRGSType.index[0], 'RatedCapacity']
        self.EarthResistanceCurrent = self.DataSRGSType.at[self.DataSRGSType.index[0], 'EarthResistanceCurrent']
        self.ResistanceTolerance = self.DataSRGSType.at[self.DataSRGSType.index[0], 'ResistanceTolerance']
        self.FlowTime = self.DataSRGSType.at[self.DataSRGSType.index[0], 'FlowTime']
     
        self.dict_SRGSType_resource = {
            'numbers_小电阻成套接地装置': int(self.numbers),
            '型号_小电阻成套接地装置': self.TypeName,
            '额定电压_小电阻成套接地装置': self.RatedVoltage,
            '额定容量_小电阻成套接地装置': self.RatedCapacity,
            '入地阻性电流_小电阻成套接地装置': self.EarthResistanceCurrent,
            '电阻阻值_小电阻成套接地装置': self.ResistanceTolerance,
            '通流时间_小电阻成套接地装置': self.FlowTime,
          }


        return self.dict_SRGSType_resource

# project01 = WindResourceDatabase()
# data = project01.extraction_DataBoxVoltageType(basic_type='扩展基础', ultimate_load=70000, fortification_intensity=7)
# turbine_numbers = 15
# data_cal = project01.excavation_cal_wind_resource(data,0.8, 0.2, turbine_numbers)
# dict_wind_resource = project01.generate_dict_wind_resource(data_cal, turbine_numbers)
# Dict = round_dict_numbers(dict_wind_resource, dict_wind_resource['numbers_tur'])
#
# docx_box = ['cr8', 'result_chapter8']
# save_path = r'C:\Users\Administrator\PycharmProjects\Odoo_addons_NB\autocrword\models\chapter_8'
# readpath = os.path.join(save_path, '%s.docx') % docx_box[0]
# savepath = os.path.join(save_path, '%s.docx') % docx_box[1]
# tpl = DocxTemplate(readpath)
# tpl.render(Dict)
# tpl.save(savepath)
