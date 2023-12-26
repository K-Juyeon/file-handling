import os
import argparse

main_p = r"Z:\workin\bbox_results"

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='File Count')
    parser.add_argument('--p', type=str,
                        default=main,
                        help='Count File Path')

    return parser

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    
    if len(opt.p) == 4 : #"Z:\\data\\auto_labeling_results" :
        data_path = os.path.join(main_p, opt.p)
    else :
        data_path = opt.p
        

    for paths, dirs, files in os.walk(data_path) :
        try :
            if "without_bbox" in paths :
                filelist = os.listdir(paths)
                filelist_jpg = [file for file in filelist if file.endswith('.jpg') or file.endswith('.json')]
                filelist_ = os.listdir(paths.replace("bbox_results", "검수완"))
                filelist_jpg_ = [file for file in filelist_ if file.endswith('.jpg') or file.endswith('.json')]
                if len(filelist_jpg) != len(filelist_jpg_) :
                    print(paths.split("\\")[-2], ":", str(len(filelist_jpg)), str(len(filelist_jpg_)))
        except:
            print(paths)

if __name__ == '__main__':
    main()