## File to write method definitions.

import datetime
import glob
import re

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB

import db_
import g_
import ui_

lv_f_queries = "queries.csv"
lv_null = 'null'


#############################################################################
#
#############################################################################


def return_text(id):
    for row in g_.gl_texts:
        row_elements = row.split(g_.gv_comma)
        t_id = row_elements[0]
        if t_id == id:
            return row.split(g_.gv_comma)[1]


#############################################################################
##
#############################################################################


def set_g_language(input):
    g_.gv_language = input.upper()
    if g_.gv_language == g_.gv_english or g_.gv_language == 'english':
        return g_.gv_english
    elif g_.gv_language == g_.gv_german or g_.gv_language == 'german' or g_.gv_language == 'deutsch':
        return g_.gv_german
    else:
        return g_.gv_english


#############################################################################
##
#############################################################################


def get_text_elements(gv_language):
    if gv_language != g_.gv_english and gv_language != g_.gv_german:
        gv_language = g_.gv_english

    gl_texts_dump = db_.read_file(g_.gc_folder_path + g_.gv_text_elements, g_.gc_newline)  # DB
    gl_texts = []

    for text_element in gl_texts_dump:
        elements = text_element.split(g_.gv_comma)
        if elements[1] == gv_language:
            if elements[2] == g_.gv_yes_en:
                g_.gv_yes = elements[3]
            if elements[2] == g_.gc_no_en:
                g_.gv_no = elements[3]
            gl_texts.append(elements[2] + g_.gv_comma + elements[3])
            elements.clear()
    gl_texts.sort()
    return gl_texts


#############################################################################
##
#############################################################################

def find_text_from_id(id):
    text = g_.gv_null
    for row in g_.gl_texts:
        t_id = row.split(g_.gv_comma)[0]
        if t_id == str(t_id):
            text = row.split(g_.gv_comma)[1]
    if text == g_.gv_null:
        ui_.sys_response(g_.gv_error_1)


#############################################################################
##
#############################################################################


def chat(queries, username):
    query = queries.split(g_.gc_newline)
    t_id = str(datetime.datetime.now())
    count = 1

    if username == g_.gv_null:

        username = ui_.user_input(2)  # Asks for the name
        user_exist = user_exists(username)  # Checks if the person exists

        if user_exist == 0:
            ui_.sys_response(12)  # User Exists

            consent = ui_.user_input(14)
            if consent == g_.gv_yes:
                sim_user = fin_sim_user(username)
                ui_.sys_com_response(15, sim_user)
            chat(queries, username)
        else:  # User Does not exist.
            consent = ui_.user_input(6)  # Do you want to create now?
            if consent == g_.gv_yes:
                make_profile(username)

            elif consent == g_.gv_no:
                username = g_.gv_private
            chat(queries, username)

    for a_query in query:
        wordcount_query = a_query.split(' ')
        if len(wordcount_query) > 0:
            # a_query = basic_operations_on_query(a_query)
            label = get_label(a_query)

            if label == 'similarity':  # Delete
                ui_.sys_com_response(15, fin_sim_user(username))

            response = get_response(label)
            ui_.sys_long_response(response)
            feedback = ui_.user_input(7)
            if feedback == g_.gv_no:
                label = ui_.user_input(8)
            db_.write_file(g_.gc_folder_path + lv_f_queries,
                           g_.gc_newline + t_id + g_.gv_comma + a_query + g_.gv_comma + label + g_.gv_comma + feedback)

    queries = ui_.user_input(9)
    if queries == g_.gv_yes:
        queries = ui_.user_input(11)
        chat(queries, username)
    elif queries == g_.gv_no:
        ui_.sys_response(10)
        exit()
    if len(queries) > 0:
        chat(queries, username)


#############################################################################
##
#############################################################################


def user_exists(username):
    all_content = db_.read_file(g_.gc_folder_path + g_.gv_profile_path + g_.gv_profile_config + g_.gv_format_csv,
                                g_.gc_newline)

    for line in all_content:
        if username == line.split(g_.gv_comma)[0]:
            return 0  # Exists

    return 1


#############################################################################
##
#############################################################################


def basic_operations_on_query(query):
    query = re.sub(r"[^a-zA-Z0-9]+", ' ', query)  # Removing special characters
    query = query.strip()  # Removing end white spaces
    # Checking if users words need to be replaced with official words.

    domain_synonym_corpus_list = db_.read_file(g_.gc_folder_path + g_.gv_f_domain_syn, g_.gc_newline)

    # Using domain specific keywords
    for line in domain_synonym_corpus_list:
        line_str = line.split(g_.gv_comma)
        if line_str[0] in query:
            query = query.replace(line_str[0], line_str[1] + ' ')

    # Removing the stop words.
    stop_words = db_.read_file(g_.gc_folder_path + g_.gv_f_stop_words, g_.gc_newline)
    word_list_query = query.split(g_.gv_space)

    for word in word_list_query:
        if word in stop_words:
            word = g_.gv_space + word + g_.gv_space
            query = query.replace(word, g_.gv_space)

    query = g_.gv_space.join(query.split())
    return query


#############################################################################
##
#############################################################################


