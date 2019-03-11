#########################################################
# Messenger chat texts classifier
# Input: Chat Text
# Output: Response with a link.
# Date: 08.03.2019
# Developers:
#   Package Implementation: Madhu Kiran Reddy Thatikonda
#   Solution Architecture: Anirban Saha
# Version: 0.3 (Draft)
#########################################################

import g_                       #Global Constants, variable & Input Output
import f_                       #General Functions
import ui_


def main():
    # Initiate conversation
    converse = ui_.user_input(1)
    convo = converse.split(g_.gv_space)

    # If there are more than two words, then we are good.
    if len(convo) > 2:
        f_.chat(converse, g_.gv_null)
    else:
        # else we ask the person to be slightly more elaborate
        ui_.sys_response(13)
        f_.chat(g_.gv_space, g_.gv_null)


if __name__ == '__main__':
    main()
