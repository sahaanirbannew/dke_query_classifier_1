##  Methods that connect to the database.

#############################################################################
#   Reads from a file and returns the content in form of list.
#   Input: Path, Delimiter.
#   Output: a List.
#
#   Process:
#   Checks if file exists.
#   if yes -> read it.
#   if no -> create it. send error message in form of list.
#   Checks if delimiter exists.
#   if yes --> split it on delimiter
#   if no --> send the total content back.
#############################################################################

import g_


def read_file(path, delimiter):
    try:
        f = open(path, g_.gv_read, encoding=g_.gv_encoding)
    except:
        f = open(path, g_.gv_write, encoding=g_.gv_encoding)

    if delimiter != g_.gv_null:
        dump = f.read().split(delimiter)
        return dump
    else:
        return f.read()


#############################################################################
#   Writes to a file.
#   Input: String.
#   Output: Success Message.
#############################################################################

def write_file(path, content):
    try:
        f = open(path, g_.gv_append, encoding=g_.gv_encoding)
    except:
        f = open(path, g_.gv_write, encoding=g_.gv_encoding)

    f.write(content)
    f.close()
