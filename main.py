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
# current Bugs:
# #1: Profile Config file does not save properly. Arrangement needs to change.
#########################################################


import g_                       #Global Constants, variable & Input Output
import f_                       #General Functions
import ui_


def main():
    # Initiate conversation
    converse = ui_.user_input(1)

    # Greet the person.
    f_.send_greetings()

    # if the user has sent a message which is more than just a greetings.
    its_just_greetings = f_.is_greetings(converse)
    if its_just_greetings == 0:  # no it has message / query in it.
        f_.chat(converse, g_.gv_null)


if __name__ == '__main__':
    main()
