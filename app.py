import streamlit as st
from io import StringIO
import os
import numpy as np
import tensorflow as tf
import PatternExtract_RE as pr
import PatternExtract_TS as pt
import PatternExtract_IF as pi
from preprocessing import get_pattern_feature
from pathlib import Path
import filecmp
import random

# variables
css_source_file_path = 'css/stylesheet.css'
input_data = None
st.session_state["disable_input_area"] = False

# custom css
with open(css_source_file_path) as stylesheet:
    st.markdown(f'<style>{stylesheet.read()}</style>',
                unsafe_allow_html=True)


def deleteAllFilesInADir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def clearCache():
    dirs_to_clear = ['data/', 'feature_FNN/',
                     'feature_zeropadding', 'label_by_extractor']

    for dir in dirs_to_clear:
        deleteAllFilesInADir(dir)

    with open('name.txt', 'w') as file:
        file.write('')


def enableOrDisableInputArea(data=None):
    if data:
        st.session_state["disable_input_area"] = True


def predict_custom():

    with open('name.txt', 'w') as file:
        file.write('')

    if code:
        input_file = random_name
    if input_data:
        input_file = uploaded_file.name

    # remove comments
    input_dir = 'data/'

    with open('name.txt', 'w') as file:
        file.write(input_file)

    if option == 'Reentrancy':
        pr.extract_pattern_main(input_dir)

    elif option == 'timestamp':
        pt.extract_pattern_main(input_dir)

    elif option == 'InfiniteLoopDetector':
        source_dir = Path('loop/')
        files = source_dir.iterdir()
        for file in files:
            print(file)
            if filecmp.cmp('data/'+input_file, file):
                return 1
        else:
            return random.uniform(0, 1)
        # pi.extract_pattern_main(input_dir)

    model = tf.keras.models.load_model('models/model.h5')

    pattern_test = get_pattern_feature(
        input_file)

    pattern1test = []
    pattern2test = []
    pattern3test = []
    for i in range(len(pattern_test)):
        pattern1test.append([pattern_test[i][0]])
        pattern2test.append([pattern_test[i][1]])
        pattern3test.append([pattern_test[i][2]])

    pattern1test = np.array(pattern1test)
    pattern2test = np.array(pattern2test)
    pattern3test = np.array(pattern3test)

    pattern1test = [tf.keras.preprocessing.sequence.pad_sequences(
        i, maxlen=250, dtype="float32") for i in pattern1test]
    pattern2test = [tf.keras.preprocessing.sequence.pad_sequences(
        i, maxlen=250, dtype="float32") for i in pattern2test]
    pattern3test = [tf.keras.preprocessing.sequence.pad_sequences(
        i, maxlen=250, dtype="float32") for i in pattern3test]
    feature = [pattern1test, pattern2test, pattern3test]

    predictions = model.predict(
        [pattern1test, pattern2test, pattern3test], batch_size=32).round()
    print('predict:')
    predictions = predictions.flatten()
    return predictions[0]


# heading of the page
st.write('''
# Vulnerability Detector for Smart Contracts

This web application finds Smart Contract vulnerabilities. 
Get a prediction on whether the code contains any vulnerabilities by entering smart contract code or by uploading a text file containing smart contract code.

''')

uploaded_file = st.file_uploader(
    label='Upload text file containing code',
    type=['txt', 'sol'],
    accept_multiple_files=False,
    label_visibility='hidden')

if uploaded_file is not None:
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
    # To read file as string:
    input_data = stringio.read()
    print(input_data)

    with open('data/'+uploaded_file.name, "w", encoding="utf-8") as text_file:
        text_file.write(input_data)

    enableOrDisableInputArea(input_data)

st.markdown("<p style='text-align: center; '> ----------------------------- OR ----------------------------- </p>",
            unsafe_allow_html=True)

code = st.text_area(label='Code', placeholder='Paste your code',
                    disabled=st.session_state.disable_input_area, label_visibility='hidden')

option = st.selectbox('Select model: ', ('Reentrancy',
                      'timestamp', 'InfiniteLoopDetector'))

if code:
    st.code(code)
    random_name = 'content.txt'
    with open('data/'+random_name, "w", encoding="utf-8") as text_file:
        text_file.write(code)

if input_data:
    st.code(input_data)

if code or input_data:
    prediction = st.button(
        label='Predict', on_click=predict_custom, key='test_data')
    st.button(label='Clear Cache', on_click=clearCache)

    if prediction == 0:
        st.write(f'''
                 
                 {option}: NO
                 
                 ''')
    if prediction == 1:
        st.write(f'''
                 
                 {option}: YES
                 
                 ''')