def make_profile(matr):
    lv_text_elements_profile = 'profile_elements'
    lv_profile_pref = 'profile_'
    lv_chat_file_pref = 'chat_rec_'
    lv_yes = ',yes'
    lv_q_username = 'username'
    lv_q_chat_rec = 'chat_rec'
    lv_q_help_others = 'help_oth'
    lv_q_allow_chat = 'allow_chat'

    all_rel_questions = []
    profile_inf = []

    # Getting the Questions from the table.
    all_questions = db_.read_file(g_.gc_folder_path + g_.gv_text_elements, g_.gc_newline)
    all_questions.sort()

    # Finding the Questions to ask.

    for sentence in all_questions:
        sentence_str = sentence.split(g_.gv_comma)
        if sentence_str[0] == lv_text_elements_profile and sentence_str[1] == g_.gv_language:
            all_rel_questions.append(sentence_str[2] + g_.gv_comma + sentence_str[3])

    #Creates the file for profile.
    for q in all_rel_questions:
        question_elements = q.split(g_.gv_comma)
        field_name = question_elements[0]
        field_val = ui_.user_input(field_name)
        db_.write_file(g_.gc_folder_path + g_.gv_profile_path + lv_profile_pref + matr + g_.gv_format_csv,
                       field_name + g_.gv_comma + field_val + g_.gc_newline)
        profile_inf.append(field_name + g_.gv_comma + field_val)


    # Update Master Profile Config
    update_info_profile_config = ''
    for profile_element in profile_inf:
        profile_element_arr = profile_element.split(',')
        if profile_element_arr[0] == lv_q_username:
            update_info_profile_config = update_info_profile_config + g_.gv_comma + profile_element_arr[1]  # Matr
            update_info_profile_config = update_info_profile_config + lv_yes  # ProfileActive: Yes
        elif profile_element_arr[0] == lv_q_chat_rec:
            update_info_profile_config = update_info_profile_config + g_.gv_comma + profile_element_arr[1]
        elif profile_element_arr[0] == lv_q_help_others:
            update_info_profile_config = update_info_profile_config + g_.gv_comma + profile_element_arr[1] \
                                     + lv_yes + lv_yes + lv_yes
        elif profile_element_arr[0] == lv_q_allow_chat:
            update_info_profile_config = update_info_profile_config + g_.gv_comma + \
                                     profile_element_arr[1] + lv_yes + lv_yes + lv_yes + lv_yes
        print(update_info_profile_config)
    db_.write_file(g_.gc_folder_path + g_.gv_profile_path + g_.gv_profile_config + g_.gv_format_csv, g_.gc_newline + update_info_profile_config)

    db_.write_file(g_.gc_folder_path + g_.gv_chat_path + lv_chat_file_pref + matr + g_.gv_format_csv, 'chat record')
    return matr


#############################################################################
##
#############################################################################


def get_response(label):
    return label


#############################################################################
#  It takes a query.
#  Retrains the system with all queries
#  Returns the class label.
#
#  Developer: Madhu K R Thatikonda.
#  Changes to make:
#      - it should train once.
#      - It should return more than one class label, based on a threshold
#          probability
#############################################################################

def get_label(query):
    # Training the model.
    vectorizer = CountVectorizer(decode_error='ignore', strip_accents='unicode', stop_words='english',
                                 ngram_range=(2, 3))
    list_of_queries = []
    list_of_labels = []
    list_new_query = []

    one_question = db_.read_file(g_.gc_folder_path + g_.gv_f_queries, g_.gc_newline)

    for question in one_question:
        line_format = question.split(g_.gv_comma)
        try:
            question_text = line_format[1]
            list_of_queries.append(question_text)
            list_of_labels.append(line_format[2])
        except:
            ui_.sys_response(lv_null)

    list_new_query.append(query)

    len_list_of_queries = len(list_of_queries)
    vectorizer.fit(list_of_queries)
    vectors = vectorizer.transform(list_of_queries)
    vectors_test = vectorizer.transform(list_new_query)

    vectorised = vectors.toarray()
    vectorised_test = vectors_test.toarray()
    classifier = MultinomialNB()
    classifier.fit(vectorised, list_of_labels)
    classifier.predict(vectorised_test)

    label = classifier.predict(vectorised_test)[0]

    return label


#############################################################################
##
#############################################################################


def fin_sim_user(person):
    # path_folder = input("Enter the path to the folder:   ")
    path_file_1 = g_.gc_folder_path + g_.gv_profile_path + 'profile_' + person + '.csv'
    path_folder = g_.gc_folder_path + g_.gv_profile_path
    most_similar = simi(path_file_1, path_folder)
    # most_similar = str(most_similar).replace('profile_', g_.gv_null).replace(g_.gv_format_csv, g_.gv_null)
    return most_similar[8:-4]


#############################################################################
##
#############################################################################


def simi(path_file_1, path_file_2):
    list_A = []
    list_folder = []
    list_result = []

    folder = glob.glob1(path_file_2, '*' + g_.gv_format_csv)
    # print(folder)

    for file in folder:
        if file == g_.gv_profile_config + g_.gv_format_csv:
            print(g_.gv_space)
        elif g_.gc_folder_path + g_.gv_profile_path + file != path_file_1:
            list_result.append(file)
            file_content = db_.read_file(g_.gc_folder_path + g_.gv_profile_path + file, g_.gv_null)
            list_folder.append(file_content)
            # print(list_folder)
        else:
            file_content = db_.read_file(g_.gc_folder_path + g_.gv_profile_path + file, g_.gv_null)
            list_A.append(file_content)

    vectorizer = TfidfVectorizer(decode_error='ignore', strip_accents='unicode', stop_words='english',
                                 ngram_range=(1, 1))
    vectorizer.fit(list_folder)
    vectors = vectorizer.transform(list_A).toarray()
    vectors2 = vectorizer.transform(list_folder).toarray()
    s = cosine_similarity(vectors, vectors2)
    max_index = np.argmax(s)
    # print(list_result[max_index])
    return list_result[max_index]
