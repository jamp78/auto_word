# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import doc_6
import base64,os
import global_dict as gl
from doc_8 import generate_civil_dict, generate_civil_docx, get_dict_8

class auto_word_electrical_infor(models.Model):
    _name = 'auto_word_electrical.infor'
    _description = 'electrical input infor'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")

    booster_station_construction_site = fields.Char(u'升压站建设地点')
    socio_economic_infor = fields.Char(u'社会经济概况')
    energy_development_plan = fields.Char(u'能源发展规划')
    power_system_development_plan = fields.Char(u'电力系统现状')
    engineering_construction_necessity = fields.Char(u'工程建设的必要性')
    project_electrical_description = fields.Char(u'项目电气描述')

    report_attachment_id = fields.Many2one('ir.attachment', string=u'工程任务和规模')

    # 提交
    dict_4_submit_word = fields.Char(u'字典4_提交')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    dict_5_submit_word = fields.Char(u'字典5_提交')


    def generate_electrical_infor(self):
        self.dict_1_submit_word = eval(self.project_id.dict_1_submit_word)
        self.dict_5_submit_word = eval(self.project_id.dict_5_submit_word)

        dict_4_word = {
            '升压站建设地点': self.booster_station_construction_site,
            '社会经济概况': self.socio_economic_infor,
            '能源发展规划': self.energy_development_plan,
            '电力系统现状': self.power_system_development_plan,
            '工程建设的必要性': self.engineering_construction_necessity,
            '项目电气描述': self.project_electrical_description,
        }

        self.dict_4_submit_word = dict_4_word

        dict_4_words = dict(dict_4_word, **eval(self.dict_1_submit_word), **eval(self.dict_5_submit_word))

        for key, value in dict_4_word.items():
            gl.set_value(key, value)

        path_chapter_6 = self.env['auto_word.project'].path_chapter_6
        generate_civil_docx(dict_4_words, path_chapter_6, 'cr4', 'result_chapter4')
        reportfile_name = open(
            file=os.path.join(path_chapter_6, '%s.docx') % 'result_chapter4',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告工程规模章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告工程规模章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告工程规模章节',
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


    def submit_electrical_infor(self):
        self.project_id.dict_4_submit_word = self.dict_4_submit_word
        return True


class auto_word_electrical(models.Model):
    _name = 'auto_word.electrical'
    _description = 'electrical input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告电气集电线路章节')

    # 提交
    dict_6_jidian_submit_word = fields.Char(u'字典6_jidian_提交')

    voltage_class = fields.Selection([(0, u"平原"), (1, u"山地")], string=u"地形", required=False)
    length_single_jL240 = fields.Float(u'单回线路长度（km）', required=False,default="25.3")
    length_double_jL240 = fields.Float(u'双回线路长度（km）', required=False,default="23.6")
    yjlv95 = fields.Float(u'直埋电缆YJLV22-26/35-3×95（km）', required=False,default="1.55")
    yjv300 = fields.Float(u'直埋电缆YJV22-26/35-1×300（km）', required=False,default="3")
    jidian_air_wind = fields.Float(u'架空长度', required=False)
    jidian_cable_wind = fields.Float(u'电缆长度', required=False,default="3.2")
    line_1 = fields.Float(u'线路总挖方', required=False,default="15000")
    line_2 = fields.Float(u'线路总填方', required=False,default="10000")
    overhead_line_num = fields.Float(u'架空线路塔基数量', required=False,default="20")
    direct_buried_cable_num = fields.Float(u'直埋电缆长度', required=False,default="3.2")

    #风能
    turbine_numbers = fields.Char(u'推荐机组数量', default="待提交", readonly=True)
    name_tur_suggestion = fields.Char(u'推荐机型', default="待提交", readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', default="待提交", readonly=True)
    circuit_number = fields.Integer(u'线路回路数', required=False,default="6")


    @api.multi
    def take_electrical_result(self):
        self.jidian_air_wind=self.length_single_jL240+self.length_double_jL240
        projectname = self.project_id
        self.turbine_numbers = projectname.turbine_numbers_suggestion
        self.name_tur_suggestion = projectname.name_tur_suggestion
        self.hub_height_suggestion = projectname.hub_height_suggestion

        if projectname.turbine_numbers_suggestion == "待提交":
            s = "风能部分"
            raise exceptions.Warning('请完成 %s，并点击 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

        args = [self.length_single_jL240, self.length_double_jL240, self.yjlv95, self.yjv300,
                int(self.turbine_numbers), self.circuit_number]
        dict6 = doc_6.generate_electrical_dict(self.voltage_class, args)

    #    挖方量每基铁塔按照140立方米，填方量按照每基100立方米，混凝土按照每基40立方米，钢筋按照每基0.8吨，
    #    地脚螺栓按照每基0.3吨

        self.line_1= float(dict6['铁塔合计'])*140
        self.line_2 = float(dict6['铁塔合计']) * 100

    @api.multi
    def electrical_generate(self):
        args = [self.length_single_jL240, self.length_double_jL240, self.yjlv95, self.yjv300,
                int(self.turbine_numbers), self.circuit_number]
        dict6=doc_6.generate_electrical_dict(self.voltage_class, args)
        dict_6_word = {
            # "机位数": self.turbine_numbers,
            "线路回路数": self.circuit_number,
            "电缆长度":self.jidian_cable_wind,
            "单回线路长度":self.length_single_jL240,
            "双回线路长度": self.length_double_jL240,

        }
        Dict6 = dict(dict_6_word, **dict6)
        self.dict_6_jidian_submit_word=Dict6

        path_chapter_6=self.env['auto_word.project'].path_chapter_6
        doc_6.generate_electrical_docx(Dict6, path_chapter_6)

        reportfile_name = open(
            file=os.path.join(path_chapter_6, '%s.docx') % 'result_chapter6',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告电气章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告电气章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告电气章节',
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
    def button_electrical(self):
        projectname = self.project_id
        myself = self
        projectname.electrical_attachment_id = myself
        projectname.electrical_attachment_ok = u"已提交,版本：" + self.version_id

        projectname.line_1 = self.line_1
        projectname.line_2 = self.line_2
        # projectname.overhead_line = self.overhead_line
        # projectname.direct_buried_cable = self.direct_buried_cable
        projectname.overhead_line_num = self.overhead_line_num
        projectname.direct_buried_cable_num = self.direct_buried_cable_num
        # projectname.main_booster_station_num = self.main_booster_station_num

        projectname.turbine_numbers = self.turbine_numbers
        projectname.voltage_class = self.voltage_class
        projectname.length_single_jL240 = self.length_single_jL240
        projectname.length_double_jL240 = self.length_double_jL240
        projectname.yjlv95 = self.yjlv95
        projectname.yjv300 = self.yjv300
        projectname.circuit_number = self.circuit_number

        projectname.jidian_air_wind = self.jidian_air_wind
        projectname.jidian_cable_wind = self.jidian_cable_wind

        projectname.dict_6_jidian_submit_word = self.dict_6_jidian_submit_word
        return True

    def electrical_refresh(self):
        projectname = self.project_id
        self.turbine_numbers = projectname.turbine_numbers_suggestion
        self.name_tur_suggestion = projectname.name_tur_suggestion
        self.hub_height_suggestion = projectname.hub_height_suggestion
