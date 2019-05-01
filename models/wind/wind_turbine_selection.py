# -*- coding: utf-8 -*-

from odoo import models, fields, api


class wind_cft_infor(models.Model):
    _name = 'wind_cft.infor'
    _description = 'Wind cft information input'
    _rec_name = 'cft_name'
    cft_name = fields.Char(string=u'测风塔')
    cft_height = fields.Integer(string=u'测风塔选定高程')
    cft_speed = fields.Float(string=u'风速')
    cft_pwd = fields.Integer(string=u'风功率密度')
    cft_deg_main = fields.Char(string=u'主风向')
    cft_deg_pwd_main = fields.Char(string=u'风能主风向')


class auto_word_wind_cft(models.Model):
    _name = 'auto_word_wind.cft'
    _description = 'Wind cft input'
    _rec_name = 'wind_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名')
    wind_id = fields.Many2one('auto_word.wind', string=u'章节分类')
    version_id = fields.Char(u'版本', default="1.0")
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', compute='_compute_cft')
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', compute='_compute_cft')
    cft_name_words = fields.Char(string=u'测风塔名字', compute='_compute_cft')
    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型')

    name_tur_selection = fields.Char(string=u'风机比选型号', readonly=True, default="待提交",
                                     compute='_compute_turbine_selection')
    select_cft_ids = fields.Many2many('wind_cft.infor', string=u'选定测风塔')

    @api.depends('select_turbine_ids')
    def _compute_turbine_selection(self):
        for re in self:
            name_tur_selection_words = ''

            for i in range(0, len(re.select_turbine_ids)):
                name_tur_selection_word = str(re.select_turbine_ids[i].name_tur)
                if len(re.select_turbine_ids) > 1:
                    if i != len(re.select_turbine_ids) - 1:
                        name_tur_selection_words = name_tur_selection_word + "/" + name_tur_selection_words
                    else:
                        name_tur_selection_words = name_tur_selection_words + name_tur_selection_word
                if len(re.select_turbine_ids) == 1:
                    name_tur_selection_words = name_tur_selection_word

            re.name_tur_selection = name_tur_selection_words
    @api.depends('select_cft_ids')
    def _compute_cft(self):
        string_speed_word = ""
        string_speed_words_final = ""

        string_deg_word = ""
        string_deg_words_final = ""
        cft_name_words_final = ""
        for i in range(0, len(self.select_cft_ids)):
            self.cft_name = self.select_cft_ids[i].cft_name
            self.cft_height = self.select_cft_ids[i].cft_height
            self.cft_speed = self.select_cft_ids[i].cft_speed
            self.cft_pwd = self.select_cft_ids[i].cft_pwd
            self.cft_deg_main = self.select_cft_ids[i].cft_deg_main
            self.cft_deg_pwd_main = self.select_cft_ids[i].cft_deg_pwd_main

            string_speed_word = str(self.cft_name) + "测风塔" + str(self.cft_height) + "m高度年平均风速为" + str(self.cft_speed) + \
                                "m/s,风功率密度为" + str(self.cft_pwd) + "W/m²。"
            string_speed_words_final = string_speed_word + string_speed_words_final

            string_deg_word = str(self.cft_name) + "测风塔" + str(self.cft_height) + "m测层风向" + str(self.cft_deg_main) + \
                              "；主风能风向" + str(self.cft_deg_pwd_main) + "。"
            string_deg_words_final = string_deg_word + string_deg_words_final
            if i != len(self.select_cft_ids)-1:
                cft_name_words_final = self.cft_name + "/" + cft_name_words_final
            else:
                cft_name_words_final = cft_name_words_final+self.cft_name

        self.cft_name_words = cft_name_words_final
        self.string_speed_words = string_speed_words_final
        self.string_deg_words = string_deg_words_final




    def button_cft(self):
        for re in self:
            re.wind_id.string_speed_words = re.string_speed_words
            re.wind_id.string_deg_words = re.string_deg_words
            re.wind_id.select_turbine_ids = re.select_turbine_ids
            re.wind_id.cft_name_words = re.cft_name_words
            re.wind_id.name_tur_selection = re.name_tur_selection

        return True