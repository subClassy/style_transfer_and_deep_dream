import cv2

def load_image(path):
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=350)
    # convert from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image)
    return image