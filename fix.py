import os
import json
import traceback
import datetime
import sys

attribute = {
    "gender" : {
        "na":" ",
        "m":"man", 
        "f":"woman"
        },

    "age_group" : {
        "na":" ",
        "if":"infant",
        "sc":"child",
        "tn":"teenager",
        "ya":"seniors",
        "ad":"old people"
        },


    "top_type" : {
        "na":" ",
        "jk":"jacket",
        "jp":"jumper",
        "lc":"long-coat",
        "sh":"shirt",
        "ts":"t-shirt"
        },

    "top_shape" : {
        "na":" ",
        "sh":"short-sleeve",
        "sl":"sleeveless",
        "lo":"long-sleeve"
        },

    "color" : {
        "na": " ",
        "be": "beige",
        "bk": "black",
        "bl": "blue",
        "br": "brown",
        "gr": "gray",
        "gn": "green",
        "nv": "navy",
        "or": "orange",
        "pk": "pink",
        "pu": "purple",
        "rd": "red",
        "wh": "white",
        "ye": "yellow",
        "ck": "check",
        "cb": "color-blocking",
        "pr": "printing",
        "st": "stripe",
        "pt": "pattern"
    },

    "bottom_type" : {
        "na":" ",
        "lp":"long-pants",
        "sp":"short-pants",
        "ls":"long-skirt",
        "ss":"short-skirt"
        },

    "hairstyle" : {
        "na":" ",
        "bl":"bald",
        "bh":"bobbed-hair",
        "ht":"hat",
        "hm":"helmet",
        "lh":"long-hair",
        "po":"ponytail",
        "sh":"short-hair"
        },

    "glasses" : {
        "na":" ",
        "gl":"glasses",
        "ng":"no-glasses",
        "sg":"sunglasses"
        },

    "bag" : {
        "na":" ",
        "bp":"backpack",
        "cr":"carrier",
        "lb":"long-strap-bag",
        "nb":"no-bag",
        "sb":"short-strap-bag"
        },
    
    "mask" : {
        "na":" ",
        "ma":"mask",
        "nm":"no-mask"
        },

    "walking_accessory" : {
        "na":" ",
        "ca":"cane",
        "cr":"crutches",
        "no":"no-wf",
        "wh":"wheelchair",
        "wf":"wf"
        },

    "shoes" : {
        "na":" ",
        "bt":"boots",
        "lf":"loafers",
        "ns":"no-shoes",
        "sp":"slipper",
        "sk":"sneakers"
        }
}
# data_path = 'Z:\\testfile\\auto_labeling_results\\20230821165130_f_if_lc_lo_pk_ls_pu_po_gl_nb_nm_ca_sk_0815-gn-na-na-na-na-na_2023_07_19_223403'
# data_path = 'Z:\\data\\auto_labeling_results\\0821\\0815\\20230821165130_f_if_lc_lo_pk_ls_pu_po_gl_nb_nm_ca_sk_0815-gn-na-na-na-na-na_2023_07_19_223403'
data_path = 'Z:\\data\\auto_labeling_results\\0801'
# data_path = 'Z:\\data\\auto_labeling_results'
error_paths = [] 
file_name_error = 0

now = datetime.datetime.now()
f = open('file_update_' + str(now.strftime('%y%m%d%H%M%S')) + '.txt', 'w', encoding='utf-8')
f.write(data_path + '\n')
code3 = 0
code2 = 0
code1 = 0
code0 = 0
code = 0

