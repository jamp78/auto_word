# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import doc_5
from . import auto_word_electrical
from . import auto_word_civil


class wind_cft_infor(models.Model):
    _name = 'wind_cft.infor'
    _description = 'Wind cft information input'
    _rec_name = 'cft_name'
    cft_name = fields.Char(string=u'测风塔', required=True)
    cft_height = fields.Integer(string=u'测风塔选定高程', required=True)
    cft_speed = fields.Float(string=u'风速', required=True)
    cft_pwd = fields.Integer(string=u'风功率密度', required=True)
    cft_deg_main = fields.Char(string=u'主风向', required=True)
    cft_deg_pwd_main = fields.Char(string=u'风能主风向', required=True)


class auto_word_wind_cft(models.Model):
    _name = 'auto_word_wind.cft'
    _description = 'Wind cft input'
    _rec_name = 'wind_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名')
    wind_id = fields.Many2one('auto_word.wind', string=u'风资源', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', compute='_compute_cft')
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', compute='_compute_cft')
    cft_name_words = fields.Char(string=u'测风塔名字', compute='_compute_cft')
    generator_ids = fields.Many2many('auto_word_wind.turbines', required=True, string=u'比选机型')

    # cft_height = fields.Char(string=u'选定高程', readonly=True, compute='_compute_cft')
    # cft_speed = fields.Char(string=u'风速', readonly=True, compute='_compute_cft')
    # cft_pwd = fields.Char(string=u'风功率密度', readonly=True, compute='_compute_cft')
    # cft_deg_main = fields.Char(string=u'主风向', readonly=True, compute='_compute_cft')

    #     # generator_ids = fields.Many2many('auto_word_wind.turbines', required=True, string=u'比选机型')
    select_cft_ids = fields.Many2many('wind_cft.infor', required=True, string=u'选定测风塔')

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
            cft_name_words_final = self.cft_name + "  " + cft_name_words_final

        self.cft_name_words = cft_name_words_final
        self.string_speed_words = string_speed_words_final
        self.string_deg_words = string_deg_words_final

    def button_cft(self):
        for re in self:
            print(re.wind_id.string_speed_words)
            re.wind_id.string_speed_words = re.string_speed_words
            re.wind_id.string_deg_words = re.string_deg_words
            re.wind_id.generator_ids = re.generator_ids
            re.wind_id.cft_name_words = re.cft_name_words
        return True
