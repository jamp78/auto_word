# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64, os
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np

from RoundUp import round_up


def get_dict_economy(index, col_name, data, sheet_name_array):
    result_dict, context = {}, {}
    result_list = []

    result_labels_name = 'result_labels' + str(index)
    result_list_name = 'result_list' + str(index)
    context[result_labels_name] = col_name
    data_np = np.array(data)
    # print(data_np.shape[0], sheet_name_array)
    for i in range(0, data_np.shape[0]):
        key = str(data_np[i, 0])

        if index.strip() == '12_7':
            value = data_np[i, :].tolist()
        else:
            value = data_np[i, 1:].tolist()
        for j in range(0, len(value)):
            if type(value[j]).__name__ == 'float':
                value[j] = round_up(value[j], 3)
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


class auto_word_economy(models.Model):
    _name = 'auto_word.economy'
    _description = 'economy res'
    _rec_name = 'content_id'
    # 项目参数
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
    Lon_words = fields.Char(string=u'东经', default='111.334294')
    Lat_words = fields.Char(string=u'北纬', default='23.132694')
    Elevation_words = fields.Char(string=u'海拔高程', default='588m～852m')
    Relative_height_difference_words = fields.Char(string=u'相对高差', default='100m-218m')
    # 土建
    Re_road_words = fields.Char(string=u'新改建道路', default='66.64')
    Extension_road_words = fields.Char(string=u'场内改扩建道路', default='15')
    New_road_words = fields.Char(string=u'新建施工检修道路', default='51.64')
    Permanent_land_words = fields.Char(string=u'永久用地', default='38.36')
    temporary_land_words = fields.Char(string=u'临时用地', default='1467.95')

    # 经评
    Project_time_words = fields.Char(string=u'施工总工期', default='18')
    Turbine_capacity_words = fields.Char(string=u'单机容量', default='2.5')
    Turbine_number_words = fields.Char(string=u'风力发电机组', default='40')
    Farm_capacity_words = fields.Char(string=u'装机容量', default='100')
    Generating_capacity_words = fields.Char(string=u'发电量', default='205531.5')
    Hour_words = fields.Char(string=u'满发小时', default='2055')

    Towter_weight_words = fields.Char(string=u'塔筒', default='8975.72')
    Earth_excavation_words = fields.Char(string=u'土石方开挖', default='154.7')
    Earth_backfill_words = fields.Char(string=u'土石方回填', default='56.01')
    Concrete_words = fields.Char(string=u'混凝土', default='3.62')
    Steel_weight_words = fields.Char(string=u'钢筋', default='2565.6')

    # 计划施工时间
    First_turbine_words = fields.Char(string=u'第一台机组发电工期', default='15')
    total_turbine_words = fields.Char(string=u'总工期', default='18')
    staff_words = fields.Char(string=u'生产单位定员', default='12')

    # 项目状况
    Farm_words = fields.Char(string=u'风电场名称', default='8975.72')
    Location_words = fields.Char(string=u'建设地点', default='154.7')
    Construction_words = fields.Char(string=u'建设单位', default='56.01')
    Turbine_cost_words = fields.Char(string=u'风电机组单位造价', default='3500')
    Tower_cost_words = fields.Char(string=u'塔筒（架）单位造价', default='10500')
    infrastructure_cost_words = fields.Char(string=u'风电机组基础单价', default='841155')
    unit_cost_words = fields.Char(string=u'单位度电投资', default='3.59')

    # 结果
    cost_time = fields.Char(string=u'价格日期')
    cost_location = fields.Char(string=u'价格地点')
    cost_water = fields.Char(string=u'施工水价')
    cost_electricity = fields.Char(string=u'施工电价')
    additional_construction_rate = fields.Char(string=u'建筑措施费利率')
    additional_c_value_rate = fields.Char(string=u'建筑增值税率')

    indirect_cost_rate = fields.Char(string=u'间接费率')
    additional_installation_rate = fields.Char(string=u'安装措施费利率')
    additional_i_value_rate = fields.Char(string=u'安装增值税率')
    longterm_lending_rate = fields.Char(string=u'长期贷款利率')
    capital_rate = fields.Char(string=u'资本金比例')

    static_investment_12 = fields.Char(string=u'静态总投资_12')
    construction_assistance = fields.Char(string=u'施工辅助工程')
    equipment_installation = fields.Char(string=u'设备及安装工程')
    constructional_engineering = fields.Char(string=u'建筑工程')
    other_expenses = fields.Char(string=u'其他费用')
    static_investment_unit = fields.Char(string=u'单位千瓦静态投资')

    domestic_bank_loan = fields.Char(string=u'国内银行贷款')
    interest_construction_loans_12 = fields.Char(string=u'建设期贷款利息_12')
    dynamic_investment_12 = fields.Char(string=u'动态总投资')
    dynamic_investment_unit = fields.Char(string=u'单位千瓦动态投资')
    dict_12_res_word={}
    # chapter 13

    def economy_generate(self):
        chapter_number = 0
        dictMerged, Dict, dict_content, dict_head = {}, {}, {}, {}
        dict_12_word = {
            "东经": self.Lon_words,
            "北纬": self.Lon_words,
            "海拔高程": self.Elevation_words,
            "相对高差": self.Relative_height_difference_words,
            "新改建道路": self.Re_road_words,
            "场内改扩建道路": self.Extension_road_words,
            "新建施工检修道路": self.New_road_words,
            "永久用地": self.Permanent_land_words,
            "临时用地": self.temporary_land_words,

            "施工总工期": self.Project_time_words,
            "单机容量": self.Turbine_capacity_words,
            "风力发电机组": self.Turbine_number_words,
            "装机容量": self.Farm_capacity_words,
            "发电量": self.Generating_capacity_words,
            "满发小时": self.Hour_words,

            "塔筒": self.Towter_weight_words,
            "土石方开挖": self.Earth_excavation_words,
            "土石方回填": self.Earth_backfill_words,
            "混凝土": self.Concrete_words,
            "钢筋": self.Steel_weight_words,

            "第一台机组发电工期": self.First_turbine_words,
            "总工期": self.total_turbine_words,
            "生产单位定员": self.staff_words,

            "风电场名称": self.Farm_words,
            "建设地点": self.Location_words,
            "建设单位": self.Construction_words,
            "风电机组单位造价": self.Turbine_cost_words,
            "塔筒单位造价": self.Tower_cost_words,
            "风电机组基础单价": self.infrastructure_cost_words,
            "单位度电投资": self.unit_cost_words,

        }

        for re in self.report_attachment_id_input:
            xlsdata = base64.standard_b64decode(re.datas)
            t = re.name
            if '概算' in t:
                chapter_number = 12
            elif '经济评价' in t:
                chapter_number = 13
            economy_path = self.env['auto_word.project'].economy_path + str(chapter_number)

            suffix_in = ".xls"
            suffix_out = ".docx"
            inputfile = t + suffix_in
            outputfile = 'result_chapter' + str(chapter_number) + suffix_out
            model_name = 'cr' + str(chapter_number) + suffix_out
            Pathinput = os.path.join(economy_path, '%s') % inputfile
            Pathoutput = os.path.join(economy_path, '%s') % outputfile
            if not os.path.exists(Pathinput):
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                f.close()
            else:
                print(Pathinput + " already existed.")
                os.remove(Pathinput)
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                f.close()
            self.xls_list.append(t)

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)

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
                    print(sheet_name_array[i], i)
                    if i == 9 or i == 12:
                        data = pd.read_excel(Pathinput, header=2, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])
                    elif i == 6:
                        data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                             # usecols=col_name_array[i]
                                             )
                    else:
                        data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])
                    data = data.replace(np.nan, '-', regex=True)

                    tabel_number = str(chapter_number) + '_' + str(i + 1)
                    dict_content = get_dict_economy(tabel_number, col_name_array[i], data, sheet_name_array[i])
                    # Dict_head = get_dict_economy_head(col_name_array[i], sheet_name_array[i])
                    # Dict = dict(Dict_content, **Dict_head)
                    dictMerged.update(dict_content)

                self.cost_time = str(dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 4]['cols'][0])
                self.cost_location = str(
                    dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 3]['cols'][0])
                self.cost_water = str(dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 2]['cols'][2])
                self.cost_electricity = str(
                    dictMerged['result_list12_2'][len(dictMerged['result_list12_2']) - 1]['cols'][2])
                self.additional_construction_rate = \
                    str(dictMerged['result_list12_3'][len(dictMerged['result_list12_3']) - 2]['cols'][0])
                self.additional_c_value_rate = \
                    str(dictMerged['result_list12_3'][len(dictMerged['result_list12_3']) - 1]['cols'][0])
                self.indirect_cost_rate = \
                    str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 3]['cols'][2])
                self.additional_installation_rate = \
                    str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 2]['cols'][2])
                self.additional_i_value_rate = \
                    str(dictMerged['result_list12_5'][len(dictMerged['result_list12_5']) - 1]['cols'][2])

                self.longterm_lending_rate = \
                    str(dictMerged['result_list12_6'][len(dictMerged['result_list12_6']) - 3]['cols'][1])
                self.capital_rate = \
                    str(dictMerged['result_list12_6'][len(dictMerged['result_list12_6']) - 2]['cols'][1])
                self.static_investment = str(dictMerged['result_list12_8'][22]['cols'][4])
                self.construction_assistance = str(dictMerged['result_list12_8'][0]['cols'][4])
                self.equipment_installation = str(dictMerged['result_list12_8'][4]['cols'][4])
                self.constructional_engineering = str(dictMerged['result_list12_8'][9]['cols'][4])
                self.other_expenses = str(dictMerged['result_list12_8'][14]['cols'][4])
                self.static_investment_unit = str(dictMerged['result_list12_8'][26]['cols'][4])
                self.domestic_bank_loan = \
                    str(dictMerged['result_list12_6'][len(dictMerged['result_list12_6']) - 1]['cols'][1])

                self.interest_construction_loans_12 = \
                    str(dictMerged['result_list12_8'][24]['cols'][4])
                self.dynamic_investment_12 = \
                    str(dictMerged['result_list12_8'][25]['cols'][4])
                self.dynamic_investment_unit = \
                    str(dictMerged['result_list12_8'][27]['cols'][4])

                dict_12_res_word = {
                    "价格日期": self.cost_time,
                    "价格地点": self.cost_location,
                    "施工水价": self.cost_water,
                    "施工电价": self.cost_electricity,

                    "建筑措施费利率": self.additional_construction_rate,
                    "建筑增值税率": self.additional_c_value_rate,

                    "间接费率": self.indirect_cost_rate,
                    "安装措施费利率": self.additional_installation_rate,
                    "安装增值税率": self.additional_i_value_rate,

                    "长期贷款利率": self.longterm_lending_rate,
                    "资本金比例": self.capital_rate,

                    "静态总投资_12": self.static_investment_12,
                    "施工辅助工程": self.construction_assistance,
                    "设备及安装工程": self.equipment_installation,
                    "建筑工程": self.constructional_engineering,
                    "其他费用": self.other_expenses,
                    "单位千瓦静态投资": self.static_investment_unit,
                    "国内银行贷款": self.domestic_bank_loan,
                    "建设期贷款利息_12": self.interest_construction_loans_12,
                    "动态总投资_12": self.dynamic_investment_12,
                    "单位千瓦动态投资": self.dynamic_investment_unit,
                }
                self.dict_12_res_word=dict_12_res_word
                Dict12 = dict(dict_12_word, **dictMerged, **dict_12_res_word)
                generate_economy_docx(Dict12, economy_path, model_name, outputfile)
            if chapter_number == 13:
                col_name_1 = ['序号', '项目', '合计', '第1年', '第2年']
                col_name_2 = ['序号', '项目', '单位', '数值']
                col_name_3 = ['方案类型', '变化幅度（%）', '投资回收期(所得税后)(年)', '项目投资财务内部收益率(所得税前)(%)',
                              '项目投资财务内部收益率(所得税后)(%)', '资本金财务内部收益率（%）']
                # '项目投资财务净现值（所得税后）（万元）', '资本金财务净现值（万元）', '总投资收益率（ROI）（ % ）',
                # '投资利税率（ % ）', '项目资本金净利润率（ROE）（ % ）', '资产负债率（ % ）']
                col_name_4 = ['序号', '项目', '合计', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                              '13', '14', '15', '16', '17', '18', '19', '20', '21']
                col_name_5, col_name_6, col_name_7, col_name_8, col_name_9, col_name_10 = col_name_4, col_name_4, col_name_4, col_name_4, col_name_4, col_name_4

                col_name_11 = ['序号', '项目', '单位', '数值']
                col_name_12 = col_name_11

                col_name_array = [col_name_1, col_name_2, col_name_3, col_name_4, col_name_5, col_name_6,
                                  col_name_7, col_name_8, col_name_9, col_name_10, col_name_11, col_name_12]
                sheet_name_array = ['投资计划与资金筹措表', '财务指标汇总表', '单因素敏感性分析表', '总成本费用表',
                                    '利润和利润分配表', '借款还本付息计划表', '项目投资现金流量表', '项目资本金现金流量表',
                                    '财务计划现金流量表', '资产负债表', '财务指标汇总表', '参数汇总表']
                for i in range(0, len(sheet_name_array)):
                    # print(sheet_name_array[i], i)
                    if i == 6:
                        data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                             skip_footer=7)
                    elif i == 7:
                        data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                             skip_footer=2)

                    elif i == 0 or (i >= 3 and i <= 9):
                        data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                             )
                    else:
                        data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])
                    data = data.replace(np.nan, '-', regex=True)

                    tabel_number = str(chapter_number) + '_' + str(i)
                    dict_content = get_dict_economy(tabel_number, col_name_array[i], data, sheet_name_array[i])
                    # Dict_head = get_dict_economy_head(col_name_array[i], sheet_name_array[i])
                    # Dict = dict(Dict_content, **Dict_head)
                    dictMerged.update(dict_content)
                dict_13_word = {

                }

                tax_deductible = fields.Char(string=u'可抵扣税金')
                static_investment_13 = fields.Char(string=u'静态总投资_13')
                interest_construction_loans_13 = fields.Char(string=u'建设期贷款利息_13')
                dynamic_investment_13 = fields.Char(string=u'动态总投资_13')
                working_fund = fields.Char(string=u'流动资金_13')
                total_investment_13 = fields.Char(string=u'总投资_13')

                self.static_investment_13 = str(dictMerged['result_list13_11'][5]['cols'][2])
                self.tax_deductible = str(dictMerged['result_list13_11'][8]['cols'][2])
                self.interest_construction_loans_13 = str(dictMerged['result_list13_10'][3]['cols'][2])
                self.dynamic_investment_13 = str(dictMerged['result_list13_11'][6]['cols'][2])
                self.working_fund = str(dictMerged['result_list13_10'][4]['cols'][2])
                self.total_investment_13 = str(dictMerged['result_list13_10'][2]['cols'][2])

                dict_13_res_word = {

                    '可抵扣税金': self.tax_deductible,
                    "静态总投资_13": self.static_investment_13,
                    "建设期贷款利息_13": self.interest_construction_loans_13,
                    "动态总投资_13": self.dynamic_investment_13,
                    "流动资金_13": self.working_fund,
                    "总投资_13": self.total_investment_13,
                }

                Dict13 = dict(dict_13_word, **dictMerged, **dict_13_res_word, **self.dict_12_res_word)
                print("ssssssssssssssssssssss")
                print(Dict13)
                generate_economy_docx(Dict13, economy_path, model_name, outputfile)

            # ###########################

            reportfile_name = open(file=Pathoutput, mode='rb')
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

            elif (chapter_number == 13):
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
