import cv2
import glob
import pandas as pd
import numpy as np
import json
from functools import cmp_to_key
from operator import itemgetter

draw = True
df = pd.DataFrame()
count =0
write_on_file = False

def find_top_n_indices(data, top=3):
    indexed = enumerate(data)  # create pairs [(0, v1), (1, v2)...]
    sorted_data = sorted(indexed,
                         key=itemgetter(1),   # sort pairs by value
                         reverse=True)       # in reversed order
    return [d[0] for d in sorted_data[:top]]  # take first N indices

def contour_sort(a, b):
    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)
    return br_a[0] - br_b[0]

for kl in ['0','1','2','3','4']: # from 2 sorted
    print("\n ############## KL grade",kl)
    list_all = glob.glob('.\\KL_samples\\masks\\'+kl+'\\*.png', recursive=False)
    original_images= list_all #= glob.glob('.\\KL_samples\\images\\'+kl+'\\*.png', recursive=False)
    print(original_images)

    # https://www.tutorialspoint.com/how-to-compute-the-area-and-perimeter-of-an-image-contour-using-opencv-python
    # https://pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/
    for image in original_images:
        file_name = image.split("\\")[-1]
        print("\nLocation: ",image, " \nfile_name: ", file_name, count)
        # Read the input image
        img = cv2.imread(image)
        img_original = cv2.imread(image.replace("masks","images"))
        line_thickness = 1
        x1, y1, y2 = 85,0,300
        cv2.line(img, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
        cv2.line(img_original, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
        x1, y1, y2 = 135, 0, 300
        cv2.line(img, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
        cv2.line(img_original, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
        # x1, x2, y1 = 0, 300, 75
        # cv2.line(img, (x1, y1), (x2, y1), (0, 255, 0), thickness=line_thickness)
        # cv2.line(img_original, (x1, y1), (x2, y1), (0, 255, 0), thickness=line_thickness)
        # x1, x2, y1 = 0, 300, 170
        # cv2.line(img, (x1, y1), (x2, y1), (0, 255, 0), thickness=line_thickness)
        # cv2.line(img_original, (x1, y1), (x2, y1), (0, 255, 0), thickness=line_thickness)
        # convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding in the gray image to create a binary image
        ret, thresh = cv2.threshold(gray, 150, 255, 0)
        # Find the contours using binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cmp_to_key(contour_sort))

        print("Number of contours in image:", len(contours))
        areas = []
        for cont in contours:
            # cnt = contours[0]
            cnt = cont
            # compute the area and perimeter
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)
            # print('Area:', area)
            areas.append(area)
            # if draw:
            # if len(contours) != 3:
            #     img1 = cv2.drawContours(img, [cnt], -1, (0, 255, 255), 1)
            #     if write_on_file:
            #         x1, y1 = cnt[0, 0]
            #         cv2.putText(img1, f'Area:{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            #         cv2.putText(img1, f'Perimeter:{perimeter}', (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if len(areas) != 3:
            print("areas: ", areas)
            # if no 3 draw:
            # Hori = np.concatenate((img, img_original), axis=1)
            # cv2.imshow("Image", Hori)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # try to solve not 3
            areas = [x for x in areas if int(x) > 20]
            file_dic = {}
            with open('dic.txt') as f:
                data = f.read()
                file_dic = json.loads(data)
                print("Last retouch: ", list(file_dic)[-1], file_dic[list(file_dic)[-1]],  )
            # file_dic["9001897L"] = [190.0]
            # file_dic["9003658L"] = [266.0, 63.5]
            # file_dic["9003658R"] = [104.5]
            # file_dic["9008820L"] = [167.0]
            # file_dic["9019287L"] = [99.5]
            # file_dic["9021195L"] = [55.5]
            # file_dic["9022703L"] = [65.0]
            # file_dic["9022789L"] = [24.0,152.0]
            # file_dic["9030418L"] = [78.0]
            # file_dic["9033937L"] = [57.5]
            # file_dic["9035779L"] = [267.5]
            # file_dic["9039972L"] = [58.0]
            # file_dic["9040390L"] = [26.0]
            # file_dic[""] = []
            # file_dic[""] = [ ]
            print("areas: ", areas)
            try:
                val_to_filter = file_dic[file_name.split(".")[0]]
                areas = [x for x in areas if ((x) not in val_to_filter) ]
                for x in val_to_filter:
                    if x=='l':
                        areas.insert(0, 0)
                    if x=='r':
                        areas.append(0)
                    if x=='c':
                        areas.insert(1, 0)
                print("solved:", areas)
                if val_to_filter[0] == 'n':
                    continue
            except:
                abc = 123
            if len(areas) != 3:
                Hori = np.concatenate((img, img_original), axis=1)
                cv2.imshow("Image", Hori)
                cv2.waitKey(3000)
                # cv2.waitKey(0)
                cv2.destroyAllWindows()

            if len(areas) < 3:

                file_dic[file_name.split(".")[0]] = []

                use = input("use?\n")
                if use == 'n':
                    file_dic[file_name.split(".")[0]] = ['n']
                    with open('dic.txt', 'w') as convert_file:
                        convert_file.write(json.dumps(file_dic))
                    continue
                while (len(areas)<3):
                    left_right_missing = input("Left or right is missing?  l/r/c")
                    if left_right_missing =="l":
                        areas.insert(0,0)
                        print('l: ',areas)
                        add = file_dic[file_name.split(".")[0]]
                        add.append('l')
                        file_dic[file_name.split(".")[0]] = add
                    if left_right_missing == "r":
                        areas.append(0)
                        print('r: ', areas)
                        add = file_dic[file_name.split(".")[0]]
                        add.append('r')
                        file_dic[file_name.split(".")[0]] = add
                    if left_right_missing == "c":
                        areas.insert(1,0)
                        print('c: ', areas)
                        add = file_dic[file_name.split(".")[0]]
                        add.append('r')
                        file_dic[file_name.split(".")[0]] = add


            if len(areas) > 3:
                file_dic[file_name.split(".")[0]] = []
                top3 = find_top_n_indices(areas)
                top3 = sorted(top3)
                elements = []
                for x in top3:
                    elements.append(areas[x])
                print("Top 3 elements: ", elements)
                top3_y = input("Top 3 elements?\n")
                if top3_y == 'y':
                    for x in range(len(areas)):
                        if areas[x] not in elements:
                            add = file_dic[file_name.split(".")[0]]
                            add.append(areas[x])
                            file_dic[file_name.split(".")[0]] = add
                    areas = elements
                # elif top3_y == 'n':
                #     file_dic[file_name.split(".")[0]]= ['n']

            if len(areas) > 3:
                print("len(areas): ",len(areas))
                filter_them = input("filter_them?\n") # 1 1 1 0
                if filter_them == 'n':
                    file_dic[file_name.split(".")[0]] = ['n']
                    with open('dic.txt', 'w') as convert_file:
                        convert_file.write(json.dumps(file_dic))
                    continue
                filter_them = filter_them.split(" ")
                filter_them = [x for x in filter_them if x not in [""," ", "  "]]
                print(filter_them)
                filtered = []
                file_dic[file_name.split(".")[0]] = []
                for x in range(len(areas)):
                    if (int(filter_them[x])==1):
                        filtered.append(areas[x])
                    else:
                        add = file_dic[file_name.split(".")[0]]
                        add.append(areas[x])
                        file_dic[file_name.split(".")[0]] =  add
                areas = filtered
                print(areas)

        with open('dic.txt', 'w') as convert_file:
            convert_file.write(json.dumps(file_dic))

        if len(areas) != 3:
            print(">>> len(areas) != 3")
            exit()

        if ("R" in file_name) :
            area_temp = areas[2]
            areas[2] = areas[0]
            areas[0] = area_temp
            side = "Right"
        elif "L"  in file_name:
            side = "Left"
        else:
            print("Not left or right!!!")
            exit()

        df = df.append({'fileLocation': image, 'file_name': file_name, 'side': side, 'inner':areas[0], 'mid':areas[1] , 'outer':areas[2], "kl":kl},
                       ignore_index=True)
        count+=1

df.to_csv('.\\data_KL_samples.csv', index=False)
print("\ncount",count)
    # biladeral frontal view

# both focused on normal
#