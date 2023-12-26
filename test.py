import os
import json
import cv2
import shutil
import pandas as pd
import sys
import traceback

def mouse_click(event, x, y, flags, param) :
    global points
    if event == cv2.EVENT_LBUTTONDOWN :
        if last_image != 1080 :
            x = int(x / zoom)
            y = int(y / zoom)
        points.append([x, y])
        if len(points) == 4: 
            cv2.destroyAllWindows()
            
base = "data"
after = "bbox_results"
zoom = 2
extra = 80
last_image = 0

while True :
    path = input("Path: ")
    if path == "exit" :
        sys.exit()
    for paths, dirs, files in os.walk(path) :
        json_files = os.listdir(paths)
        json_file = [file for file in json_files if file.endswith('.json')]
        if len(json_file) > 0 and "without_bbox" in paths:
            try :
                shutil.copytree(paths, paths.replace(base, after))
            except FileExistsError as e:
                pass
            except :
                print(traceback.format_exc())
                break

            with open(os.path.join(paths.replace(base, after), json_file[0]), 'r', encoding="utf-8") as file:
                data = json.load(file)

            images = data['images']
            if len(images) == 0 :
                print(paths)

            for image_info in images:
                points = []
                image_id = image_info.get('id')
                file_name = image_info.get('file_name')

                for ann in data['annotations'] :
                    if ann['id'] == image_id :
                        x, y, width, height = ann["bbox"] 
                        # print(x, y, width, height)

                        image_path = os.path.join(paths.replace(base, after), file_name)

                        image = cv2.imread(image_path)
                        roi = image[y-extra:y+height+extra, x-extra:x+width+extra]

                        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                        cv2.rectangle(image, (x, y + height), (x + width, y), (0,255,0), thickness=1)
                        # cv2.imshow('image', image)
                        try :
                            zoom_image = cv2.resize(roi, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_LINEAR)
                            cv2.imshow('image', zoom_image)
                            last_image = zoom_image.shape[0]
                            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                            # cv2.moveWindow('image', 0, 0)
                        except :
                            cv2.imshow('image', image)
                            last_image = image.shape[0]
                            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        
                        while True :
                            cv2.setMouseCallback('image', mouse_click)
                            key = cv2.waitKey(0)

                            if len(points) == 4 :
                                if last_image == 1080 :
                                    points_df = pd.DataFrame(points)

                                    x_ = points_df[:][0].min()
                                    y_ = points_df[:][1].min()
                                    width_ = points_df[:][0].max() - points_df[:][0].min()
                                    height_ = points_df[:][1].max() - points_df[:][1].min()
                                else :
                                    points_df = pd.DataFrame(points)

                                    x_ = points_df[:][0].min() + (x-extra)
                                    y_ = points_df[:][1].min() + (y-extra)
                                    width_ = points_df[:][0].max() - points_df[:][0].min()
                                    height_ = points_df[:][1].max() - points_df[:][1].min()

                                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                                cv2.rectangle(image, (x_, y_ + height_), (x_ + width_, y_), (255,0,0), thickness=1)
                                cv2.imshow('image', image)
                                cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                                if key == ord('s') or key == ord('S') :
                                    cv2.destroyAllWindows()
                                    ann["bbox"] = [int(x_), int(y_), int(width_), int(height_)]

                                    with open(os.path.join(paths.replace(base, after), json_file[0]), 'w', encoding="utf-8") as file:
                                        json.dump(data, file)
                                    print(os.path.join(paths, image_path), "수정")
                                    break
                                elif key == ord('a') or key == ord('A') :
                                    with open(os.path.join(paths.split("\\")[0], "bbox"), 'a+', encoding="utf-8") as file:
                                        file.writelines(os.path.join(paths, file_name))
                                elif key == ord('r') or key == ord('R') :
                                    cv2.destroyAllWindows()
                                    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                                    cv2.rectangle(image, (x, y + height), (x + width, y), (0,255,0), thickness=1)
                                    cv2.imshow('image', zoom_image)
                                    last_image = zoom_image.shape[0]
                                    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    points = []
                                    continue
                                elif key == ord('q') or key == ord('Q') :
                                    sys.exit()
                            elif key == ord('z') or key == ord('Z') :
                                if last_image == 1080 :
                                    cv2.destroyAllWindows()
                                    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                                    cv2.imshow('image', zoom_image)
                                    last_image = zoom_image.shape[0]
                                    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    points = []
                                    continue
                                else :
                                    cv2.destroyAllWindows()
                                    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                                    cv2.imshow('image', image)
                                    last_image = image.shape[0]
                                    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    points = []
                                    continue
                            elif key == ord('p') or key == ord('P') :
                                cv2.destroyAllWindows()
                                print(os.path.join(paths, image_path), "미수정")
                                break
                            elif key == ord('q') or key == ord('Q') :
                                sys.exit()
                            elif key == ord('e') or key == ord('E') :
                                with open("./error.txt", "a+", encoding="utf-8") as tfile :
                                    tfile.writelines(str(os.path.join(paths, file_name)))
                                print(os.path.join(paths, file_name) + " ERROR")


