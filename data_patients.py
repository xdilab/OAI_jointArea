import cv2
import glob
import pandas as pd

draw = True
df = pd.DataFrame()
count =0

list_all = glob.glob('.\\images\\*.png', recursive=False)
original_images= [x for x in list_all if "[" in x]
print(original_images)

# https://www.tutorialspoint.com/how-to-compute-the-area-and-perimeter-of-an-image-contour-using-opencv-python
# https://pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/
for image in original_images:
    file_name = image.split("\\")[-1]
    print("\nLocation: ",image, " \nfile_name: ", file_name)
        # Read the input image
    img = cv2.imread(image)
    img_original = cv2.imread(image.replace("[1]",""))
    line_thickness = 3
    x1, y1, y2 = 85,0,300
    cv2.line(img, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
    cv2.line(img_original, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
    x1, y1, y2 = 135, 0, 300
    cv2.line(img, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
    cv2.line(img_original, (x1, y1), (x1, y2), (0, 255, 0), thickness=line_thickness)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholding in the gray image to create a binary image
    ret, thresh = cv2.threshold(gray, 150, 255, 0)
    # Find the contours using binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours in image:", len(contours))
    if len(contours) != 3:
        print("not 3 contours")
        break
    areas = []
    for cont in contours:
        # cnt = contours[0]
        cnt = cont
        # compute the area and perimeter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        perimeter = round(perimeter, 4)
        print('Area:', area)
        areas.append(area)
        # print('Perimeter:', perimeter)
        if draw:
            img1 = cv2.drawContours(img, [cnt], -1, (0, 255, 255), 3)
            x1, y1 = cnt[0, 0]
            # cv2.putText(img1, f'Area:{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            # cv2.putText(img1, f'Perimeter:{perimeter}', (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    if draw:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow("Image", img_original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # write to pandas
    if "R" in file_name:
        area_temp = areas[2]
        areas[2] = areas[0]
        areas[0] = area_temp
        side = "Right"
    elif "L"  in file_name:
        side = "Left"
    else:
        print("Not left or right!")
        exit()
    df = df.append({'fileLocation': image, 'file_name': file_name, 'side': side, 'inner':areas[0], 'mid':areas[1] , 'outer':areas[2]},
                   ignore_index=True)
    count +=1
    df.to_csv('.\\data_patients.csv', index=False)
    print("\n count",count)
    # biladeral frontal view

# both focused on normal
#