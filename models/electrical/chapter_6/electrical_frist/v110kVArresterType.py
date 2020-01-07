import math
import pandas as pd
from connect_sql import connect_sql_pandas
import numpy as np


# from docxtpl import DocxTemplate
# from RoundUp import round_dict_numbers


# 4.2 110kV避雷器
class v110kVArresterType:

    def __init__(self):
        # ===========selecting parameters=============
        self.TypeID = 0
        # ===========basic parameters==============
        self.Data110kVArresterType = pd.DataFrame()
        self.TypeName, self.RatedVoltageArrester, self.OperatingVoltageArrester = "", 0, ""
        self.DischargeCurrentArrester, self.LightningResidualVoltage = "", ""
        # ===========Calculated parameters==============
        # self.earth_excavation_wind_resource, self.stone_excavation_wind_resource = 0, 0
        # self.earth_work_back_fill_wind_resource, self.earth_excavation_wind_resource_numbers = 0, 0
        # self.stone_excavation_wind_resource_numbers, self.earth_work_back_fill_wind_resource_numbers = 0, 0
        # self.c40_wind_resource_numbers, self.c15_wind_resource_numbers, self.c80_wind_resource_numbers = 0, 0, 0
        # self.c80_wind_resource_numbers, self.reinforcement_wind_resource_numbers = 0, 0

    def extraction_data_110kVArresterType_resource(self, TypeID):
        self.TypeID = TypeID

        sql = "SELECT * FROM auto_word_electrical_110kVArresterType"
        self.Data110kVArresterType = connect_sql_pandas(sql)
        self.Data110kVArresterType = \
            self.Data110kVArresterType.loc[
                self.Data110kVArresterType['TypeID'] == self.TypeID]
        return self.Data110kVArresterType

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

    def generate_dict_110kVArresterType_resource(self, data, num):
        self.Data110kVArresterType = data
        self.numbers = num
        self.TypeName = self.Data110kVArresterType.at[self.Data110kVArresterType.index[0], 'TypeName']
        
        self.RatedVoltageArrester = self.Data110kVArresterType.at[self.Data110kVArresterType.index[0], 'RatedVoltageArrester']
        self.OperatingVoltageArrester = self.Data110kVArresterType.at[self.Data110kVArresterType.index[0], 'OperatingVoltageArrester']
        self.DischargeCurrentArrester = self.Data110kVArresterType.at[self.Data110kVArresterType.index[0], 'DischargeCurrentArrester']
        self.LightningResidualVoltage = self.Data110kVArresterType.at[self.Data110kVArresterType.index[0], 'LightningResidualVoltage']
     
        self.dict_110kVArresterType_resource = {
            'numbers_110kV避雷器': int(self.numbers),
            '型号_110kV避雷器': self.TypeName,
            '避雷器额定电压_110kV避雷器': self.RatedVoltageArrester,
            '避雷器持续运行电压_110kV避雷器': self.OperatingVoltageArrester,
            '避雷器的标称放电电流_110kV避雷器': self.DischargeCurrentArrester,
            '雷电冲击电流残压_110kV避雷器': self.LightningResidualVoltage,
        }
        return self.dict_110kVArresterType_resource

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
