import os
import time

from flask import Flask, request, flash, redirect, render_template, send_from_directory
from mp3stego import Steganography
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.getcwd() + '/uploads')
ALLOWED_EXTENSIONS = {'mp3'}

FUNC_NAME_TO_TAB_NUM = {
    'decode': 1,
    'encode': 2,
    'hide': 3,
    'reveal': 4,
    'clear': 5,
}

TAB_ID_TO_TAB_NUM = {
    'home-tab': 0,
    'decode-tab': 1,
    'encode-tab': 2,
    'hide-tab': 3,
    'reveal-tab': 4,
    'clear-tab': 5,
    'lib-tab': 6,
    'about-tab': 7,
}

is_uploads_exist = os.path.exists(UPLOAD_FOLDER)

if not is_uploads_exist:
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

s = Steganography()

already_used_files = []


def get_path_with_rnd(file_name: str):
    dot_index = file_name.rfind('.')
    file_name = file_name[:dot_index] + '_' + str(hex(int(time.time()))[2:]) + file_name[dot_index:]
    return file_name


def get_full_path(file_name: str):
    return os.path.join(app.config['UPLOAD_FOLDER'], file_name)


def hide_msg(input_file_name, msg):
    output_file_path = get_path_with_rnd('output.mp3')
    too_long = s.hide_message(get_full_path(input_file_name), get_full_path(output_file_path), msg)
    return output_file_path, too_long


def reveal_msg(input_file_name, _):
    output_file_path = get_path_with_rnd('reveal.txt')
    s.reveal_massage(get_full_path(input_file_name), get_full_path(output_file_path))
    return output_file_path, None


def clear_file(input_file_name, _):
    output_file_path = get_path_with_rnd('cleared_file.mp3')
    s.clear_file(get_full_path(input_file_name), get_full_path(output_file_path))
    return output_file_path, None


def wav_to_mp3(input_file_name, bitrate):
    output_file_path = get_path_with_rnd('output.mp3')
    try:
        bitrate = int(bitrate)
    except:
        bitrate = 320
    bitrate = bitrate if bitrate < 1000 else bitrate // 1000
    s.encode_wav_to_mp3(get_full_path(input_file_name), get_full_path(output_file_path), bitrate)
    return output_file_path, None


def mp3_to_wav(input_file_name, _):
    output_file_path = get_path_with_rnd('output.wav')
    s.decode_mp3_to_wav(get_full_path(input_file_name), get_full_path(output_file_path))
    return output_file_path, None


funcs = {
    'hide': hide_msg,
    'reveal': reveal_msg,
    'clear': clear_file,
    'encode': wav_to_mp3,
    'decode': mp3_to_wav
}


def allowed_file(filename, func_name):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) or (
        filename.rsplit('.', 1)[1].lower() == "wav" if func_name == 'encode' else False)


def upload_file(func_name):
    # check if the post request has the file part
    if 'file-mp3' not in request.files:
        flash('No file part')
        return redirect(f'/#tab{FUNC_NAME_TO_TAB_NUM[func_name]}')
    file = request.files['file-mp3']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return render_template('index.html', curr_tab=FUNC_NAME_TO_TAB_NUM[func_name],
                               text_error='FILE UPLOAD ERROR - You must upload file for using the website functions')
    if file and allowed_file(file.filename, func_name):
        filename = secure_filename(file.filename)
        file.save(get_full_path(filename))

        func = funcs[func_name]

        warning_txt = ''
        try:
            message = ''
            if func_name == 'hide':
                if 'file-txt' not in request.files:
                    flash('No file part')
                    return redirect(f'/#tab{FUNC_NAME_TO_TAB_NUM[func_name]}')
                txt_file = request.files['file-txt']
                if txt_file.filename == '':
                    return render_template('index.html', curr_tab=FUNC_NAME_TO_TAB_NUM[func_name],
                                           text_error='FILE UPLOAD ERROR - You must upload TXT file for using the '
                                                      'hiding function')
                if '.' in txt_file.filename and (txt_file.filename.rsplit('.', 1)[1].lower() == 'txt'):
                    pass
                else:
                    return render_template('index.html', curr_tab=FUNC_NAME_TO_TAB_NUM[func_name],
                                           text_error='FILE DOESN\'T MATCH - You must upload TXT file for using the '
                                                      'hiding function')
                txt_filename = secure_filename(txt_file.filename)
                txt_file.save(get_full_path(txt_filename))

                with open(get_full_path(txt_filename)) as f:
                    message = f.read()

            file_name, too_long = func(filename, message if func_name == 'hide' else request.form.get('bitrate'))
            if func_name == 'hide' and too_long:
                warning_txt = 'Note: your message is too long for this MP3 file, it has been cut'

        except BaseException as err:
            return render_template('index.html', curr_tab=FUNC_NAME_TO_TAB_NUM[func_name],
                                   text_error='ERROR ON SERVER - ' + str(err))
        already_used_files.append(get_full_path(filename))
        return render_template('index.html', file_path=file_name, display_download=True, text_error=warning_txt)

    return render_template('index.html', curr_tab=FUNC_NAME_TO_TAB_NUM[func_name],
                           text_error='FILE DOESN\'T MATCH - You must upload file that matches the instruction for '
                                      'using the website functions')


@app.route('/', methods=['POST'])
def form_handler():
    func_name = request.form['submit']
    return upload_file(func_name)


@app.route('/', methods=['GET'])
def load_home_page():
    return render_template('index.html', file_path='', display_download=False, curr_tab=0)


@app.route('/download/<file_path>', methods=['GET'])
def download(file_path):
    already_used_files.append(get_full_path(file_path))
    return send_from_directory(app.config["UPLOAD_FOLDER"], file_path, as_attachment=True)


def delete_all_used_files():
    current_used_files = already_used_files.copy()
    for file in current_used_files:
        if os.path.exists(file):
            os.remove(file)
            already_used_files.remove(file)


def delete_all_files():
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(get_full_path(f))


@app.route('/reset/<tab_name>')
def reset(tab_name):
    delete_all_used_files()
    tab_num = TAB_ID_TO_TAB_NUM[tab_name]
    return redirect(f'/#tab{tab_num}')


if __name__ == '__main__':
    delete_all_files()
    app.run(debug=True)
