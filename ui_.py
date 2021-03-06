#############################################################################
##  About: File to write the User Input and Output
##
##  Developer: Anirban Saha & Madhu Thatikonda
##  Version: 0.1 (Draft)
#############################################################################

import g_
import f_
from googletrans import Translator  # change_01


#############################################################################
## user_input takes the input from the user.
## Input:   text ID: Text in the language set by the user, asking for input.
## Output:  User's response to the calling function.
#############################################################################


def user_input(txt_id):
    # print("Text ID: " + str(txt_id))
    text = g_.gv_null
    if str(txt_id) == '5':
        text = g_.gv_lang_sel_text

    else:
        for row in g_.gl_texts:
            t_id = row.split(g_.gv_comma)[0]
            if t_id == str(txt_id):
                text = row.split(g_.gv_comma)[1]
        if text == g_.gv_null:
            sys_response(g_.gv_error_1)
    response = input(text)
    response = f_.basic_operations_on_query(response)
    return response


#############################################################################
#  Gives the systems response to the user based on a text ID.
#  Input:  text ID
#  Output: Shows to the user, the message.
#############################################################################


def sys_response(txt_id):
    text = g_.gv_null

    for row in g_.gl_texts:
        t_id = row.split(g_.gv_comma)[0]
        if t_id == str(txt_id):
            text = row.split(g_.gv_comma)[1]
    print(text)

    if text == g_.gv_null:
        sys_response(g_.gv_error_1)
        exit()


#############################################################################
#  Gives the systems long response to the user.
#  It is not based on the Text ID.
#  Input:  Message text
#  Output:
#       If global language is English:
#           Shows to the user the message.
#       Else:
#           translates the text and shows to the user.
#############################################################################
#   Date:               Change by:          Status:         Tracking code:
#   11.03.2019          Anirban             Sign off        N.A.
#   14.03.2019          Anirban             Sign off        #change_01
#############################################################################


def sys_long_response(text):
    if text == g_.gv_null:
        sys_response(g_.gv_error_1)
        exit()
# change_01: Begin of change.
    if g_.gv_language != g_.gv_english:
        translator = Translator()
        text = translator.translate(text, dest=g_.gv_language)
        text = text.text
# change_01: End of change.
    print(text)


#############################################################################
##  Gives the systems long response to the user based on Text ID and a value
##  Input:  text ID and a value.
##  Output: Shows the user the text and the value.
#############################################################################

def sys_com_response(txt_id, value):
    text = g_.gv_null
    for row in g_.gl_texts:
        t_id = row.split(g_.gv_comma)[0]
        if t_id == str(txt_id):
            text = row.split(g_.gv_comma)[1]
            print(text + value)
    if text == g_.gv_null:
        sys_response(g_.gv_error_1)
        exit()
