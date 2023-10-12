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

def get_heatmap_updater():
    inputs = layers.Input((1024, 1024, 2))
    x = layers.Conv2D(8, 16, 1, "same", activation="relu")(inputs)
    x = layers.Conv2D(8, 8, 1, "same", activation="relu")(x)
    x = layers.Conv2D(8, 8, 1, "same", activation="relu")(x)
    x = layers.Conv2D(8, 8, 1, "same", activation="relu")(x)
    x = layers.Conv2D(1, 4, 1, "same", activation="sigmoid", activity_regularizer=regularizers.l1_l2())(x)

    m = models.Model(inputs=inputs, outputs=x, name="heatmapper")
    m.summary()
    return m

def get_reader():
    img_input = layers.Input((1024, 1024, 1))
    prev_pred = layers.Input((EMB_DIM, ))
    x = layers.Conv2D(8, 16, activation="relu")(img_input)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Conv2D(8, 8, 2, activation="relu")(x)
    x = layers.Flatten()(x)

    x = layers.Dense(2 * EMB_DIM, activation="tanh")(x)
    x = layers.Concatenate()([x, prev_pred])

    x = layers.Dense(EMB_DIM, activation="softmax")(x)

    m = models.Model(inputs=[img_input, prev_pred], outputs=x, name="reader")
    m.summary()
    return m


DRST_PATH = "/home/aman/drst"
NUM_SAMPLES = 20000


heatmapper = get_heatmap_updater()
reader = get_reader()

map_opt = optimizers.Adam(learning_rate=0.00001)
read_opt = optimizers.Adam(learning_rate=0.00001)


def train(steps=1000):
    for i in range(steps):

        with tf.GradientTape() as map_tape, tf.GradientTape() as read_tape:
            
            valid = False
            while not valid:
                try:
                    pick = random.randint(0, NUM_SAMPLES-1)
                    y_true = open(f"{DRST_PATH}/texts/{pick}.txt", "r").read()
                    img = cv2.imread(f"{DRST_PATH}/pngs/doc{pick}.png", cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (1024, 1024))
                    img = tf.convert_to_tensor(img, dtype=tf.dtypes.float32) / 255.
                    img = tf.expand_dims(img, axis=-1)
                    valid = True
                    
                except Exception as e:
                    pass
            
            y_true = [embeddings[c] for c in y_true] + [embeddings["end"]]
            y_true = y_true[:5]

            map = tf.zeros_like(img)
            pred = embeddings["start"]
            pred = tf.expand_dims(pred, 0)
            inp = tf.concat([img, map], axis=-1)
            inp = tf.expand_dims(inp, 0)

            preds = []
            for j, _ in enumerate(y_true):
                map = heatmapper(inp)
                plt.imshow((tf.multiply(map, img)).numpy()[0], vmin=0, vmax=1)
                cv2.imwrite(f"maps/{i}_{j}.png", tf.multiply(map, img).numpy()[0] * 255.)
                pred = reader([tf.multiply(map, img), pred])

                preds.append(pred[0])
            
            total_loss = sum([losses.categorical_crossentropy(true, pred) for pred, true in zip(preds, y_true)])
            print(i, float(total_loss))
            
            map_grads = map_tape.gradient(total_loss, heatmapper.trainable_variables)
            read_grads = read_tape.gradient(total_loss, reader.trainable_variables)

            map_opt.apply_gradients(zip(map_grads, heatmapper.trainable_variables))
            read_opt.apply_gradients(zip(read_grads, reader.trainable_variables))

train()