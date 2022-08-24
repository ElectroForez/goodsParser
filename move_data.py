import pandas as pd
import re
from numpy import NaN


def move_data_to_csv(filename, new_filename='untitled.csv'):
    def split_title(title):
        result = {}
        pattern = r'[ ]+(\w*(\d|-)+|DIN).*'
        re_result = re.search(pattern, title)
        if re_result:
            result['size'] = re_result[0].strip()
            result['name'] = title[:re_result.span(0)[0]]
        else:
            result['size'] = NaN
            result['name'] = title.strip()
        return result

    df = pd.read_excel(filename, header=None)
    title_column = 2

    df_size = df[title_column].apply(lambda x: split_title(x)['size'])
    df_name = df[title_column].apply(lambda x: split_title(x)['name'])
    df.insert(title_column, 'size', df_size)
    df.insert(title_column, 'name', df_name)
    df = df.drop(title_column, axis=1)

    df_wo_legend = df.iloc[:, :-2]  # legend exists from right size
    df_wo_legend.to_csv(new_filename, sep=';', header=False, index=False)


if __name__ == '__main__':
    # example of launch
    filename = 'example/База 07.06.22.xlsx'
    new_filename = 'example/База.txt'
    move_data_to_csv(filename, new_filename)
