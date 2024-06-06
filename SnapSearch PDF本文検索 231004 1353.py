# coding: shift-jis
# ------------------------------------------------------------
# PDF�t�@�C���̒��g��and��������v���O���� Snap Search
# 2023-OCT-04 Wed.
# This program "Snap Search" was developed with the assistance of ChatGPT. ���̃v���O�����uSnap Search�v�́AChatGPT�̏��͂ɂ���ĊJ�����ꂽ�B
# Copyright (c) 2023 NAGATA Mizuho, �i�c �݂���. Institute of Laser Engineering, Osaka University.
# ------------------------------------------------------------
import os
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime  # datetime���W���[�����C���|�[�g

def search_pdf():
    # �_�C�A���O�{�b�N�X��\�����ăf�B���N�g����I��
    selected_directory = filedialog.askdirectory(title="�����������f�B���N�g����I��") # �_�C�A���O�{�b�N�X�̃^�C�g����ݒ�

    # ���͂��ꂽ�L�[���[�h���擾
    search_keywords = keyword_entry.get().split()  # �X�y�[�X�ŃL�[���[�h�𕪊�

    # and�����`�F�b�N�{�b�N�X�̏�Ԃ��擾
    and_search = and_checkbox_var.get()

    # �������ʂ�ۑ����郊�X�g
    search_results = []

    # �f�B���N�g������PDF�t�@�C��������
    for root, _, files in os.walk(selected_directory):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_file_path = os.path.join(root, filename)

                # PDF�t�@�C�����J��
                pdf_reader = PdfReader(pdf_file_path)

                # �e�y�[�W������
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()

                    # and����: ���ׂẴL�[���[�h���܂܂�Ă��邩�`�F�b�N
                if and_search:
                    if all(keyword in page_text for keyword in search_keywords):
                        # �������ʂɃL�[���[�h���ǉ�
                        search_results.append((filename, pdf_file_path, search_keywords))
                        continue  # ���̃y�[�W�̓`�F�b�N�s�v
                # or����: �ǂꂩ��̃L�[���[�h���܂܂�Ă��邩�`�F�b�N
                else:
                    if any(keyword in page_text for keyword in search_keywords):
                        # �������ʂɃL�[���[�h���ǉ�
                        search_results.append((filename, pdf_file_path, search_keywords))


    # ���݂̓��t�Ǝ������擾
    current_datetime = datetime.now()

    # ���݂̓��t�Ǝ������t�H�[�}�b�g
    date_time_str = current_datetime.strftime("%Y%m%d_%H%M%S")

    # ��������CSV�t�@�C���ւ̃p�X�i���ݎ������܂ށj
    csv_file_path = f'search_results_{date_time_str}.csv'

    # CSV�t�@�C���Ɍ������ʂ���������
    with open(csv_file_path, 'w', newline='', encoding='shift-jis') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['�t�@�C����', '�ꏊ', '�L�[���[�h'])

        for filename, location, keywords in search_results:
            csv_writer.writerow([filename, location, ', '.join(keywords)])

    # �������ʕ\���p�̃E�B���h�E���쐬
    result_window = tk.Toplevel(window)
    result_window.title('PDF�{����������')

    if not search_results:
        # �������ʂ��Ȃ��ꍇ�̃��x��
        result_label = tk.Label(result_window, text='�L�[���[�h��������܂���ł���')
        result_label.pack()
    else:
        # �������ʂ�\��
        result_label = tk.Label(result_window, text='�L�[���[�h����������PDF�t�@�C��:')
        result_label.pack()

    # �������ʂ̃t�@�C�����A�ꏊ�A����уL�[���[�h��\��
    for filename, location, keywords in search_results:
        keyword_str = ', '.join(keywords)
        result_text = f'�t�@�C����: {filename}, �ꏊ: {location}, �L�[���[�h: {keyword_str}'
        result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 14))
        result_label.pack()

# GUI�E�B���h�E���쐬
window = tk.Tk()
window.title('PDF�{������ Snap Search')

# �E�B���h�E�̃T�C�Y��ύX����
window.geometry("400x200")  # ��400�s�N�Z���A����200�s�N�Z��

# �L�[���[�h���͗�
keyword_label = tk.Label(window, text='�����L�[���[�h (�X�y�[�X�ŋ�؂��ē���):', font=("Helvetica", 14))
keyword_label.pack()
keyword_entry = tk.Entry(window, font=("Helvetica", 14))
keyword_entry.pack()

# and�����`�F�b�N�{�b�N�X (�ŏ�����`�F�b�N���ꂽ���)
and_checkbox_var = tk.BooleanVar(value=True)
and_checkbox = tk.Checkbutton(window, text='and����', font=("Helvetica", 14), variable=and_checkbox_var)
and_checkbox.pack()

# �f�B���N�g���I����CSV�o�̓{�^��
export_csv_button = tk.Button(window, text='�f�B���N�g����I�� \n �������ʂ�CSV�o��', font=("Helvetica", 14), command=search_pdf)
export_csv_button.pack()

window.mainloop()
