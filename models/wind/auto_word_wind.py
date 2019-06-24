# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import sys, win32ui, os
import numpy as np
import pandas as pd

sys.path.append(r'H:\GOdoo12_community\myaddons\auto_word\models\wind')
import doc_5

sys.path.append(r'H:\GOdoo12_community\myaddons\auto_word\models\source')
from RoundUp import round_up, Get_Average, Get_Sum


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'content_id'
    # 项目参数
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("其他", u"其他")], string=u"章节分类", required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")

    # 上传参数
    # --------测风信息---------
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")

    # --------机型推荐---------
    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型')
    # --------方案比选---------
    compare_id = fields.Many2one('auto_word_wind_turbines.compare', string=u'方案名')
    name_tur_suggestion = fields.Char(u'推荐机型', compute='_compute_compare_case', readonly=True)
    turbine_numbers_suggestion = fields.Char(u'机位数', compute='_compute_compare_case', readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', compute='_compute_compare_case', readonly=True)
    rotor_diameter_suggestion = fields.Char(string=u'叶轮直径', readonly=True, default="待提交",
                                            compute='_compute_compare_case')
    farm_capacity = fields.Char(string=u'风电场容量', readonly=True, compute='_compute_compare_case', default="待提交")

    case_number = fields.Char(string=u'方案数', default="待提交")
    case_names = fields.Many2many('auto_word_wind_turbines.compare', string=u'方案比选')
    # --------风场信息---------
    IECLevel = fields.Selection([("IA", u"IA"), ("IIA", u"IIA"), ("IIIA", u"IIIA"),
                                 ("IB", u"IB"), ("IIB", u"IIB"), ("IIIB", u"IIIB"),
                                 ("IC", u"IC"), ("IIC", u"IIC"), ("IIIC", u"IIIC"),
                                 ], string=u"IEC等级", default="IIIB", required=True)
    farm_elevation = fields.Char(string=u'海拔高程', default="510~680", required=True)
    farm_area = fields.Char(string=u'区域面积', default="150", required=True)
    farm_speed_range = fields.Char(string=u'风速区间', default="5.2~6.4", required=True)
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")
    # --------结果文件---------
    png_list = []
    auto_word_wind_res = fields.Many2many('auto_word_wind.res', string=u'机位结果', required=True)
    file_excel_path = fields.Char(u'文件路径')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')
    report_attachment_id2 = fields.Many2many('ir.attachment', string=u'图片')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    @api.depends('compare_id')
    def _compute_compare_case(self):
        for re in self:
            re.name_tur_suggestion = re.compare_id.name_tur
            re.hub_height_suggestion = re.compare_id.hub_height_suggestion
            re.turbine_numbers_suggestion = re.compare_id.turbine_numbers
            re.farm_capacity = re.compare_id.farm_capacity
            re.rotor_diameter_suggestion = re.compare_id.rotor_diameter_case

    @api.multi
    def submit_wind(self):
        self.project_id.wind_attachment_ok = u"已提交,版本：" + self.version_id

        self.project_id.case_name = self.compare_id.case_name
        self.project_id.turbine_numbers_suggestion = self.compare_id.turbine_numbers
        self.project_id.hub_height_suggestion = self.compare_id.hub_height_suggestion
        self.project_id.project_capacity = self.compare_id.farm_capacity
        self.project_id.name_tur_suggestion = self.compare_id.name_tur
        self.project_id.investment_E1 = self.compare_id.investment_E1
        self.project_id.investment_E2 = self.compare_id.investment_E2
        self.project_id.investment_E3 = self.compare_id.investment_E3
        self.project_id.investment_E4 = self.compare_id.investment_E4
        self.project_id.investment_E5 = self.compare_id.investment_E5
        self.project_id.investment_E6 = self.compare_id.investment_E6
        self.project_id.investment_E7 = self.compare_id.investment_E7
        self.project_id.investment = self.compare_id.investment
        self.project_id.investment_unit = self.compare_id.investment_unit

    def wind_generate(self):
        tur_name = []
        for i in range(0, len(self.select_turbine_ids)):
            tur_name.append(self.select_turbine_ids[i].name_tur)
        path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5"

        case_name_dict, name_tur_dict, turbine_numbers_dict, capacity_dict = [], [], [], []
        farm_capacity_dict, rotor_diameter_dict, tower_weight_dict = [], [], []
        case_hub_height_dict, power_generation_dict, weak_dict = [], [], []
        power_hours_dict, investment_dict, investment_unit_dict = [], [], []
        investment_E1_dict, investment_E2_dict, investment_E3_dict = [], [], []
        investment_E4_dict, investment_E5_dict, investment_E6_dict, investment_E7_dict = [], [], [], []
        investment_turbines_kws_dict = []

        # 机型结果
        project_id_input_dict, case_name_dict, Turbine_dict, tur_id_dict = [], [], [], []
        X_dict, Y_dict, Z_dict, H_dict, Latitude_dict, Longitude_dict, TrustCoefficient_dict = [], [], [], [], [], [], []
        WeibullA_dict, WeibullK_dict, EnergyDensity_dict, PowerGeneration_dict = [], [], [], []
        PowerGeneration_Weak_dict, CapacityCoe_dict, AverageWindSpeed_dict = [], [], []
        TurbulenceEnv_StrongWind_dict, Turbulence_StrongWind_dict, AverageWindSpeed_Weak_dict = [], [], []
        Weak_res_dict, AirDensity_dict, WindShear_Avg_dict, WindShear_Max_dict, WindShear_Max_Deg_dict = [], [], [], [], []
        InflowAngle_Avg_dict, InflowAngle_Max_dict, InflowAngle_Max_Deg_dict, NextTur_dict = [], [], [], []
        NextLength_M_dict, Diameter_dict, NextLength_D_dict, NextDeg_dict, Sectors_dict = [], [], [], [], []
        hours_year_dict, ongrid_power_dict, Elevation_dict = [], [], []
        ave_elevation, ave_powerGeneration, ave_weak_res, ave_hours_year, ave_ongrid_power = 0, 0, 0, 0, 0
        ave_AverageWindSpeed_Weak, total_powerGeneration, total_ongrid_power, total_powerGeneration_weak = 0, 0, 0, 0

        # 方案比选 Dict
        for i in range(0, len(self.case_names)):
            case_name_dict.append(self.case_names[i].case_name)
            name_tur_dict.append('WTG' + str(int(i + 1)))
            turbine_numbers_dict.append(self.case_names[i].turbine_numbers)
            capacity_dict.append(self.case_names[i].capacity)
            farm_capacity_dict.append(self.case_names[i].farm_capacity)
            rotor_diameter_dict.append(self.case_names[i].rotor_diameter_case)
            case_hub_height_dict.append(self.case_names[i].hub_height_suggestion)
            power_generation_dict.append(self.case_names[i].power_generation)
            weak_dict.append(self.case_names[i].weak)
            power_hours_dict.append(self.case_names[i].power_hours)
            tower_weight_dict.append(str(self.case_names[i].tower_weight))
            investment_E1_dict.append(str(self.case_names[i].investment_E1))
            investment_E2_dict.append(str(self.case_names[i].investment_E2))
            investment_E3_dict.append(str(self.case_names[i].investment_E3))
            investment_E4_dict.append(str(self.case_names[i].investment_E4))
            investment_E5_dict.append(str(self.case_names[i].investment_E5))
            investment_E6_dict.append(str(self.case_names[i].investment_E6))
            investment_E7_dict.append(str(self.case_names[i].investment_E7))
            investment_dict.append(str(self.case_names[i].investment))
            investment_unit_dict.append(str(self.case_names[i].investment_unit))
            investment_turbines_kws_dict.append(str(self.case_names[i].investment_turbines_kws))

        # 结果 Dict
        for re in self.auto_word_wind_res:
            project_id_input_dict.append(re.project_id_input)
            Turbine_dict.append(re.Turbine)
            tur_id_dict.append(re.tur_id)
            X_dict.append(re.X)
            Y_dict.append(re.Y)
            Z_dict.append(round_up(float(re.Z)))
            H_dict.append(round_up(float(re.H)))
            Elevation_dict.append(round_up(float(re.Z)) - round_up(float(re.H)))
            Latitude_dict.append(re.Latitude)
            Longitude_dict.append(re.Longitude)
            TrustCoefficient_dict.append(re.TrustCoefficient)
            WeibullA_dict.append(re.WeibullA)
            WeibullK_dict.append(re.WeibullK)
            EnergyDensity_dict.append(re.EnergyDensity)
            PowerGeneration_dict.append(round_up(float(re.PowerGeneration)))
            PowerGeneration_Weak_dict.append(round_up(float(re.PowerGeneration_Weak)))
            CapacityCoe_dict.append(re.CapacityCoe)
            AverageWindSpeed_dict.append(re.AverageWindSpeed)
            TurbulenceEnv_StrongWind_dict.append(re.TurbulenceEnv_StrongWind)
            Turbulence_StrongWind_dict.append(re.Turbulence_StrongWind)
            AverageWindSpeed_Weak_dict.append(round_up(float(re.AverageWindSpeed_Weak)))
            Weak_res_dict.append(round_up(float(re.Weak)))
            AirDensity_dict.append(re.AirDensity)
            WindShear_Avg_dict.append(re.WindShear_Avg)
            WindShear_Max_dict.append(re.WindShear_Max)
            WindShear_Max_Deg_dict.append(re.WindShear_Max_Deg)
            InflowAngle_Avg_dict.append(re.InflowAngle_Avg)
            InflowAngle_Max_dict.append(re.InflowAngle_Max)
            InflowAngle_Max_Deg_dict.append(re.InflowAngle_Max_Deg)
            NextTur_dict.append(re.NextTur)
            NextLength_M_dict.append(re.NextLength_M)
            Diameter_dict.append(re.Diameter)
            NextLength_D_dict.append(re.NextLength_D)
            NextDeg_dict.append(re.NextDeg)
            Sectors_dict.append(re.Sectors)

            ongrid_power_dict.append(round_up(float(re.ongrid_power)))
            hours_year_dict.append(round_up(float(re.hours_year)))

        ave_elevation = round_up(Get_Average(Elevation_dict))
        ave_AverageWindSpeed_Weak = round_up(Get_Average(AverageWindSpeed_Weak_dict))
        ave_powerGeneration = round_up(Get_Average(PowerGeneration_dict))
        ave_weak_res = round_up(Get_Average(Weak_res_dict))
        ave_weak_res_xz = 1 + ave_weak_res
        ave_hours_year = round_up(Get_Average(hours_year_dict))
        ave_ongrid_power = round_up(Get_Average(ongrid_power_dict))
        total_powerGeneration_weak = round_up(Get_Sum(PowerGeneration_Weak_dict))
        total_powerGeneration = round_up(Get_Sum(PowerGeneration_dict))
        total_ongrid_power = round_up(Get_Sum(ongrid_power_dict))

        result = np.vstack((np.array(X_dict), np.array(Y_dict), np.array(Z_dict),
                            np.array(AverageWindSpeed_Weak_dict),
                            np.array(InflowAngle_Max_dict), np.array(PowerGeneration_dict),
                            np.array(Weak_res_dict), np.array(hours_year_dict), np.array(ongrid_power_dict)
                            ))
        result = result.T

        context = {}
        result_list = []
        result_lables_chapter5 = ['X', 'Y', 'Z', '尾流后风速', '最大入流角', '理论发电量',
                                  '尾流损失', '满发小时', '上网电量']

        context['result_labels'] = result_lables_chapter5
        for i in range(0, len(result)):
            result_dict = {'number': tur_id_dict[i], 'cols': result[i]}
            result_list.append(result_dict)

        context['result_list'] = result_list

        dict5 = doc_5.generate_wind_dict(tur_name, path_images)
        dict_5_word = {
            "最终方案": self.project_id.case_name,
            "方案e": case_name_dict,
            "风机类型e": name_tur_dict,
            "风机台数e": turbine_numbers_dict,
            "单机容量e": capacity_dict,
            "装机容量e": farm_capacity_dict,
            "叶轮直径e": rotor_diameter_dict,
            "轮毂高度e": case_hub_height_dict,
            "上网电量e": power_generation_dict,
            "尾流衰减e": weak_dict,
            "满发小时e": power_hours_dict,
            "塔筒重量e": tower_weight_dict,
            "风机投资e": investment_turbines_kws_dict,
            "塔筒投资e": investment_E1_dict,
            "风机设备投资e": investment_E2_dict,
            "基础投资e": investment_E3_dict,
            "道路投资e": investment_E4_dict,
            "吊装费用e": investment_E5_dict,
            "箱变投资e": investment_E6_dict,
            "集电线路e": investment_E7_dict,
            "发电部分投资e": investment_dict,
            "单位度电投资e": investment_unit_dict,

            "平均海拔": ave_elevation,
            "尾流后平均风速": ave_AverageWindSpeed_Weak,
            "平均发电量": ave_powerGeneration,
            "总发电量": total_powerGeneration,
            "平均尾流损失": ave_weak_res,
            "满发小时": ave_hours_year,
            "平均上网电量": ave_ongrid_power,
            "总上网电量": total_ongrid_power,
            "尾流损失修正系数": ave_weak_res_xz,
            "尾流修正后的总理论发电量": total_powerGeneration_weak,

            "叶轮直径": self.rotor_diameter_suggestion,
            "方案数": self.case_number,
            "海拔高程": self.farm_elevation,
            "区域面积": self.farm_area,
            "平均风速区间": self.farm_speed_range,
            '测风塔名字': self.cft_name_words,
            '测风塔风速信息': self.string_speed_words,
            '测风塔风向信息': self.string_deg_words,
            '推荐轮毂高度': self.hub_height_suggestion,
            'IEC等级': self.IECLevel,

        }
        Dict5 = dict(dict_5_word, **dict5, **context)
        # doc_5.generate_wind_docx(Dict5, path_images)

        for re in self.report_attachment_id2:
            imgdata = base64.standard_b64decode(re.datas)
            t = re.name
            suffix = ".png"
            # suffix = ".xls"
            newfile = t + suffix
            Patt = os.path.join(path_images, '%s') % newfile
            if not os.path.exists(Patt):
                f = open(Patt, 'wb+')
                f.write(imgdata)
                f.close()
            else:
                print(Patt + " already existed.")
                f = open(Patt, 'wb+')
                f.write(imgdata)
                f.close()
            self.png_list.append(t)

        col_name = ['项目名称', '单位', '数量', '单价(元)', '合计(万元)']

        data = pd.read_excel(
            r'D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5\123.xls',
            header=1, sheet_name='施工辅助工程概算表', usecols=col_name)
        print("asdasdasdasdasdssssssssssssssssss")
        print(data["合计(万元)"][1])
        print(len(data.index))
        Dict_e = {}
        for i in range(0, len(data.index)):
            key = data['项目名称'][i]
            value = [data['数量'][i], data['单价(元)'][i], data['合计(万元)'][i]]
            Dict_e[key] = value
        print(Dict_e)

        doc_5.generate_wind_docx1(Dict5, path_images, self.png_list)
        ###########################

        reportfile_name = open(
            file=r'D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5\result_chapter5.docx',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告风电章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告风电章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告风电章节',
                'create_date': fields.date.today(),
                'public': True,  # 此处需设置为true 否则attachments.read  读不到
                # 'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                # 'res_model': 'autoreport.project'
                # 'res_field': 'report_attachment_id'
            })
            print('已创建新纪录：', New)
            print('new dataslen：', len(New.datas))
            self.report_attachment_id = New
        else:
            self.report_attachment_id.datas = base64.standard_b64encode(byte)

        print('new attachment：', self.report_attachment_id)
        print('new datas len：', len(self.report_attachment_id.datas))
        return True


    @api.multi
    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'auto_word.wind'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'auto_word.wind', 'default_res_id': self.id}
        return res

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'auto_word.wind'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)