for paths, dirs, files in os.walk(data_path) :
    filelist = os.listdir(paths)
    filelist_jpg = [file for file in filelist if file.endswith('.jpg')]
    json_path = [file for file in filelist if file.endswith('.json')]
    if "0825" not in paths :
        if len(json_path) > 0 :
            try :
                with open(os.path.join(paths, json_path[0]), 'r', encoding="utf-8") as json_file:
                    json_data = json.load(json_file)
            except json.JSONDecodeError:
                print(json_path[0])
                print(traceback.format_exc())
                exit()
            for img, ann in zip(json_data["images"], json_data["annotations"]):
                id = img["id"]
                file_name2 = img["file_name"]
                seq = file_name2[75:85]
                att = ann['attributes']
                model_no = att["actor_id"]
                if att["top_shape"] == "short_sleeve" :
                    att["top_shape"] = "short-sleeve"
                elif att["top_shape"] == "long_sleeve":
                    att["top_shape"] = "long-sleeve"
                gender_jname            = [key for key, val in attribute["gender"].items() if val == att["gender"]][0]
                age_group_jname         = [key for key, val in attribute["age_group"].items() if val == att["age_group"]][0]
                top_type_jname          = [key for key, val in attribute["top_type"].items() if val == att["top_type"]][0]
                top_shape_jname         = [key for key, val in attribute["top_shape"].items() if val == att["top_shape"]][0]
                top_color_jname         = [key for key, val in attribute["color"].items() if val == att["top_color"]][0]
                bottom_type_jname       = [key for key, val in attribute["bottom_type"].items() if val == att["bottom_type"]][0]
                bottom_color_jname      = [key for key, val in attribute["color"].items() if val == att["bottom_color"]][0]
                hairstyle_jname         = [key for key, val in attribute["hairstyle"].items() if val == att["hairstyle"]][0]
                glasses_jname           = [key for key, val in attribute["glasses"].items() if val == att["glasses"]][0]
                bag_jname               = [key for key, val in attribute["bag"].items() if val == att["bag"]][0]
                mask_jname              = [key for key, val in attribute["mask"].items() if val == att["mask"]][0]
                walking_accessory_jname = [key for key, val in attribute["walking_accessory"].items() if val == att["walking_accessory"]][0]
                shoes_jname             = [key for key, val in attribute["shoes"].items() if val == att["shoes"]][0]
                inner_color_jname       = [key for key, val in attribute["color"].items() if val == att["inner_color"]][0]
                top_color1_jname        = [key for key, val in attribute["color"].items() if val == att["top_color1"]][0]
                top_color2_jname        = [key for key, val in attribute["color"].items() if val == att["top_color2"]][0]
                top_color3_jname        = [key for key, val in attribute["color"].items() if val == att["top_color3"]][0]
                bottom_color1_jname     = [key for key, val in attribute["color"].items() if val == att["bottom_color1"]][0]
                bottom_color2_jname     = [key for key, val in attribute["color"].items() if val == att["bottom_color2"]][0]

                if top_color_jname == "ck" :
                    att["top_check"] == True
                    att["top_color_blocking"] == False
                    att["top_printing"] == False
                    att["top_stripe"] == False
                elif top_color_jname == "cb" :
                    att["top_check"] == False
                    att["top_color_blocking"] == True
                    att["top_printing"] == False
                    att["top_stripe"] == False
                elif top_color_jname == "pr" :
                    att["top_check"] == False
                    att["top_color_blocking"] == False
                    att["top_printing"] == True
                    att["top_stripe"] == False
                elif top_color_jname == "st" :
                    att["top_check"] == False
                    att["top_color_blocking"] == False
                    att["top_printing"] == False
                    att["top_stripe"] == True
                else :
                    att["top_check"] == False
                if bottom_color_jname == "pt" :
                    att["bottom_pattern"] == True
                else :
                    att["bottom_pattern"] == False

                file_name3 = file_name2[0:14] + "_" + gender_jname + "_" + age_group_jname + "_" + top_type_jname + "_" + top_shape_jname + "_" + top_color_jname + "_" + bottom_type_jname + "_" + bottom_color_jname + "_" + hairstyle_jname + "_" + glasses_jname + "_" + bag_jname + "_" + mask_jname + "_" + walking_accessory_jname + "_" +  shoes_jname + "_" + model_no + "-" + inner_color_jname + "-" + top_color1_jname + "-" + top_color2_jname + "-" + top_color3_jname + "-" + bottom_color1_jname + "-" + bottom_color2_jname + seq
                try :
                    file_name_1 = [file for file in filelist_jpg if seq in file]
                    file_name1 = file_name_1[0]
                    if len(file_name_1) > 1 :
                        print(file_name_1)
                except :
                    file_name1 == 'ERROR: ' + file_name2

                if 'ERROR' in file_name1 :
                    f.write("실제 파일 명: " + file_name1 + "\n")
                    f.write("파일 파일 명: " + file_name2 + "\n")
                    f.write("속성 파일 명: " + file_name3 + "\n\n")
                else :
                    # # if file_name3 != file_name2 and file_name3 != file_name1 and file_name1 == file_name2 :
                    # #     code3 += 1
                    # #     # f.write("파일명 변경\n")
                    # #     f.write("실제 파일 명: " + file_name1 + "\n")
                    # #     f.write("파일 파일 명: " + file_name2 + "\n")
                    # #     f.write("속성 파일 명: " + file_name3 + "\n\n")
                    # #     img["file_name"] = file_name3
                    # #     os.rename(os.path.join(paths, file_name1), os.path.join(paths, file_name3))
                    # if file_name1 != file_name2 and file_name1 != file_name3 and file_name2 == file_name3 :
                    # # if file_name3 != file_name2 or file_name3 != file_name1 :
                        # code2 += 1 #20230707110118_m_ya_ts_sh_gr_lp_nv_sh_gl_nb_nm_no_sk_0145-na-na-na-na-na-na_000000.ㅓㅔㅎ
                        # f_att_list = file_name1.split("_")
                        # f_att_list_ex = f_att_list[14].split("-")
                        # att["gender"] = attribute["gender"][f_att_list[1]]
                        # att["age_group"] = attribute["age_group"][f_att_list[2]]
                        # att["top_type"] = attribute["top_type"][f_att_list[3]]
                        # att["top_shape"] = attribute["top_shape"][f_att_list[4]]
                        # att["top_color"] = attribute["color"][f_att_list[5]]
                        # att["bottom_type"] = attribute["bottom_type"][f_att_list[6]]
                        # att["bottom_color"] = attribute["color"][f_att_list[7]]
                        # att["hairstyle"] = attribute["hairstyle"][f_att_list[8]]
                        # att["glasses"] = attribute["glasses"][f_att_list[9]]
                        # att["bag"] = attribute["bag"][f_att_list[10]]
                        # att["mask"] = attribute["mask"][f_att_list[11]]
                        # att["walking_accessory"] = attribute["walking_accessory"][f_att_list[12]]
                        # att["shoes"] = attribute["shoes"][f_att_list[13]]
                        # att["inner_color"] = attribute["color"][f_att_list_ex[1]]
                        # att["top_color1"] = attribute["color"][f_att_list_ex[2]]
                        # att["top_color2"] = attribute["color"][f_att_list_ex[3]]
                        # att["top_color3"] = attribute["color"][f_att_list_ex[4]]
                        # att["bottom_color1"] = attribute["color"][f_att_list_ex[5]]
                        # att["bottom_color2"] = attribute["color"][f_att_list_ex[6][0:2]]

                    #     if att["top_color"] == "ck" :
                    #         att["top_check"] == True
                    #         att["top_color_blocking"] == False
                    #         att["top_printing"] == False
                    #         att["top_stripe"] == False
                    #     elif att["top_color"] == "cb" :
                    #         att["top_check"] == False
                    #         att["top_color_blocking"] == True
                    #         att["top_printing"] == False
                    #         att["top_stripe"] == False
                    #     elif att["top_color"] == "pr" :
                    #         att["top_check"] == False
                    #         att["top_color_blocking"] == False
                    #         att["top_printing"] == True
                    #         att["top_stripe"] == False
                    #     elif att["top_color"] == "st" :
                    #         att["top_check"] == False
                    #         att["top_color_blocking"] == False
                    #         att["top_printing"] == False
                    #         att["top_stripe"] == True
                    #     else :
                    #         att["top_check"] == False
                    #     if att["bottom_color"] == "pt" :
                    #         att["bottom_pattern"] == True
                    #     else :
                    #         att["bottom_pattern"] == False

                    #     f.write(paths + "\n")
                    #     f.write("실제 파일 명: " + file_name1 + "\n")
                    #     f.write("파일 파일 명: " + file_name2 + "\n")
                    #     f.write("속성 파일 명: " + file_name3 + "\n\n")
                    #     img["file_name"] = file_name1
                    # elif file_name2 != file_name1 and file_name2 != file_name3 and file_name1 == file_name3 :
                    #     code1 += 1
                    #     # f.write("파일명 변경\n")
                    #     f.write("실제 파일 명: " + file_name1 + "\n")
                    #     f.write("파일 파일 명: " + file_name2 + "\n")
                    #     f.write("속성 파일 명: " + file_name3 + "\n\n")
                    #     img["file_name"] = file_name3
                    #     os.rename(os.path.join(paths, file_name1), os.path.join(paths, file_name3))
                    # else :
                    #     code0 += 1
                    # if file_name3 != file_name2 or file_name3 != file_name1 :
                        # code += 1

                        # f.write("실제 파일 명: " + file_name1 + "\n")
                        # f.write("파일 파일 명: " + file_name2 + "\n")
                        # f.write("속성 파일 명: " + file_name3 + "\n\n")

                    #     img["file_name"] = file_name3
                    #     os.rename(os.path.join(paths, file_name1), os.path.join(paths, file_name3))
                    # with open(os.path.join(paths, json_path[0]), 'w', encoding="utf-8") as json_file:
                    #     json.dump(json_data, json_file)
                    if file_name1 != file_name2 or file_name1 != file_name3 or file_name2 != file_name3:
                        code += 1
                        f.write("실제 파일 명: " + file_name1 + "\n")
                        f.write("파일 파일 명: " + file_name2 + "\n")
                        f.write("속성 파일 명: " + file_name3 + "\n\n")

                    #     img["file_name"] = file_name3
                    #     os.rename(os.path.join(paths, file_name1), os.path.join(paths, file_name3))
                    # with open(os.path.join(paths, json_path[0]), 'w', encoding="utf-8") as json_file:
                    #     json.dump(json_data, json_file)

print('속성값 기준:', str(code3), '\n실제 파일명 기준:', str(code2), '\njson 파일명 기준:', str(code1), '\n그 외:', str(code0))
print(code)