# -*- coding: utf-8 -*-

from odoo import models, fields, api
import sys
sys.path.append(r'D:\GOdoo12_community\myaddons\auto_word\models\electrical')
import doc_6
import base64


class auto_word_electrical(models.Model):
    path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\electrical\chapter_6"
    _name = 'auto_word.electrical'
    _description = 'electrical input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    voltage_class = fields.Selection([(0, u"平原"), (1, u"山地")], string=u"地形", required=False)
    length_single_jL240 = fields.Float(u'单回线路JL/G1A-240/30长度（km）', required=False,default="19")
    length_double_jL240 = fields.Float(u'双回线路JL/G1A-240/30长度（km）', required=False,default="22")
    yjlv95 = fields.Float(u'直埋电缆YJLV22-26/35-3×95（km）', required=False,default="8")
    yjv300 = fields.Float(u'直埋电缆YJV22-26/35-1×300（km）', required=False,default="1.5")

    turbine_numbers = fields.Char(u'机位数', default="待提交", readonly=True)
    name_tur_suggestion = fields.Char(u'推荐机型', default="待提交", readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', default="待提交", readonly=True)

    circuit_number = fields.Integer(u'线路回路数', required=False,default="6")
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告电气章节')

    line_1 = fields.Float(u'线路总挖方', required=False,default="15000")
    line_2 = fields.Float(u'线路总填方', required=False,default="10000")
    overhead_line = fields.Float(u'架空线路用地', required=False,default="1500")
    direct_buried_cable = fields.Float(u'直埋电缆用地', required=False,default="3000")
    overhead_line_num = fields.Float(u'架空线路塔基数量', required=False,default="20")
    direct_buried_cable_num = fields.Float(u'直埋电缆长度', required=False,default="3.2")
    main_booster_station_num = fields.Float(u'主变数量', required=False,default="2.0")

    #风能
    jidian_air_wind = fields.Float(u'架空长度', required=False,default="74.2")
    jidian_cable_wind = fields.Float(u'电缆长度', required=False,default="3.2")


    # @api.depends('length_singlejL240', 'length_doublejL240')
    # def _compute_total_length(self):
    #     for re in self:
    #         re.total_length = re.length_singlejL240 + re.length_doublejL240 * 2

    @api.multi
    def electrical_generate(self):
        args = [self.length_single_jL240, self.length_double_jL240, self.yjlv95, self.yjv300,
                int(self.turbine_numbers), self.circuit_number]
        dict6=doc_6.generate_electrical_dict(self.voltage_class, args)
        dict_6_word = {
            "机位数": self.turbine_numbers,
        }
        Dict6 = dict(dict_6_word, **dict6)
        print(Dict6)
        doc_6.generate_electrical_docx(Dict6, self.path_images)
        reportfile_name = open(
            file=r'D:\GOdoo12_community\myaddons\auto_word\models\electrical\chapter_6\result_chapter6.docx',
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
        projectname.overhead_line = self.overhead_line
        projectname.direct_buried_cable = self.direct_buried_cable
        projectname.overhead_line_num = self.overhead_line_num
        projectname.direct_buried_cable_num = self.direct_buried_cable_num
        projectname.main_booster_station_num = self.main_booster_station_num

        projectname.turbine_numbers = self.turbine_numbers
        projectname.voltage_class = self.voltage_class
        projectname.length_single_jL240 = self.length_single_jL240
        projectname.length_double_jL240 = self.length_double_jL240
        projectname.yjlv95 = self.yjlv95
        projectname.yjv300 = self.yjv300
        projectname.circuit_number = self.circuit_number

        projectname.jidian_air_wind = self.jidian_air_wind
        projectname.jidian_cable_wind = self.jidian_cable_wind

        return True

    def electrical_refresh(self):
        projectname = self.project_id
        self.turbine_numbers = projectname.turbine_numbers_suggestion
        self.name_tur_suggestion = projectname.name_tur_suggestion
        self.hub_height_suggestion = projectname.hub_height_suggestion
