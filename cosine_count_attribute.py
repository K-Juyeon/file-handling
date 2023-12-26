import os

def count_attribute(filelist_jpg, date, results) :
    result = [0 for _ in range(77)]
    for file in filelist_jpg :
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
    results.append(result)
    return results