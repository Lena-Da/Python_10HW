import csv


def write_csv(array:list)->None:
    '''
    Запись в файл
    '''
    with open('data.csv', mode ='a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=',', lineterminator='\n')
        file_writer.writerow(array)

def search_csv(text:str)->list:
    """
    Поиск данных в файле и вывод
    """
    with open('data.csv', 'r', encoding='utf-8') as f:
        lst = f.read().splitlines()
        list_search = []
        for i in lst:
            if text in i:
                list_search.append(i)
        if len(list_search) == 0:
            return 'Данные осутствуют'
        else:
            return list_search

def read_csv()->list:
    '''
    Чтение из файла
    '''
    with open('data.csv', newline='\n', encoding = 'utf-8') as File:  
        reader = csv.reader(File, delimiter=',', lineterminator='\n')
        file_reader = []        
        for row in reader:
            file_reader.append(row)
    return file_reader