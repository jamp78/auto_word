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

    cft_TI = fields.Char(string=u'湍流信息')
    cft_time = fields.Char(string=u'选取时间段')


class auto_word_wind_cft(models.Model):
    _name = 'auto_word_wind.cft'
    _description = 'Wind cft input'
    _rec_name = 'wind_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    wind_id = fields.Many2one('auto_word.wind', string=u'章节分类', required=True)
    version_id = fields.Char(u'版本', default="1.0")
    string_speed_words = fields.Char(string=u'测风塔风速', default="待提交", readonly=True)
    string_deg_words = fields.Char(string=u'测风塔风向', default="待提交", readonly=True)
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交", readonly=True)
    cft_number_words = fields.Char(string=u'测风塔数目', default="待提交", readonly=True)

    cft_TI_words = fields.Char(string=u'湍流信息', default="待提交", readonly=True)
    cft_time_words = fields.Char(string=u'选取时间段', default="待提交", readonly=True)

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

    # @api.depends('select_cft_ids')
    def compute_cft(self):
        for re in self:
            string_speed_words_final = ""
            string_deg_words_final = ""
            cft_name_words_final = ""
            string_cft_TI_words_final=""
            string_cft_time_words_final=""
            self.cft_number_words = len(re.select_cft_ids)
            for i in range(0, len(re.select_cft_ids)):
                re.cft_name = re.select_cft_ids[i].cft_name
                re.cft_height = re.select_cft_ids[i].cft_height
                re.cft_speed = re.select_cft_ids[i].cft_speed
                re.cft_pwd = re.select_cft_ids[i].cft_pwd
                re.cft_deg_main = re.select_cft_ids[i].cft_deg_main
                re.cft_deg_pwd_main = re.select_cft_ids[i].cft_deg_pwd_main

                re.cft_TI = re.select_cft_ids[i].cft_TI
                re.cft_time = re.select_cft_ids[i].cft_time

                string_speed_word = str(re.cft_name) + "测风塔" + str(re.cft_height) + "m高度年平均风速为" + str(re.cft_speed) + \
                                    "m/s,风功率密度为" + str(re.cft_pwd) + "W/m²。"
                string_speed_words_final = string_speed_word + string_speed_words_final

                string_deg_word = str(re.cft_name) + "测风塔" + str(re.cft_height) + "m测层风向" + str(re.cft_deg_main) + \
                                  "；主风能风向" + str(re.cft_deg_pwd_main) + "。"
                string_deg_words_final = string_deg_word + string_deg_words_final

                string_cft_TI_word = str(re.cft_name) + "测风塔" + str(re.cft_height) + "m测层代表湍流强度" + str(re.cft_TI) + "。"
                string_cft_TI_words_final = string_cft_TI_word + string_cft_TI_words_final

                string_cft_time_word = str(re.cft_name) + "测风塔" + str(re.cft_height) + "m选取" + str(re.cft_time) + "。"
                string_cft_time_words_final = string_cft_time_word + string_cft_time_words_final

                if i != len(re.select_cft_ids) - 1:
                    cft_name_words_final = re.cft_name + "/" + cft_name_words_final
                else:
                    cft_name_words_final = cft_name_words_final + re.cft_name

            re.cft_name_words = cft_name_words_final
            re.string_speed_words = string_speed_words_final
            re.string_deg_words = string_deg_words_final
            re.cft_TI_words = string_cft_TI_words_final
            re.cft_time_words = string_cft_time_words_final

        print('self.cft_time_words')
        print(self.cft_time_words)
    def button_cft(self):

        for re in self:
            re.project_id.string_speed_words = re.string_speed_words
            re.project_id.string_deg_words = re.string_deg_words
            re.project_id.select_turbine_ids = re.select_turbine_ids
            re.project_id.cft_name_words = re.cft_name_words
            re.project_id.name_tur_selection = re.name_tur_selection
            re.project_id.cft_number_words = re.cft_number_words

            re.env['auto_word.wind'].search([('project_id.project_name', '=',
                                              re.project_id.project_name)]).select_turbine_ids = re.select_turbine_ids

            # re.wind_id.select_turbine_ids=re.select_turbine_ids
            re.wind_id.cft_name_words = re.cft_name_words
            re.wind_id.string_speed_words = re.string_speed_words
            re.wind_id.string_deg_words = re.string_deg_words
            re.wind_id.cft_number_words = re.cft_number_words

            re.wind_id.cft_TI_words = re.cft_TI_words
            re.wind_id.cft_time_words = re.cft_time_words
            re.wind_id.Lat_words = re.project_id.Lat_words
            re.wind_id.Lon_words = re.project_id.Lon_words

        return True
