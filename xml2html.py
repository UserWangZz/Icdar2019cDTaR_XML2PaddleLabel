from xml.etree import ElementTree as ET
from table import Cell, Table
from pathlib import Path
import os
import random
from tqdm import tqdm
import json


# xml_file = ET.parse('/Users/wangzhe35/Desktop/table/table/cTDaR_t00055.xml')
# print(xml_file)
# document = xml_file.getroot()
# filename = document.attrib.get('filename')

# table = xml_file.find('table')


# cells = []
# for cell in table.findall('cell'):
#     start_row = cell.attrib.get('start-row')
#     start_col = cell.attrib.get('start-col')
#     end_row = cell.attrib.get('end-row')
#     end_col = cell.attrib.get('end-col')
#     coords = cell.find('Coords')
#     points = coords.attrib.get('points')
#     cell = Cell(start_row, end_row, start_col, end_col, points, '1')
#     print(cell)
#     cells.append(cell)

# # print(cells)
# table = Table(cells)

# with open('./output55.html', 'w') as f:
#     f.write(table.recorvery_html_table())


def list_files(directory: Path, file_list: list = None):
    if file_list is None:
        file_list = []
    for item in directory.iterdir():
        if item.is_file():
            file_list.append(item.absolute())
        elif item.is_dir():
            list_files(item, file_list)
    return file_list


def read_xml(path_dir_of_xml):
    file_path = Path(path_dir_of_xml)
    file_list = list_files(file_path)

    # 根据文件名排序
    file_list.sort(key=lambda x: x)

    result = []
    for file in file_list:
        file = str(file)
        dir_name, base_name = os.path.split(file)
        if base_name.split('.')[-1] != 'xml':
            continue
        xml_file = ET.parse(file)
        result.append(xml_file)

    return result


def label_convert(xml_file, stage='train', img_id=0):
    '''
        将xml文件转换成ppstructure表格识别的label格式
    '''
    single_result_dict = {}
    document = xml_file.getroot()
    filename = document.attrib.get('filename')
    single_result_dict['filename'] = 'images/' + filename
    if stage == 'train':
        single_result_dict['split'] = 'train'
    else:
        single_result_dict['split'] = 'val'
    single_result_dict['img_id'] = img_id

    table = xml_file.find('table')

    cells = []
    for cell in table.findall('cell'):
        start_row = cell.attrib.get('start-row')
        start_col = cell.attrib.get('start-col')
        end_row = cell.attrib.get('end-row')
        end_col = cell.attrib.get('end-col')
        coords = cell.find('Coords')
        points = coords.attrib.get('points')
        cell = Cell(start_row, end_row, start_col, end_col, points, '1')
        # print(cell)
        cells.append(cell)

    # print(cells)
    table = Table(cells)

    convert_label = table.get_html_label()
    single_result_dict['html'] = convert_label

    return single_result_dict

# test single xml file
# if __name__ == '__main__':
#     xml_file = ET.parse(
#         './ICDAR2019_cTDaR/training/TRACKB1/ground_truth/cTDaR_t00031.xml')
#     label = label_convert(xml_file, stage='train', img_id=0)
#     print(label)

#     with open('test_label.json', 'w') as f:
#         json.dump(label, f)


if __name__ == '__main__':
    # give the path of xml and jpg file
    file_list = read_xml('./images')

    # you can delect this random code for the whole dataset.
    # file_dict共391个文件，将其划分为300和91，其中300个文件作为训练集，91个文件作为测试集，需要随机挑选
    random.seed(1024)
    train_set = random.sample(file_list, 300)
    # 剩下的91个文件作为测试集
    test_set = list(set(file_list) - set(train_set))
    print(len(train_set))
    print(len(test_set))

    # 处理train_set
    train_set_label_list = []
    train_img_id = 0
    for train_xml_file in tqdm(train_set):
        # 判断同名jpg文件是否存在
        train_single_label = label_convert(train_xml_file, stage='train', img_id=train_img_id)
        train_set_label_list.append(train_single_label)
        train_img_id += 1
    print(len(train_set_label_list))
    
    with open('train.txt', 'w') as f:
        for line in train_set_label_list:
            f.write(json.dumps(line) + '\n')
    
    
    # 处理test_set
    test_set_label_list = []
    test_img_id = 0
    for test_xml_file in tqdm(test_set):
        test_single_label = label_convert(test_xml_file, stage='test', img_id=test_img_id)
        test_set_label_list.append(test_single_label)
        test_img_id += 1
    print(len(test_set_label_list))
    with open('val.txt', 'w') as f:
        for line in test_set_label_list:
            f.write(json.dumps(line) + '\n')

    print('finished!!!')
