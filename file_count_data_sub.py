import os
import argparse
from tqdm import tqdm

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='File Count')
    parser.add_argument('--path', type=str,
                        default='Z:\\data\\auto_labeling_results',
                        help='Count File Path')

    return parser

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    
    if len(opt.path) == 4 : #"Z:\\data\\auto_labeling_results" :
        data_path = os.path.join('Z:\\original_data\\auto_labeling_results', opt.path)
    else :
        data_path = opt.path
    count = 0
    # count_dict = {}

    # data_path_list = os.listdir(data_path)
    # for date in tqdm(data_path_list, desc="FILE COUNT") :
    #     for paths, dirs, files in os.walk(os.path.join(data_path, date)) :
    #         filelist = os.listdir(paths)
    #         filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
    #         for file in filelist_jpg :
    #             if 'with_bbox' in str(os.path.join(paths, file)) :
    #                 if date in count_dict.keys() :
    #                     count_dict[date] += 1
    #                 else :
    #                     count_dict[date] = 1
    #                 count += 1
    # print(count_dict)
    # print(count)

    for paths, dirs, files in os.walk(data_path) :
        filelist = os.listdir(paths)
        filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
        if 'without_bbox' in paths :
            count += len(filelist_jpg)

    print(count)
    # print(count)

if __name__ == '__main__':
    main()