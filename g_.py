##  File to declare global variables and constants.

import ui_
import f_

gc_folder_path = "C:/Users/Anirban Saha/Documents/Python/"
gv_profile_config = 'master_profile_config'
gv_yes_en = 'yes'
gv_yes_de = 'ja'
gv_yes = ''
gv_no = ''
gv_null = ''
gv_english = 'en' #change101
gv_german = 'de'    #change101
gv_error_1 = 'E1'
gv_comma = ','
gv_lang_sel_text = 'Enter D to continue in German. To continue in English, press E'
gv_profile_fields = 'profile_fields.csv'
gv_append = 'a'
gv_encoding = 'utf-8'
gv_text_elements = 'texts.csv'
gv_read = 'r'
gv_write = 'w'
gc_newline = '\n'
gv_profile_path = 'profile/'
gv_format_csv = '.csv'
gv_chat_path = 'chat_rec/'
gc_no_en = 'no'
gc_no_de = 'nein'
gv_f_domain_syn = 'domain-synonyms.csv'
gv_f_stop_words = 'stop_words.txt'
gv_f_queries = 'queries.csv'
gv_space = ' '
gv_private = 'basic_operations_on_query'
gv_username = gv_null
gc_colon = ':'

gl_texts = []
gv_language = ui_.user_input(5)

gv_language = f_.set_g_language(gv_language)
gl_texts = f_.get_text_elements(gv_language)
gv_yes = f_.return_text(gv_yes_en)
gv_no = f_.return_text(gc_no_en)