import os
import argparse
from tqdm import tqdm

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='File Count')
    parser.add_argument('--p', type=str,
                        default="",
                        help='Count File Path')
    parser.add_argument('--s', type=int,
                        default=0,
                        help='Count File Path')
    parser.add_argument('--e', type=int,
                        default=1,
                        help='Count File Path')

    return parser

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    
    # if len(opt.path) == 4 : #"Z:\\data\\auto_labeling_results" :
    #     data_path = os.path.join('Z:\\data\\auto_labeling_results', opt.path)
    # else :
    #     data_path = opt.path
    data_path = opt.p
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

    for m in range(opt.s, opt.e + 1) :
        if len(str(m)) == 3:
            m = "0" + str(m)
        m_path = os.path.join(data_path, str(m))
        for paths, dirs, files in os.walk(m_path) :
            filelist = os.listdir(paths)
            filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
            if 'without_bbox' in paths :
                count += len(filelist_jpg)

    # for paths, dirs, files in os.walk(data_path) :
    #     filelist = os.listdir(paths)
    #     filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
    #     if 'without_bbox' in paths :
    #         count += len(filelist_jpg)

    print(count)
    # print(count)

if __name__ == '__main__':
    main()