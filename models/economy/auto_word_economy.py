# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import base64, os
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
import global_dict as gl
from RoundUp import round_up


def get_dict_economy(index, col_name, data, sheet_name_array):
    result_dict, context = {}, {}
    result_list = []

    result_labels_name = 'result_labels' + str(index)
    result_list_name = 'result_list' + str(index)
    context[result_labels_name] = col_name
    data_np = np.array(data)
    for i in range(0, data_np.shape[0]):
        key = str(data_np[i, 0])

        if index.strip() == '12_6':
            value = data_np[i, :].tolist()
        else:
            value = data_np[i, 1:].tolist()
        for j in range(0, len(value)):
            if type(value[j]).__name__ == 'float':
                if (index.strip() == '13_4' and i == 1) or ('12' in index.strip()):
                    value[j] = round_up(value[j], 2)
                else:
                    value[j] = round_up(value[j], 2)
        value = [str(i) for i in value]

        result_dict = {'number': key, 'cols': value}
        result_list.append(result_dict)
    context[result_list_name] = result_list

    # key = str(data_np[i, 0]) + "_" + sheet_name
    # value = data_np[i, 1:].tolist()
    # value = [str(i) for i in value]
    # Dict_e[key] = value
    return context


def get_dict_economy_head(col_name, sheet_name):
    Dict_h = {}
    data_np = np.array(col_name)
    key = str(data_np[0]) + "_" + sheet_name
    value = data_np[1:].tolist()
    value = [str(i) for i in value]
    Dict_h[key] = value
    return Dict_h


def generate_economy_docx(Dict, path_images, model_name, outputfile):
    filename_box = [model_name, outputfile]
    read_path = os.path.join(path_images, '%s') % filename_box[0]
    save_path = os.path.join(path_images, '%s') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)


