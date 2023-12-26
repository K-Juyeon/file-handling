import os
import argparse
import pandas as pd

def _get_parser():
    ''' Get arguments parser '''
    parser = argparse.ArgumentParser(description='Attribute Count')
    parser.add_argument('--p', type=str,
                        default='',
                        help='Count Attribute Path')

    return parser

def count_attribute(dataset_path, date, results) :
    result = [0 for _ in range(77)]
    for paths, dirs, files in os.walk(os.path.join(dataset_path, date)) :
        filelist = os.listdir(paths)
        filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
        for file in filelist_jpg :
            if 'without_bbox' in str(os.path.join(paths, file)) :
                filename = file.split("_")
                if filename[1] == "m" : result[0] += 1
                elif filename[1] == "f" : result[1] += 1

                if filename[2] == "if" : result[2] += 1
                elif filename[2] == "sc" : result[3] += 1
                elif filename[2] == "tn" : result[4] += 1
                elif filename[2] == "ya" : result[5] += 1
                elif filename[2] == "ad" : result[6] += 1

                if filename[3] == "jp" : result[7] += 1
                elif filename[3] == "sh" : result[8] += 1
                elif filename[3] == "jk" : result[9] += 1
                elif filename[3] == "lc" : result[10] += 1
                elif filename[3] == "ts" : result[11] += 1

                if filename[4] == "lo" : result[12] += 1
                elif filename[4] == "sh" : result[13] += 1
                elif filename[4] == "sl" : result[14] += 1

                if filename[5] == "br" : result[15] += 1
                elif filename[5] == "rd" : result[16] += 1
                elif filename[5] == "or" : result[17] += 1
                elif filename[5] == "ye" : result[18] += 1
                elif filename[5] == "gn" : result[19] += 1
                elif filename[5] == "be" : result[20] += 1
                elif filename[5] == "nv" : result[21] += 1
                elif filename[5] == "bl" : result[22] += 1
                elif filename[5] == "pu" : result[23] += 1
                elif filename[5] == "pk" : result[24] += 1
                elif filename[5] == "gr" : result[25] += 1
                elif filename[5] == "wh" : result[26] += 1
                elif filename[5] == "bk" : result[27] += 1
                elif filename[5] == "ck" : result[28] += 1
                elif filename[5] == "st" : result[29] += 1
                elif filename[5] == "cb" : result[30] += 1
                elif filename[5] == "pr" : result[31] += 1

                if filename[6] == "lp" : result[32] += 1
                elif filename[6] == "sp" : result[33] += 1
                elif filename[6] == "ls" : result[34] += 1
                elif filename[6] == "ss" : result[35] += 1

                if filename[7] == "br" : result[36] += 1
                elif filename[7] == "rd" : result[37] += 1
                elif filename[7] == "or" : result[38] += 1
                elif filename[7] == "ye" : result[39] += 1
                elif filename[7] == "gn" : result[40] += 1
                elif filename[7] == "be" : result[41] += 1
                elif filename[7] == "nv" : result[42] += 1
                elif filename[7] == "bl" : result[43] += 1
                elif filename[7] == "pu" : result[44] += 1
                elif filename[7] == "pk" : result[45] += 1
                elif filename[7] == "gr" : result[46] += 1
                elif filename[7] == "wh" : result[47] += 1
                elif filename[7] == "bk" : result[48] += 1
                elif filename[7] == "pt" : result[49] += 1

                if filename[8] == "sh" : result[50] += 1
                elif filename[8] == "bh" : result[51] += 1
                elif filename[8] == "lh" : result[52] += 1
                elif filename[8] == "po" : result[53] += 1
                elif filename[8] == "bl" : result[54] += 1
                elif filename[8] == "ht" : result[55] += 1
                elif filename[8] == "hm" : result[56] += 1

                if filename[9] == "gl" : result[57] += 1
                elif filename[9] == "sg" : result[58] += 1
                elif filename[9] == "ng" : result[59] += 1

                if filename[10] == "lb" : result[60] += 1
                elif filename[10] == "sb" : result[61] += 1
                elif filename[10] == "bp" : result[62] += 1
                elif filename[10] == "cr" : result[63] += 1
                elif filename[10] == "nb" : result[64] += 1

                if filename[11] == "ma" : result[65] += 1
                elif filename[11] == "nm" : result[66] += 1

                if filename[12] == "cr" : result[67] += 1
                elif filename[12] == "wh" : result[68] += 1
                elif filename[12] == "ca" : result[69] += 1
                elif filename[12] == "wf" : result[70] += 1
                elif filename[12] == "no" : result[71] += 1

                if filename[13] == "bt" : result[72] += 1
                elif filename[13] == "lf" : result[73] += 1
                elif filename[13] == "sk" : result[74] += 1
                elif filename[13] == "sp" : result[75] += 1
                elif filename[13] == "ns" : result[76] += 1
    result.insert(0, date)
    print(result)
    results.append(result)
    return results

def main():
    parser = _get_parser()
    opt = parser.parse_args()
    results = []

    if len(opt.p) == 4 :
        # dataset_path = os.path.join('Z:\\data\\auto_labeling_results', opt.p)
        dataset_path = 'Z:\\data_final'
        date = opt.p
        results = count_attribute(dataset_path, date, results)
    else :
        dataset_path = opt.p
        date_list = os.listdir(dataset_path)
        for date in date_list :
            results = count_attribute(dataset_path, date, results)

    result_df = pd.DataFrame(results, columns=['date', 'man', 'woman', 'infant', 'child', 'teenager', 'senior',
                                               'old_people', 'jumper', 'shirt', 'jacket', 'long_coat', 't_shirt',
                                               'long_sleeve', 'short_sleeve', 'sleeveless', 'top_brown', 'top_red', 'top_orange',
                                               'top_yellow', 'top_green', 'top_beige', 'top_navy', 'top_blue', 'top_purple',
                                               'top_pink', 'top_gray', 'top_white', 'top_black', 'top_check', 'top_stripe',
                                               'top_colorblocking', 'top_printing', 'long_pants', 'short_pants', 'long_skirt', 'short_skirt',
                                               'bottom_brown', 'bottom_red', 'bottom_orange',
                                               'bottom_yellow', 'bottom_green', 'bottom_beige', 'bottom_navy', 'bottom_blue', 'bottom_purple',
                                               'bottom_pink', 'bottom_gray', 'bottom_white', 'bottom_black', 'bottom_pattern',
                                               'short_hair', 'bobbed_hair', 'long_hair', 'ponytail', 'blad', 'hat', 'halmet',
                                               'glass', 'sunglass', 'no_glass', 'long_strap_bag', 'short_strap_bag', 'backpack',
                                               'carrier', 'no_bag', 'mask', 'no_mask', 'crutches', 'wheelchair',
                                               'cane', 'wf', 'no_wf', 'boots', 'loafers', 'sneakers',
                                               'slipper', 'no_shoes'])
    
    with pd.ExcelWriter(".\\count_attribute.xlsx", engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='results', index=False)

if __name__ == '__main__':
    main()