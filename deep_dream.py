import cv2
import imutils
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import preprocess_input

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


@tf.function
def deep_dream_pass(model, img, step_size, eps=1e-8):
    with tf.GradientTape() as tape:
        tape.watch(img)
        loss = calculate_loss(img, model)
    
    gradients = tape.gradient(loss, img)
    gradients /= tf.math.reduce_std(gradients) + eps 
    img = img + (gradients * step_size)
    img = tf.clip_by_value(img, -1, 1)

    return (loss, img)


def deep_dream_model(model, image, iterations=50, stepSize=0.01):
    image = preprocess_input(image)

    for iteration in range(iterations):
        (loss, image) = deep_dream_pass(model, image, stepSize)

        if iteration % 50 == 0:
            print ("Iteration {} with loss {}".format(iteration, loss))

    return deprocess(image)

names = ["mixed3", "mixed5", "mixed7"]

OCTAVE_SCALE = 1.3
NUM_OCTAVES = 2