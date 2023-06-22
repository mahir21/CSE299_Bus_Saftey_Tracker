from flask import Flask, render_template, jsonify
import cv2
import pandas as pd
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR//tesseract'
#import main


app = Flask(__name__)

def check_plate_safety(csv_file, plate_number):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Iterate over each row in the DataFrame

    plate_number = plate_number.strip()

    for index, row in df.iterrows():

        if str(row ['Number Plate']).lower() == plate_number.lower(

        ):

            return row['Vehicle Saftey Index']

    # Plate number not found
    return None

def process_image():
    #taking our image input and resizing it's width to 300 pixels
    image = cv2.imread('D:/NumberPlateDetector/image/test.jpg')

    image = imutils.resize(image, width=300 )
    cv2.imshow("original image", image)
    cv2.waitKey(0)

    #Converting the image input to grey scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("greyed image", gray_image)
    cv2.waitKey(0)

    #Reducing noise in the image
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    cv2.imshow("smoothened image", gray_image)
    cv2.waitKey(0)

    #Detecing the edges of smoothned image
    edged = cv2.Canny(gray_image, 30, 200)
    cv2.imshow("edged image", edged)
    cv2.waitKey(0)

    #Finding Contours of edge image
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1=image.copy()
    cv2.drawContours(image1,cnts,-1,(0,255,0),3)
    cv2.imshow("contours",image1)
    cv2.waitKey(0)

    #Sorting Identfied Contours
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2,cnts,-1,(0,255,0),3)
    cv2.imshow("Top 30 contours",image2)
    cv2.waitKey(0)

    #Finding Contour With 4 Sides
    i=7
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx

            #Cropping the rectangular part identified as license plate
            x,y,w,h = cv2.boundingRect(c)
            new_img=image[y:y+h,x:x+w]
            cv2.imwrite('./'+str(i)+'.png',new_img)
            i+=1

            #Drawing the selected contour on the original image
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
            cv2.imshow("image with detected license plate", image)
            cv2.waitKey(0)

            #Extracting text from the image of the cropped license plate
            plate = pytesseract.image_to_string(new_img, lang='eng')
            print("Number plate is:", plate)
            csv_file = r'C:\Users\USER\Desktop\CSE299Project\299Train.csv'  # Use raw string (r) to avoid escape characters

            # Specify the plate number to check


            # Call the function to check the plate safety index
            safety_index = check_plate_safety(csv_file, str(plate) )
            #print(safety_index)

            #
           # if safety_index is not None:
                #print(f"The safety index for plate number {plate} is {safety_index}.")
            #else:
               # print("No matching plate number found.")

            cv2.imshow("cropped", new_img)
            cv2.waitKey(0)

# Prepare the response as a JSON object
    response = {
        "plate_number": "",
        "safety_index": 8
    }

    return jsonify(response)



cv2.destroyAllWindows()


@app.route("/")
def home():
    # Call the image processing route to get the result
    result = app.test_client().get('/process_image')
    result_json = result.json

    # Pass the result to the template
    return render_template("index.html", result=result_json)





# @app.route("/")
# def home():
#     code = 1234
#
#     return render_template("index.html", code=code)


if __name__ == "__main__":
    app.run(debug=True)



#2nd Test Code For The Function
# from flask import Flask, render_template
# import cv2
# import pandas as pd
# import imutils
# import pytesseract
#
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
#
# app = Flask(__name__)
#
# def check_plate_safety(csv_file, plate_number):
#     # Read the CSV file into a pandas DataFrame
#     df = pd.read_csv(csv_file)
#
#     # Iterate over each row in the DataFrame
#     for index, row in df.iterrows():
#         if str(row['Number Plate']).lower() == plate_number.lower():
#             return row['Vehicle Safety Index']
#
#     # Plate number not found
#     return None
#
# def process_image():
#     # Taking the image input and resizing its width to 300 pixels
#     image = cv2.imread('D:/NumberPlateDetector/image/test.jpg')
#     image = imutils.resize(image, width=300)
#
#     # Converting the image input to grayscale
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Reducing noise in the image
#     gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
#
#     # Detecting the edges of the smoothed image
#     edged = cv2.Canny(gray_image, 30, 200)
#
#     # Finding contours of the edge image
#     cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
#     screenCnt = None
#
#     # Finding contour with 4 sides
#     i = 7  # Initialize i here
#     for c in cnts:
#         perimeter = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
#         if len(approx) == 4:
#             screenCnt = approx
#
#             # Cropping the rectangular part identified as the license plate
#             x, y, w, h = cv2.boundingRect(c)
#             new_img = image[y:y+h, x:x+w]
#             cv2.imwrite('./' + str(i) + '.png', new_img)
#             i += 1
#
#             # Drawing the selected contour on the original image
#             cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
#
#             # Extracting text from the image of the cropped license plate
#             plate = pytesseract.image_to_string(new_img, lang='eng')
#             print("Number plate is:", plate)
#             csv_file = r'C:\Users\USER\Desktop\CSE299Project\299Train.csv'  # Use raw string (r) to avoid escape characters
#
#             # Call the function to check the plate safety index
#             safety_index = check_plate_safety(csv_file, str(plate))
#
#             return plate, safety_index
#
#     return None, None
#
# @app.route("/")
# def home():
#     # Call the image processing function to get the result
#     plate, safety_index = process_image()
#
#     # Pass the plate number and safety index to the template
#     return render_template("index.html", plate_number=1234, safety_index=1)