def cal_economy_result(self):
    self.dict_1_submit_word = self.project_id.dict_1_submit_word
    self.dict_5_submit_word = self.project_id.dict_5_submit_word
    self.dict_8_submit_word = self.project_id.dict_8_submit_word

    print("check dict_1_submit_word")
    print(self.dict_1_submit_word)
    if self.dict_1_submit_word == False:
        s = "项目"
        raise exceptions.Warning('请点选 %s，并点击 --> 分发信息（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    if self.dict_5_submit_word == False:
        s = "风能部分"
        raise exceptions.Warning('请点选 %s，并点击风能详情 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    if self.dict_8_submit_word == False:
        s = "土建部分"
        raise exceptions.Warning('请点选 %s，并点击土建详情 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    # 风能
    dictMerged, dictMerged_rows, Dict, dict_content, dict_head = {}, [], {}, {}, {}
    global file_first
    global file_second
    Dict_12_Final, Dict_13_Final = {}, {}
    file_first = False;
    file_second = False
    for re in self.report_attachment_id_input:
        t = re.name
        if '概算' in t:
            chapter_number = 12
            xlsdata_first = base64.standard_b64decode(re.datas)
            name_first = t
            file_first = True
        elif '经济评价' in t:
            chapter_number = 13
            xlsdata_second = base64.standard_b64decode(re.datas)
            name_second = t
            file_second = True
    for chapter_number in range(12, 14):
        if file_first == False:
            return
        elif chapter_number == 13 and file_second == False:
            return
        economy_path = self.env['auto_word.project'].economy_path + str(chapter_number)
        suffix_in = ".xls";
        suffix_out = ".docx"
        if chapter_number == 12:
            inputfile = name_first + suffix_in
        elif chapter_number == 13 and file_second == True:
            inputfile = name_second + suffix_in
        outputfile = 'result_chapter' + str(chapter_number) + suffix_out
        model_name = 'cr' + str(chapter_number) + suffix_out
        Pathinput = os.path.join(economy_path, '%s') % inputfile
        self.Pathoutput = os.path.join(economy_path, '%s') % outputfile
        if not os.path.exists(Pathinput):
            f = open(Pathinput, 'wb+')
            if chapter_number == 12:
                f.write(xlsdata_first)
            elif chapter_number == 13:
                f.write(xlsdata_second)
            f.close()
        else:
            print(Pathinput + " already existed.")
            os.remove(Pathinput)
            f = open(Pathinput, 'wb+')
            if chapter_number == 12:
                f.write(xlsdata_first)
            elif chapter_number == 13:
                f.write(xlsdata_second)
            f.close()

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        dict5 = eval(self.dict_5_submit_word)
        dict8 = eval(self.dict_8_submit_word)

        if chapter_number == 12:
            col_name_0 = ['设备', '单位', '设备价', '备注']
            col_name_1 = ['编号', '材料名称及规格', '单位', '预算价格']
            col_name_2 = ['工程类别', '计算基础', '费率']
            col_name_3 = col_name_2
            col_name_4 = ['工程类别', '分类', '计算基础', '费率']

            col_name_5 = ['费用名称', '计算基础', '费率']
            col_name_7 = ['序号', '项目名称', '设备购置费(万元)', '建安工程费(万元)', '其他费用(万元)', '合计(万元)', '占总投资比例(%)']
            col_name_8 = ['序号', '项目名称', '单位', '数量', '单价(元)', '合计(万元)']
            col_name_9 = ['序号', '名称及规格', '单位', '数量', '设备费（单价）', '安装费（单价）', '设备费（合计）', '安装费（合计）']
            col_name_10 = ['序号', '工程或费用名称', '单位', '数量', '单价(元)', '合计(万元)']
            col_name_11 = ['序号', '工程或费用名称', '单位', '数量', '单价(万元)', '合计(万元)']
            col_name_12 = ['序号', '工程名称', '工程投资', '第1年', '第2年']
            col_name_13 = ['编号', '工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '装置性材料费',
                           '措施费', '间接费', '利润', '税金']
            col_name_14 = ['编号', '工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '中间单价',
                           '措施费', '间接费', '利润', '税金']
            col_name_15 = ['序号', '钢筋(t)', '水泥(t)', '桩(m)', '钢材(t)', '电缆(km)']
            col_name_16 = ['编号', '名称及规格', '台时费', '折旧费', '修理费', '安装拆卸费', '人工费', '动力燃料费',
                           '其他费用']
            col_name_17 = ['编号', '名称及规格', '单位', '预算价格', '原价依据', '原价(元)', '运杂费(元)', '采购及保管费(元)']
            col_name_18 = ['编号', '混凝土强度 水泥标号 级配', '水泥(kg)', '掺和料(kg)', '砂(m³)', '石子(m³)', '外加剂(kg)',
                           '水(m³)', '单价(元)']
            col_name_6 = []

            col_name_array = [col_name_0, col_name_1, col_name_2, col_name_3, col_name_4, col_name_5, col_name_6,
                              col_name_7, col_name_8, col_name_9, col_name_10, col_name_11, col_name_12,
                              col_name_13, col_name_14,
                              # col_name_15, col_name_16, col_name_17
                              ]
            sheet_name_array = ['主要设备价格汇总表', '主要材料价格表', '建筑工程措施费费率表', '建筑工程间接费费率表',
                                '安装工程措施费费率表', '主要费率指标表', '主要技术经济指标表', '工程总概算表',
                                '施工辅助工程概算表', '设备及安装工程概算表', '建筑工程概算表', '其他费用概算表', '分年度投资表',
                                # '安装工程单价汇总表', '建筑工程单价汇总表', '主要材料用量汇总表', '施工机械台时费汇总表',
                                # '主要材料预算价格计算表', '混凝土材料单价计算表'
                                ]
            for i in range(0, len(sheet_name_array)):
                # print(sheet_name_array[i], i)
                if i == 9 or i == 12:
                    data = pd.read_excel(Pathinput, header=2, sheet_name=sheet_name_array[i],
                                         # usecols=col_name_array[i]
                                         )
                elif i == 6:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                         # usecols=col_name_array[i]
                                         )
                else:
                    data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i],
                                         # usecols=col_name_array[i]
                                         )
                data = data.replace(np.nan, '-', regex=True)

                tabel_number = str(chapter_number) + '_' + str(i)
                dict_content = get_dict_economy(tabel_number, col_name_array[i], data, sheet_name_array[i])
                dictMerged.update(dict_content)

            self.cost_time = str(dictMerged['result_list12_1'][len(dictMerged['result_list12_1']) - 4]['cols'][0])
            # self.cost_location = str(
            #     dictMerged['result_list12_1'][len(dictMerged['result_list12_1']) - 3]['cols'][0])
            self.cost_water = str(dictMerged['result_list12_1'][len(dictMerged['result_list12_2']) - 1]['cols'][2])
            self.cost_electricity = str(
                dictMerged['result_list12_1'][len(dictMerged['result_list12_1']) - 1]['cols'][2])
            self.additional_construction_rate = \
                str(dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 2]['cols'][0])
            self.additional_c_value_rate = \
                str(dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 1]['cols'][0])
            self.indirect_cost_rate = \
                str(dictMerged['result_list12_4'][len(dictMerged['result_list12_4']) - 3]['cols'][2])
            self.additional_installation_rate = \
                str(dictMerged['result_list12_4'][len(dictMerged['result_list12_4']) - 2]['cols'][2])
            self.additional_i_value_rate = \
                str(dictMerged['result_list12_4'][len(dictMerged['result_list12_4']) - 1]['cols'][2])

            self.longterm_lending_rate_12 = \
                str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 3]['cols'][1])
            self.capital_rate_12 = \
                str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 2]['cols'][1])

            self.domestic_bank_loan = \
                str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 1]['cols'][1])

            for i in range(0, len(dictMerged['result_list12_6'])):  # 主要技术经济指标表 6
                if str(dictMerged['result_list12_6'][i]['cols'][1]) == '风电场名称':
                    self.Farm_words = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][1]) == '建设地点':
                    self.Location_words = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][1]) == '建设单位':
                    self.company_id = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '装机规模':
                    self.project_capacity = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '单机容量':
                    self.TurbineCapacity = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '年发电量':
                    self.Generating_capacity_words = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '年利用小时数':
                    self.Hour_words = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '静态投资':
                    self.static_investment_12 = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '工程总投资':
                    self.dynamic_investment_12 = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '单位千瓦投资':
                    self.static_investment_unit = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '单位电量投资':
                    self.unit_cost_words = str(dictMerged['result_list12_6'][i]['cols'][2])
                if str(dictMerged['result_list12_6'][i]['cols'][0]) == '建设期利息':
                    self.interest_construction_loans_12 = str(dictMerged['result_list12_6'][i]['cols'][2])

                if str(dictMerged['result_list12_6'][i]['cols'][3]) == '风电机组设备价格':
                    self.investment_turbines_kws = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][3]) == '塔筒(架)设备价格':
                    self.Tower_cost_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][3]) == '风电机组基础造价':
                    self.infrastructure_cost_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '土石方开挖':
                    self.Earth_excavation_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '回填':
                    self.EarthWorkBackFill_WindResource = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '钢筋':
                    self.Reinforcement = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '混凝土':
                    self.Concrete_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '塔筒':
                    self.Towter_weight_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '永久用地':
                    self.Permanent_land_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '临时用(租)地':
                    self.temporary_land_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '第一批(组)机组发电工期':
                    self.First_turbine_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][4]) == '总工期':
                    self.Project_time_words = str(dictMerged['result_list12_6'][i]['cols'][6])
                if str(dictMerged['result_list12_6'][i]['cols'][3]) == '生产单位定员':
                    self.staff_words = str(dictMerged['result_list12_6'][i]['cols'][6])

            for i in range(0, len(dictMerged['result_list12_7'])):  # 工程总概算表 7

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '施工辅助工程':
                    self.construction_assistance = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '工程静态投资(一～五)部分合计':
                    self.static_investment_12 = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '设备及安装工程':
                    self.equipment_installation = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '建筑工程':
                    self.constructional_engineering = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '其他费用':
                    self.other_expenses = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '基本预备费':
                    self.basic_funds = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '建设期利息':
                    self.interest_construction_loans_12 = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '工程总投资(一～七)部分合计':
                    self.dynamic_investment_12 = str(dictMerged['result_list12_7'][i]['cols'][4])

                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '单位千瓦静态投资(元/kW)':
                    self.static_investment_unit = str(dictMerged['result_list12_7'][i]['cols'][4])
                if str(dictMerged['result_list12_7'][i]['cols'][0]) == '单位千瓦动态投资(元/kW)':
                    self.dynamic_investment_unit = str(dictMerged['result_list12_7'][i]['cols'][4])

            self.Farm_words = self.project_id.Farm_words
            self.Lon_words = self.project_id.Lon_words
            self.Lat_words = self.project_id.Lat_words
            self.Location_words = self.project_id.Location_words
            self.Elevation_words = self.project_id.Elevation_words
            self.area_words = self.project_id.area_words
            self.company_id = self.project_id.company_id.name

            self.project_capacity = self.project_id.project_capacity
            self.TurbineCapacity = self.project_id.TurbineCapacity
            self.turbine_numbers_suggestion = self.project_id.turbine_numbers_suggestion

            self.ongrid_power = self.project_id.ongrid_power
            self.Hour_words = self.project_id.Hour_words

            self.road_1_num = self.project_id.road_1_num
            self.road_2_num = self.project_id.road_2_num
            self.road_3_num = self.project_id.road_3_num
            self.total_civil_length = self.project_id.total_civil_length

            self.Permanent_land_words = self.project_id.permanent_land_area
            self.temporary_land_words = self.project_id.temporary_land_area

            self.Reinforcement = self.project_id.Reinforcement

            if self.investment_turbines_kws == "-":
                self.investment_turbines_kws = self.project_id.investment_turbines_kws
            if self.unit_cost_words == "-":
                self.unit_cost_words = round_up(float(self.dynamic_investment_12) / (float(self.ongrid_power) / 10), 2)
            if self.Towter_weight_words == "-":
                self.Towter_weight_words = float(self.project_id.tower_weight) * float(self.turbine_numbers_suggestion)

            if self.Project_time_words == "-":
                self.Project_time_words = 12

            if self.EarthWorkBackFill_WindResource == "-":
                # self.EarthWorkBackFill_WindResource = self.project_id.EarthWorkBackFill_WindResource
                self.EarthWorkBackFill_WindResource = self.project_id.excavation

            if self.Earth_excavation_words == "-":
                # self.Earth_excavation_words = round_up(float(self.project_id.EarthExcavation_WindResource) + float(
                #     self.project_id.StoneExcavation_WindResource), 2)
                self.Earth_excavation_words = self.project_id.excavation

            self.Concrete_words = round_up(float(self.project_id.Volume) + float(
                self.project_id.Cushion), 2)

            self.turbine_numbers_suggestion = int(
                float(self.project_capacity) / (float(self.TurbineCapacity)))

            dict_12_res_word = {
                "价格日期": self.cost_time,
                # "价格地点": self.cost_location,
                "施工水价": self.cost_water,
                "施工电价": self.cost_electricity,

                "建筑措施费利率": self.additional_construction_rate,
                "建筑增值税率": self.additional_c_value_rate,

                "间接费率": self.indirect_cost_rate,
                "安装措施费利率": self.additional_installation_rate,
                "安装增值税率": self.additional_i_value_rate,

                "长期贷款利率_12": self.longterm_lending_rate_12,
                "资本金比例_12": self.capital_rate_12,

                "静态总投资_12": self.static_investment_12,
                "施工辅助工程": self.construction_assistance,
                "设备及安装工程": self.equipment_installation,
                "建筑工程": self.constructional_engineering,
                "其他费用": self.other_expenses,
                "基本预备费": self.basic_funds,
                "单位千瓦静态投资": self.static_investment_unit,
                "国内银行贷款": self.domestic_bank_loan,
                "建设期贷款利息_12": self.interest_construction_loans_12,
                "动态总投资_12": self.dynamic_investment_12,
                "单位千瓦动态投资": self.dynamic_investment_unit,
            }
            self.dict_12_res_word = dict_12_res_word
            dict_12_word = {
                "施工总工期": self.Project_time_words,
                "塔筒": self.Towter_weight_words,
                "混凝土": self.Concrete_words,
                "钢筋": self.Reinforcement,

                "第一台机组发电工期": self.First_turbine_words,
                "总工期": self.Project_time_words,
                "生产单位定员": self.staff_words,
                "风电机组单位造价": self.investment_turbines_kws,
                "塔筒单位造价": self.Tower_cost_words,
                "风电机组基础单价": self.infrastructure_cost_words,
                "单位度电投资": self.unit_cost_words,
            }

            Dict12 = dict(dict_12_word, **dictMerged, **dict_12_res_word, **dict5,
                          **dict8
                          )
            print(Dict12)
            Dict_12_Final = dict(dict_12_word, **dict_12_res_word)
            for key, value in Dict_12_Final.items():
                gl.set_value(key, value)

            generate_economy_docx(Dict12, economy_path, model_name, outputfile)
        if chapter_number == 13:
            sheet_name_array = ['投资计划与资金筹措表', '财务指标汇总表', '单因素敏感性分析表', '总成本费用表',
                                '利润和利润分配表', '借款还本付息计划表', '项目投资现金流量表', '项目资本金现金流量表',
                                '财务计划现金流量表', '资产负债表', '财务指标汇总表', '参数汇总表', '基本参数']
            for i in range(0, len(sheet_name_array)):
                # print(sheet_name_array[i], i)
                if i == 6:
                    data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                         skip_footer=7)
                    col_name = data.columns.tolist()
                    col_name[0] = '序号'
                    col_name[1] = '项目'
                    col_name[2] = '合计'

                elif i == 7:
                    data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                         skip_footer=2)
                    col_name = data.columns.tolist()
                    col_name[0] = '序号'
                    col_name[1] = '项目'
                    col_name[2] = '合计'

                elif i == 0 or (i >= 3 and i < 9):
                    data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                         )
                    col_name = data.columns.tolist()
                    col_name[0] = '序号'
                    col_name[1] = '项目'
                    col_name[2] = '合计'

                elif i == 9:
                    data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i], )
                    col_name = data.columns.tolist()
                    col_name[0] = '序号'
                    col_name[1] = '项目'

                elif i == 12:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                         )
                    col_name = data.columns.tolist()

                elif i == 2:
                    data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i],
                                         usecols="A:F")
                    col_name = data.columns.tolist()
                else:
                    data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i], )
                    col_name = data.columns.tolist()

                data = data.replace(np.nan, '-', regex=True)
                col_name_array.append(col_name)

                tabel_number = str(chapter_number) + '_' + str(i)
                dict_content = get_dict_economy(tabel_number, col_name, data, sheet_name_array[i])
                dictMerged.update(dict_content)

            self.static_investment_13 = str(dictMerged['result_list13_11'][5]['cols'][2])
            self.tax_deductible = str(dictMerged['result_list13_11'][8]['cols'][2])
            self.interest_construction_loans_13 = str(dictMerged['result_list13_10'][3]['cols'][2])
            self.dynamic_investment_13 = str(dictMerged['result_list13_11'][6]['cols'][2])
            self.working_fund = str(dictMerged['result_list13_10'][4]['cols'][2])
            self.total_investment_13 = str(dictMerged['result_list13_10'][2]['cols'][2])
            self.capital_rate_13 = str(dictMerged['result_list13_11'][7]['cols'][2])
            self.construction_investment_13 = str(dictMerged['result_list13_0'][1]['cols'][1])

            self.profit_tax_investment_ratio = str(dictMerged['result_list13_10'][20]['cols'][2])
            self.pre_tax_investment_net_value = str(dictMerged['result_list13_10'][15]['cols'][2])
            self.tax_investment_net_value = str(dictMerged['result_list13_10'][16]['cols'][2])
            self.asset_liability_ratio = str(dictMerged['result_list13_10'][22]['cols'][2])

            self.fixed_investment_13 = str(
                round_up(float(self.dynamic_investment_13) - float(self.tax_deductible), 2))
            self.fund_raising_13 = str(dictMerged['result_list13_0'][5]['cols'][1])
            self.load_rate_13 = str(100 - float(self.capital_rate_13))
            self.load_investment_13 = str(dictMerged['result_list13_0'][8]['cols'][1])

            self.longterm_lending_13 = str(dictMerged['result_list13_0'][10]['cols'][1])
            self.longterm_lending_rate_13 = str(dictMerged['result_list13_11'][13]['cols'][2])

            self.repayment_period = str(dictMerged['result_list13_11'][11]['cols'][2])
            self.grid_price = str(dictMerged['result_list13_11'][26]['cols'][2])

            self.Internal_financial_rate_before = str(dictMerged['result_list13_10'][13]['cols'][2])
            self.Internal_financial_rate_after = str(dictMerged['result_list13_10'][14]['cols'][2])
            self.Internal_financial_rate_capital = str(dictMerged['result_list13_10'][17]['cols'][2])

            self.payback_period = str(dictMerged['result_list13_10'][12]['cols'][2])
            self.ROI_13 = str(dictMerged['result_list13_10'][19]['cols'][2])
            self.ROE_13 = str(dictMerged['result_list13_10'][21]['cols'][2])

            dict_13_res_word = {
                '可抵扣税金': self.tax_deductible,
                "静态总投资_13": self.static_investment_13,
                "建设期贷款利息_13": self.interest_construction_loans_13,
                "动态总投资_13": self.dynamic_investment_13,
                "流动资金_13": self.working_fund,
                "总投资_13": self.total_investment_13,
                "资本金比例_13": self.capital_rate_13,
                "建设投资_13": self.construction_investment_13,
                "投产后固定资产_13": self.fixed_investment_13,
                "资金筹措_13": self.fund_raising_13,
                "贷款比例_13": self.load_rate_13,
                "贷款总额_13": self.load_investment_13,

                "中长期借款本金_13": self.longterm_lending_13,
                "长期贷款利率_13": self.longterm_lending_rate_13,
                "还款期限_13": self.repayment_period,
                "上网电价_13": self.grid_price,
                "投资利税率": self.profit_tax_investment_ratio,
                "税前项目投资财务净现值": self.pre_tax_investment_net_value,
                "税后项目投资财务净现值": self.tax_investment_net_value,
                "资产负债率": self.asset_liability_ratio,

                "税前财务内部收益率_13": self.Internal_financial_rate_before,
                "税后财务内部收益率_13": self.Internal_financial_rate_after,
                "资本金税后财务内部收益率_13": self.Internal_financial_rate_capital,
                "投资回收期_13": self.payback_period,

                "总投资收益率_13": self.ROI_13,
                "资本金利润率_13": self.ROE_13,
            }

            Dict13 = dict(dict_12_word, **dictMerged, **dict_13_res_word, **self.dict_12_res_word, **dict5,
                          **dict8
                          )
            Dict_13_Final = dict(dictMerged, **dict_13_res_word)

            for key, value in Dict_13_Final.items():
                gl.set_value(key, value)

            generate_economy_docx(Dict13, economy_path, model_name, outputfile)

        # ###########################
        reportfile_name = open(file=self.Pathoutput, mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        if (chapter_number == 12):
            if (str(self.report_attachment_id_output12) == 'ir.attachment()'):
                Attachments = self.env['ir.attachment']
                print('开始创建新纪录12')
                New = Attachments.create({
                    'name': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '下载页',
                    'datas_fname': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '.docx',
                    'datas': base64.standard_b64encode(byte),
                    'display_name': self.project_id.project_name + '可研报告经评章节',
                    'create_date': fields.date.today(),
                    'public': True,  # 此处需设置为true 否则attachments.read  读不到
                })
                print('已创建新纪录：', New)
                print('new dataslen：', len(New.datas))
                self.report_attachment_id_output12 = New
            else:
                self.report_attachment_id_output12.datas = base64.standard_b64encode(byte)
        elif (chapter_number == 13 and file_second == True):
            if (str(self.report_attachment_id_output13) == 'ir.attachment()'):
                Attachments = self.env['ir.attachment']
                print('开始创建新纪录13')
                New = Attachments.create({
                    'name': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '下载页',
                    'datas_fname': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '.docx',
                    'datas': base64.standard_b64encode(byte),
                    'display_name': self.project_id.project_name + '可研报告经评章节',
                    'create_date': fields.date.today(),
                    'public': True,  # 此处需设置为true 否则attachments.read  读不到
                })
                print('已创建新纪录：', New)
                print('new dataslen：', len(New.datas))
                self.report_attachment_id_output13 = New
            else:
                self.report_attachment_id_output13.datas = base64.standard_b64encode(byte)

            print('new attachment：', self.report_attachment_id_output13)
            print('new datas len：', len(self.report_attachment_id_output13.datas))

    return Dict_12_Final, Dict_13_Final


class auto_word_economy(models.Model):
    _name = 'auto_word.economy'
    _description = 'economy res'
    _rec_name = 'content_id'
    # 项目参数

    # 提交
    dict_12_submit_word = fields.Char(u'字典8_提交')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    dict_5_submit_word = fields.Char(u'字典5_提交')
    dict_8_submit_word = fields.Char(u'字典8_提交')

    Pathoutput = fields.Char(u'输出路径')

    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("经评", u"经评"), ("其他", u"其他")], string=u"章节分类", required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id_output12 = fields.Many2one('ir.attachment', string=u'可研报告经评章节12')
    report_attachment_id_output13 = fields.Many2one('ir.attachment', string=u'可研报告经评章节13')
    report_attachment_id_input = fields.Many2many('ir.attachment', string=u'经济性评价结果')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    xls_list = []
    # 风能
    Lon_words = fields.Char(string=u'东经', default="待提交", readonly=True)
    Lat_words = fields.Char(string=u'北纬', default="待提交", readonly=True)
    Elevation_words = fields.Char(string=u'海拔高程', default="待提交", readonly=True)
    Relative_height_difference_words = fields.Char(string=u'相对高差', default="待提交", readonly=True)
    # 土建
    total_civil_length = fields.Char(string=u'道路工程长度', default='待提交')
    road_1_num = fields.Char(string=u'改扩建道路', default='待提交')
    road_2_num = fields.Char(string=u'进站道路', default='待提交')
    road_3_num = fields.Char(string=u'新建施工检修道路', default='待提交')
    Permanent_land_words = fields.Char(string=u'永久用地', default='待提交')
    temporary_land_words = fields.Char(string=u'临时用地', default='待提交')

    # 经评
    Project_time_words = fields.Char(string=u'施工总工期', default='12')
    TurbineCapacity = fields.Char(string=u'单机容量', default="待提交", readonly=True)
    project_capacity = fields.Char(string=u'装机容量', readonly=True)
    project_capacity_B = fields.Char(string=u'装机容量_B')
    turbine_numbers_suggestion = fields.Char(string=u'机组数量', readonly=True)

    Generating_capacity_words = fields.Char(string=u'年发电量', default="待提交", readonly=True)
    Hour_words = fields.Char(string=u'满发小时', default="待提交", readonly=True)
    ongrid_power = fields.Char(u'上网电量', default="待提交", readonly=True)

    Towter_weight_words = fields.Char(string=u'塔筒总重量（吨）', default='待提交')
    Earth_excavation_words = fields.Char(string=u'土石方开挖（m3）', default='待提交')
    EarthWorkBackFill_WindResource = fields.Char(string=u'土石方回填（m3）', default='待提交')

    Concrete_words = fields.Char(string=u'混凝土(万m³)', default='待提交')
    Reinforcement = fields.Char(string=u'钢筋(吨)', default='待提交')

    # 计划施工时间
    First_turbine_words = fields.Char(string=u'第一台机组发电工期', default='待提交')
    # total_turbine_words = fields.Char(string=u'总工期', default='12')
    staff_words = fields.Char(string=u'生产单位定员', default='待提交')

    # 项目状况
    Farm_words = fields.Char(string=u'风电场名称')
    Location_words = fields.Char(string=u'建设地点', readonly=True)
    company_id = fields.Char(string=u'项目大区', readonly=True)
    investment_turbines_kws = fields.Char(string=u'风电机组单位造价')
    Tower_cost_words = fields.Char(string=u'塔筒（架）单位造价', default='待提交')
    infrastructure_cost_words = fields.Char(string=u'风电机组基础单价', default='待提交')
    unit_cost_words = fields.Char(string=u'单位度电投资', default='待提交')
    area_words = fields.Char(string=u'风场面积', readonly=True)

    # 结果
    cost_time = fields.Char(string=u'价格日期')
    # cost_location = fields.Char(string=u'价格地点')
    cost_water = fields.Char(string=u'施工水价')
    cost_electricity = fields.Char(string=u'施工电价')
    additional_construction_rate = fields.Char(string=u'建筑措施费利率')
    additional_c_value_rate = fields.Char(string=u'建筑增值税率')

    indirect_cost_rate = fields.Char(string=u'间接费率')
    additional_installation_rate = fields.Char(string=u'安装措施费利率')
    additional_i_value_rate = fields.Char(string=u'安装增值税率')
    longterm_lending_rate_12 = fields.Char(string=u'长期贷款利率_12')
    capital_rate_12 = fields.Char(string=u'资本金比例')

    static_investment_12 = fields.Char(string=u'静态总投资')
    construction_assistance = fields.Char(string=u'施工辅助工程')
    equipment_installation = fields.Char(string=u'设备及安装工程')
    constructional_engineering = fields.Char(string=u'建筑工程')
    other_expenses = fields.Char(string=u'其他费用')
    basic_funds = fields.Char(string=u'基本预备费')

    static_investment_unit = fields.Char(string=u'单位千瓦静态投资')

    domestic_bank_loan = fields.Char(string=u'国内银行贷款')
    interest_construction_loans_12 = fields.Char(string=u'建设期贷款利息_12')
    dynamic_investment_12 = fields.Char(string=u'动态总投资')
    dynamic_investment_unit = fields.Char(string=u'单位千瓦动态投资')
    dict_12_res_word = {}
    # chapter 13
    tax_deductible = fields.Char(string=u'可抵扣税金')
    static_investment_13 = fields.Char(string=u'静态总投资')
    interest_construction_loans_13 = fields.Char(string=u'建设期贷款利息_13')
    dynamic_investment_13 = fields.Char(string=u'动态总投资')
    working_fund = fields.Char(string=u'流动资金_13')
    total_investment_13 = fields.Char(string=u'总投资_13')
    capital_rate_13 = fields.Char(string=u'资本金比例')
    construction_investment_13 = fields.Char(string=u'建设投资_13')
    fixed_investment_13 = fields.Char(string=u'投产后固定资产_13')
    fund_raising_13 = fields.Char(string=u'资金筹措_13')
    load_rate_13 = fields.Char(string=u'贷款比例_13')
    load_investment_13 = fields.Char(string=u'贷款总额_13')
    longterm_lending_13 = fields.Char(string=u'中长期借款本金_13')
    longterm_lending_rate_13 = fields.Char(string=u'长期贷款利率_13')

    repayment_period = fields.Char(string=u'还款期限_13')
    grid_price = fields.Char(string=u'上网电价_13')
    profit_tax_investment_ratio = fields.Char(string=u'投资利税率')
    pre_tax_investment_net_value = fields.Char(string=u'税前项目投资财务净现值')
    tax_investment_net_value = fields.Char(string=u'税后项目投资财务净现值')
    asset_liability_ratio = fields.Char(string=u'资产负债率')

    Internal_financial_rate_before = fields.Char(string=u'税前财务内部收益率(%)')
    Internal_financial_rate_after = fields.Char(string=u'税后财务内部收益率(%)')
    Internal_financial_rate_capital = fields.Char(string=u'资本金税后内部收益率(%)')
    payback_period = fields.Char(string=u'投资回收期(年)')
    ROI_13 = fields.Char(string=u'总投资收益率(%)')
    ROE_13 = fields.Char(string=u'资本金利润率(%)')

    def economy_generate(self):
        Dict_12_Final, Dict_13_Final = cal_economy_result(self)
        self.project_id.Dict_12_Final = Dict_12_Final
        self.project_id.Dict_13_Final = Dict_13_Final
        return True

    @api.multi
    def action_get_attachment_economy_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'auto_word.economy'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'auto_word.economy', 'default_res_id': self.id}
        return res

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'auto_word.economy'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    def economy_refresh(self):
        # 风能
        self.Farm_words = self.project_id.Farm_words
        self.Lon_words = self.project_id.Lon_words
        self.Lat_words = self.project_id.Lat_words
        self.Location_words = self.project_id.Location_words
        self.Elevation_words = self.project_id.Elevation_words
        self.area_words = self.project_id.area_words
        self.company_id = self.project_id.company_id.name

        self.project_capacity = self.project_id.project_capacity
        self.ongrid_power = self.project_id.ongrid_power
        self.Hour_words = self.project_id.Hour_words

        self.road_1_num = self.project_id.road_1_num
        self.road_2_num = self.project_id.road_2_num
        self.road_3_num = self.project_id.road_3_num
        self.total_civil_length = self.project_id.total_civil_length

        self.Permanent_land_words = self.project_id.permanent_land_area
        self.temporary_land_words = self.project_id.temporary_land_area
        return True

    def submit_economy(self):
        self.project_id.static_investment_12 = self.static_investment_12
        self.project_id.construction_assistance = self.construction_assistance
        self.project_id.equipment_installation = self.equipment_installation
        self.project_id.constructional_engineering = self.constructional_engineering
        self.project_id.other_expenses = self.other_expenses
        self.project_id.static_investment_unit = self.static_investment_unit

        self.project_id.capital_rate_12 = self.capital_rate_12
        self.project_id.domestic_bank_loan = self.domestic_bank_loan
        self.project_id.interest_construction_loans_12 = self.interest_construction_loans_12
        self.project_id.dynamic_investment_12 = self.dynamic_investment_12

        self.project_id.static_investment_13 = self.static_investment_13
        self.project_id.static_investment_unit = self.static_investment_unit
        self.project_id.Internal_financial_rate_before = self.Internal_financial_rate_before
        self.project_id.Internal_financial_rate_after = self.Internal_financial_rate_after
        self.project_id.Internal_financial_rate_capital = self.Internal_financial_rate_capital
        self.project_id.dynamic_investment_13 = self.dynamic_investment_13
        self.project_id.dynamic_investment_unit = self.dynamic_investment_unit
        self.project_id.payback_period = self.payback_period
        self.project_id.ROI_13 = self.ROI_13
        self.project_id.ROE_13 = self.ROE_13
        self.project_id.grid_price = self.grid_price
        self.project_id.Concrete_words = self.Concrete_words
        self.project_id.Reinforcement = self.Reinforcement

        self.project_id.Project_time_words = self.Project_time_words

        return True
