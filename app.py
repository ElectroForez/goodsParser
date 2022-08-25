import os
from tkinter import Tk, Label, Button, Entry, filedialog, END, messagebox
from tkinter.ttk import Combobox

from config import *
from move_data import move_data_to_csv

window = Tk()

window.title('goods parser')
window.geometry('450x200')


def click_upload():
    file = filedialog.askopenfile(filetypes=[('xlsx-файлы', '*.xlsx'), ('Все файлы', '*.*')])
    if file is None:
        print('Отмена выбора файла')
        return
    filename = os.path.relpath(file.name)
    lblNewFile.configure(text=filename)
    entryNewFile.delete(0, END)
    file, ext = os.path.splitext(filename)
    print('Выбран файл ' + file)
    entryNewFile.configure(state='normal')
    entryNewFile.insert(0, file + '.txt')


def click_save():
    filename = lblNewFile.cget('text')
    new_filename = entryNewFile.get()
    if not new_filename:
        messagebox.showerror('Разрази меня гром', f'Куда файл-то сохранять?')
        return

    try:
        move_data_to_csv(filename, new_filename, sep=comboSep.get())
        print('Новый файл сохранён ' + new_filename)
    except OSError as error:
        messagebox.showerror('Японский дивидишник', f'Путь {new_filename} не существует')
        raise error
    except ValueError as error:
        messagebox.showerror('Ядрён батон', f'Чёт не так с файлом {filename}')


lblSep = Label(window, text="Разделитель", font=default_font)
lblSep.grid(column=0, row=0)

comboSep = Combobox(window, width=2, state='readonly', font=default_font)
comboSep['values'] = separators
comboSep.current(0)
comboSep.grid(column=1, row=0)

btnFile = Button(window, text="Выбрать файл", command=click_upload, font=default_font)
btnFile.grid(column=0, row=1)

lblNewFile = Label(window, text='Файл не выбран', font=default_font)
lblNewFile.grid(column=1, row=1)

entryNewFile = Entry(window, font=default_font, state='disabled')
entryNewFile.insert(0, 'untitled.txt')
entryNewFile.grid(column=0, row=2)

btnFile = Button(window, text="Создать новый файл", command=click_save, font=default_font)
btnFile.grid(column=1, row=2)

window.mainloop()
