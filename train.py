import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from keras import layers, models, losses, activations, optimizers, regularizers
import random
import cv2
from matplotlib import pyplot as plt

from stringgen import all_chars


embeddings = list(set(["start", "end"] + all_chars + ["\n", " ", chr(0x0c00 + 77), ".", "?", "!"]))
embeddings = {c: tf.convert_to_tensor([0 if i != j else 1 for i in range(len(embeddings))]) for j, c in enumerate(embeddings)}
EMB_DIM = len(embeddings)


def get_model():
    img_input = layers.Input((1024, 1024, 1))
    map_input = layers.Input((1024, 1024, 1))
    tok_input = layers.Input((EMB_DIM, ))

    cat = layers.Concatenate()([img_input, map_input])
    x = layers.Conv2D(8, 16, 1, "same")(cat)
    x = layers.Conv2D(8, 16, 1, "same")(x)
    x = layers.Conv2D(8, 16, 1, "same")(x)
    new_map = layers.Conv2D(1, 16, 1, "same")(x)
    
    mapped_img = layers.Multiply()([img_input, new_map])
    x = layers.Conv2D(8, 16, 2)(mapped_img)    
    x = layers.Conv2D(8, 16, 2)(x)    
    x = layers.Conv2D(8, 8, 2)(x)    
    x = layers.Conv2D(8, 8, 2)(x)    
    x = layers.Conv2D(8, 4, 2)(x)
    x = layers.Conv2D(8, 4, 2)(x)

    x = layers.Flatten()(x)
    x = layers.Concatenate()([x, tok_input])
    outputs = layers.Dense(EMB_DIM)(x)
        
    m = models.Model(inputs=[img_input, map_input, tok_input], outputs=[outputs, new_map])
    m.summary()
    return m

DRST_PATH = "/home/aman/drst"
NUM_SAMPLES = 20000


model = get_model()

map_opt = optimizers.Adam(learning_rate=0.0001)
read_opt = optimizers.Adam(learning_rate=0.0001)


BATCH_SIZE = 4
def train(steps=2000):
    for i in range(steps):
        opt = optimizers.Adam()

        imgs = []
        batch_y = []

        while len(batch_y) < BATCH_SIZE:
            valid = False
            while not valid:
                try:
                    pick = random.randint(0, NUM_SAMPLES-1)
                    img = cv2.imread(f"{DRST_PATH}/pngs/doc{pick}.png", cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (1024, 1024))
                    img = tf.convert_to_tensor(img, dtype=tf.dtypes.float32) / 255.
                    img = -img + 1.
                    img = tf.expand_dims(img, axis=-1)
                    
                    y_true = open(f"{DRST_PATH}/texts/{pick}.txt", "r").read()
                    y_true = y_true.strip()
                    y_true = [embeddings[c] for c in y_true] + [embeddings["end"]]
                    y_true = y_true[:5]

                    imgs.append(img)
                    batch_y.append(y_true)
                    valid = True

                except Exception as _:
                    pass
                    
        imgs = tf.convert_to_tensor(imgs)
        batch_y = tf.convert_to_tensor(batch_y)
        
        with tf.GradientTape() as tape:
            maps = tf.zeros_like(imgs)
            toks = tf.convert_to_tensor([embeddings["start"] for _ in range(BATCH_SIZE)])

            preds = []
            for _ in range(len(batch_y[0])):
                toks, maps = model([imgs, maps, toks])
                preds.append(toks)
            
            preds = tf.convert_to_tensor(preds)
            preds = tf.transpose(preds, perm=[1, 0, 2])

            loss = losses.categorical_crossentropy(batch_y, preds)

            grads = tape.gradient(loss, model.trainable_variables)
            opt.apply_gradients(grads, model.trainable_variables)

        print(i, float(tf.reduce_sum(loss)))

train()