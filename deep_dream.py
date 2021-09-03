import cv2
import imutils
import numpy as np
import tensorflow as tf

def load_image(path):
    image = cv2.imread(path)
    image = imutils.resize(image, width=350)
    # convert from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image)
    return image

def deprocess(image):
    image = 255 * (image + 1.0) 
    image /= 2.0
    image = tf.cast(image, tf.uint8)
    return image

def calculate_loss(img, model):
    img = tf.expand_dims(img, axis=0)
    layer_activations = model(img)

    losses = []
    for activations in layer_activations:
        losses.append(tf.reduce_mean(activations))

    return tf.reduce_sum(losses)

