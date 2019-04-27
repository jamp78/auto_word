# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import doc_5
import RoundUp


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'content_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("其他", u"其他")], string=u"章节分类", required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")

    IECLevel = fields.Selection([("IA", u"IA"), ("IIA", u"IIA"), ("IIIA", u"IIIA"),
                                 ("IB", u"IB"), ("IIB", u"IIB"), ("IIIB", u"IIIB"),
                                 ("IC", u"IC"), ("IIC", u"IIC"), ("IIIC", u"IIIC"),
                                 ], string=u"IEC等级", default="IIIB", required=True)
    farm_elevation = fields.Char(string=u'海拔高程', default="待提交", required=True)
    farm_area = fields.Char(string=u'区域面积', default="待提交", required=True)
    farm_speed_range = fields.Char(string=u'风速区间', default="待提交", required=True)
    select_ids = fields.Many2many('wind_turbines.selection', required=True, string=u'机型推荐')

    farm_capacity = fields.Char(string=u'风电场容量', readonly=True, compute='_compute_compare_case', default="待提交")
    rotor_diameter_selection = fields.Char(string=u'叶轮直径', readonly=True, default="待提交",
                                           compute='_compute_compare_case')

    rotor_diameter_case = fields.Char(string=u'叶轮直径', default="待提交")

    name_tur_selection = fields.Char(string=u'风机型号', readonly=True, default="待提交",
                                     compute='_compute_turbine_numbers')

    generator_ids = fields.Many2many('auto_word_wind.turbines', string=u'比选机型')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')

    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")

    case_number = fields.Char(string=u'方案数', default="待提交")

    case_names = fields.Many2many('auto_word_wind_turbines.compare',string=u'方案比选')

    case_name_selection = fields.Char(u'方案名称', compute='_compute_compare_case', readonly=True)
    name_tur_selection = fields.Char(u'推荐机型', compute='_compute_compare_case', readonly=True)
    turbine_numbers_selection = fields.Char(u'机位数', compute='_compute_compare_case', readonly=True)

    hub_height_selection = fields.Char(u'推荐轮毂高度', compute='_compute_compare_case', readonly=True)

    compare_id = fields.Many2one('auto_word_wind_turbines.compare', string=u'方案名', required=True)

    @api.depends('compare_id')
    def _compute_compare_case(self):
        for re in self:
            re.case_name_selection = re.compare_id.case_name
            re.name_tur_selection = re.compare_id.name_tur
            re.hub_height_selection = re.compare_id.case_hub_height
            re.turbine_numbers_selection = re.compare_id.turbine_numbers
            re.farm_capacity = re.compare_id.farm_capacity
            re.rotor_diameter_selection = re.compare_id.rotor_diameter_case

    # @api.depends('select_ids')
    # def _compute_turbine_numbers(self):
    #     rotor_diameter_words,name_tur_selction_words = '',''
    #     for re in self:
    #         for i in range(0, len(re.select_ids)):
    #             re.turbine_numbers = str(int(re.select_ids[i].turbine_numbers) + int(re.turbine_numbers))
    #             re.farm_capacity = str(
    #                 int(re.select_ids[i].turbine_numbers) * int(re.select_ids[i].capacity) + int(re.farm_capacity))
    #
    #             if i != len(re.select_ids) - 1:
    #                 rotor_diameter_words = str(re.select_ids[i].rotor_diameter) + "/" + rotor_diameter_words
    #                 name_tur_selction_words = str(re.select_ids[i].name_tur) + "/" + name_tur_selction_words
    #             else:
    #                 rotor_diameter_words = rotor_diameter_words + str(re.select_ids[i].rotor_diameter)
    #                 name_tur_selction_words = name_tur_selction_words + str(re.select_ids[i].name_tur)
    #
    #         re.farm_capacity = str(int(re.farm_capacity) / 1000)
    #         re.rotor_diameter_selection = rotor_diameter_words
    #         re.name_tur_selection = name_tur_selction_words

    # project_res= fields.Many2many('auto_word.windres', string=u'机位结果', required=True)

    @api.multi
    def button_wind(self):
        projectname = self.project_id
        myself = self
        projectname.wind_attachment_id = myself
        projectname.wind_attachment_ok = u"已提交,版本：" + self.version_id
        projectname.turbine_numbers = self.turbine_numbers
        projectname.select_hub_height = self.select_hub_height
        projectname.project_capacity = self.farm_capacity
        projectname.name_tur_selection = self.name_tur_selection

        return True

    @api.multi
    def wind_generate(self):
        tur_name = []
        for i in range(0, len(self.generator_ids)):
            tur_name.append(self.generator_ids[i].name_tur)
        path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\source\chapter_5"

        case_name_dict, name_tur_dict, turbine_numbers_dict, capacity_dict = [], [], [], []
        farm_capacity_dict, rotor_diameter_dict, tower_weight_dict = [], [], []
        case_hub_height_dict, power_generation_dict, weak_dict = [], [], []
        power_hours_dict, investment_dict, investment_unit_dict = [], [], []
        investment_E1_dict, investment_E2_dict, investment_E3_dict = [], [], []
        investment_E4_dict, investment_E5_dict, investment_E6_dict, investment_E7_dict = [], [], [], []
        investment_turbines_kws_dict = []
        for i in range(0, len(self.case_names)):
            case_name_dict.append(self.case_names[i].case_name)
            name_tur_dict.append('WTG' + str(int(i + 1)))
            turbine_numbers_dict.append(self.case_names[i].turbine_numbers)
            capacity_dict.append(self.case_names[i].capacity)
            farm_capacity_dict.append(self.case_names[i].farm_capacity)
            rotor_diameter_dict.append(self.case_names[i].rotor_diameter_case)
            case_hub_height_dict.append(self.case_names[i].case_hub_height)
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
        dict5 = doc_5.generate_wind_dict(tur_name, path_images)
        dict_5_word = {
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

            "叶轮直径": self.rotor_diameter_selection,
            "方案数": self.case_number,
            "海拔高程": self.farm_elevation,
            "区域面积": self.farm_area,
            "平均风速区间": self.farm_speed_range,
            '测风塔名字': self.cft_name_words,
            '测风塔风速信息': self.string_speed_words,
            '测风塔风向信息': self.string_deg_words,
            '推荐轮毂高度': self.select_hub_height,
            'IEC等级': self.IECLevel,
        }
        Dict5 = dict(dict_5_word, **dict5)
        print(Dict5)
        doc_5.generate_wind_docx(Dict5, path_images)
        ###########################

        reportfile_name = open(
            file=r'D:\GOdoo12_community\myaddons\auto_word\models\source\chapter_5\result_chapter5.docx',
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


# 机型比选
class auto_word_wind_turbines_compare(models.Model):
    # _inherit = 'auto_word.wind'
    _name = 'auto_word_wind_turbines.compare'
    _description = 'turbines_compare'
    _rec_name = 'case_name'
    # mixed_turbines_bool = fields.Boolean(string=u'是否为混排方案',help='若是混排方案请勾选')
    #
    case_name = fields.Char(u'方案名称', required=True, default="方案1")
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_ids = fields.Many2one('auto_word.wind', string=u'章节分类', required=True)
    power_generation = fields.Float(u'上网电量', default=1, required=True)
    weak = fields.Float(u'尾流衰减', required=True)
    power_hours = fields.Float(u'满发小时', required=True)
    TerrainType_turbines_compare = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("山地", u"山地")], string=u"山地类型", required=True)
    jidian_air_wind = fields.Float(u'架空长度', default=0, help='若不填写即采用电气集电线路')
    jidian_cable_wind = fields.Float(u'电缆长度', default=0, help='若不填写即采用电气集电线路')

    case_ids = fields.Many2many('wind_turbines.selection', string=u'比选方案')
    turbine_numbers = fields.Char(string=u'风机数量', readonly=True, compute='_compute_turbine', default="待提交")
    name_tur = fields.Char(string=u'风机类型', readonly=True, compute='_compute_turbine', default="待提交")
    capacity = fields.Char(string=u'风机容量', readonly=True, compute='_compute_turbine', default="待提交")
    farm_capacity = fields.Char(string=u'装机容量', readonly=True, compute='_compute_turbine', default="待提交")
    tower_weight = fields.Char(compute='_compute_turbine', string=u'塔筒重量', default="待提交")
    rotor_diameter_case = fields.Char(compute='_compute_turbine', string=u'叶轮直径', default="待提交")
    case_number = fields.Char(compute='_compute_turbine', string=u'方案数')

    investment_E1 = fields.Float(compute='_compute_turbine', string=u'塔筒投资(万元)')
    investment_E2 = fields.Float(compute='_compute_turbine', string=u'风机设备投资(万元)')
    investment_E3 = fields.Float(string=u'基础投资(万元)', required=True)
    investment_E4 = fields.Float(string=u'道路投资(万元)', readonly=True, compute='_compute_turbine')
    investment_E5 = fields.Float(string=u'吊装费用(万元)', readonly=True, compute='_compute_turbine')
    investment_E6 = fields.Float(string=u'箱变投资(万元)', readonly=True, compute='_compute_turbine')
    investment_E7 = fields.Float(string=u'集电线路(万元)', readonly=True, compute='_compute_turbine')

    investment_turbines_kws = fields.Char(u'风机kw投资', readonly=True, compute='_compute_turbine')
    case_hub_height = fields.Char(u'推荐轮毂高度', readonly=True, compute='_compute_turbine')

    investment = fields.Float(string=u'发电部分投资(万元)', readonly=True, compute='_compute_turbine')
    investment_unit = fields.Float(string=u'单位度电投资', readonly=True, compute='_compute_turbine')

    @api.depends('case_ids', 'TerrainType_turbines_compare')
    def _compute_turbine(self):

        investment_e1_sum, investment_e2_sum = 0, 0
        investment_e5_sum, investment_e6_sum = 0, 0
        for re in self:
            tower_weight_word, tower_weight_words = '', ''
            rotor_diameter_word, rotor_diameter_words = '', ''
            investment_turbines_kw_word, investment_turbines_kw_words = '', ''
            case_hub_height_word, case_hub_height_words, capacity_words = '', '', ''
            name_tur_words = ''
            re.case_number = str(len(re.case_ids))
            for i in range(0, len(re.case_ids)):

                if case_hub_height_word == str(re.case_ids[i].case_hub_height):
                    message_change = False
                else:
                    message_change = True

                tower_weight_word = str(re.case_ids[i].tower_weight)
                rotor_diameter_word = str(re.case_ids[i].rotor_diameter)
                investment_turbines_kw_word = str(re.case_ids[i].investment_turbines_kw)
                case_hub_height_word = str(re.case_ids[i].case_hub_height)
                capacity_word = str(re.case_ids[i].capacity)
                name_tur_word = str(re.case_ids[i].name_tur)

                re.turbine_numbers = int(re.case_ids[i].turbine_numbers) + int(re.turbine_numbers)
                re.farm_capacity = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) + int(
                    re.farm_capacity)
                investment_e1 = re.case_ids[i].tower_weight * re.case_ids[i].turbine_numbers * 1.05
                investment_e1_sum = investment_e1_sum + investment_e1

                investment_e2 = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) * int(
                    re.case_ids[i].investment_turbines_kw) / 10000
                investment_e2_sum = investment_e2_sum + investment_e2

                if re.case_ids[i].case_hub_height <= 90:
                    investment_e5 = re.case_ids[i].turbine_numbers * 38
                elif 90 < re.case_ids[i].case_hub_height <= 100:
                    investment_e5 = re.case_ids[i].turbine_numbers * 45
                elif 100 < re.case_ids[i].case_hub_height <= 120:
                    investment_e5 = re.case_ids[i].turbine_numbers * 55
                elif 120 < re.case_ids[i].case_hub_height <= 140:
                    investment_e5 = re.case_ids[i].turbine_numbers * 65

                if re.case_ids[i].capacity <= 2000:
                    investment_e6 = re.case_ids[i].turbine_numbers * 23
                elif 2000 < re.case_ids[i].capacity <= 2200:
                    investment_e6 = re.case_ids[i].turbine_numbers * 25
                elif 2200 < re.case_ids[i].capacity <= 2500:
                    investment_e6 = re.case_ids[i].turbine_numbers * 28
                elif 2500 < re.case_ids[i].capacity <= 4000:
                    investment_e6 = re.case_ids[i].turbine_numbers * 32

                investment_e5_sum = investment_e5_sum + investment_e5
                investment_e6_sum = investment_e6_sum + investment_e6
                if len(re.case_ids) > 1:
                    if i != len(re.case_ids) - 1:
                        tower_weight_words = tower_weight_word + "/" + tower_weight_words
                        rotor_diameter_words = rotor_diameter_word + "/" + rotor_diameter_words
                        investment_turbines_kw_words = investment_turbines_kw_word + "/" + investment_turbines_kw_words
                        name_tur_words = name_tur_word + "/" + name_tur_words
                        if message_change == True:
                            case_hub_height_words = case_hub_height_word + "/" + case_hub_height_words
                            capacity_words = capacity_word + "/" + capacity_words

                    else:
                        tower_weight_words = tower_weight_words + tower_weight_word
                        rotor_diameter_words = rotor_diameter_words + rotor_diameter_word
                        investment_turbines_kw_words = investment_turbines_kw_words + investment_turbines_kw_word
                        name_tur_words = name_tur_words + name_tur_word
                        if message_change == True:
                            case_hub_height_words = case_hub_height_words + case_hub_height_word
                            capacity_words = capacity_words + capacity_word

                if len(re.case_ids) == 1:
                    tower_weight_words = tower_weight_word
                    rotor_diameter_words = rotor_diameter_word
                    investment_turbines_kw_words = investment_turbines_kw_word
                    case_hub_height_words = case_hub_height_word
                    capacity_words = capacity_word
                    name_tur_words = name_tur_word

            re.name_tur = name_tur_words
            re.capacity = capacity_words
            re.tower_weight = tower_weight_words
            re.rotor_diameter_case = rotor_diameter_words
            re.investment_turbines_kws = investment_turbines_kw_words
            re.case_hub_height = case_hub_height_words

            re.farm_capacity = int(re.farm_capacity) / 1000
            re.investment_E1 = investment_e1_sum
            re.investment_E2 = investment_e2_sum

            if re.TerrainType_turbines_compare == "平原":
                re.investment_E4 = float(re.project_id.total_civil_length) * 50
            elif re.TerrainType_turbines_compare == "丘陵":
                re.investment_E4 = float(re.project_id.total_civil_length) * 80
            elif re.TerrainType_turbines_compare == "山地":
                re.investment_E4 = float(re.project_id.total_civil_length) * 140

            re.investment_E5 = investment_e5_sum
            re.investment_E6 = investment_e6_sum

            if re.jidian_air_wind == 0 and re.jidian_cable_wind == 0:
                re.investment_E7 = float(re.project_id.jidian_air_wind) * 40 + float(
                    re.project_id.jidian_cable_wind) * 50
            else:
                re.investment_E7 = float(re.jidian_air_wind) * 40 + float(re.jidian_cable_wind) * 50

            re.investment = RoundUp.round_up(re.investment_E1 + re.investment_E2 + re.investment_E3 + re.investment_E4 + \
                                             re.investment_E5 + re.investment_E6 + re.investment_E7)

            re.investment_unit = RoundUp.round_up(re.investment / re.power_generation * 10)

    def wind_turbines_compare_form_refresh(self):
        for re in self:
            re.content_ids.rotor_diameter_case = re.rotor_diameter_case
            re.content_ids.case_number = re.case_number
