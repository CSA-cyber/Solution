import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import os
import random


def set_seed(seed):
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    random.seed(seed)


seed = 42
set_seed(seed)

def normalize(data):
    """
    Normalizes image dataset
    :param data: Numpy array containing images
    :return: Normalized image array
    """
    return data / 255

def get_neural_network():
    """
    returns an artificial neural network
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
    model.add(tf.keras.layers.Dense(128,activation="relu"))
    model.add(tf.keras.layers.Dense(128,activation="relu"))
    model.add(tf.keras.layers.Dense(10, activation="softmax"))
    return model

def plot_accuracy(history):
    """
    Draws training accuracy graph
    :param history: keras history object
    """
    sns.set(font_scale=1)
    r = lambda x: round(x*100)
    plt.figure(figsize=(7, 4))
    n = len(history.history['accuracy'])
    plt.plot(range(1, n+1), [r(x) for x in history.history['accuracy']], 'red', linewidth=2, label='train')
    plt.plot(range(1, n+1), [r(x) for x in history.history['val_accuracy']], 'blue', linewidth=2, label='valid')
    plt.xticks(range(1, n+1, 3))
    plt.title(f'Accuracy')
    plt.ylabel('accuracy (%)')
    plt.xlabel('epoch')
    plt.legend(loc='lower right')
    plt.savefig(f'accuracy.png', dpi=200, bbox_inches='tight')

def plot_loss(history):
    """
    Draws training loss graph
    :param history: keras history object
    """
    sns.set(font_scale=1)
    r = lambda x: round(x*100)
    plt.figure(figsize=(7, 4))
    n = len(history.history['loss'])
    plt.plot(range(1, n+1), [r(x) for x in history.history['loss']], 'red', linewidth=2, label='train')
    plt.plot(range(1, n+1), [r(x) for x in history.history['val_loss']], 'blue', linewidth=2, label='valid')
    plt.xticks(range(1, n+1, 3))
    plt.title(f'Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(loc='upper right')
    plt.savefig(f'loss.png', dpi=200, bbox_inches='tight')
    
# loads the mnist dataset
(X_train,y_train),(X_test,y_test)=tf.keras.datasets.mnist.load_data()

# normalizing dataset
X_train = normalize(X_train)
X_test = normalize(X_test)

# one hot encoding labels for training
y_train = tf.keras.utils.to_categorical(y_train)

# initilizing and setting optimizers
model = get_neural_network()
optimizer = tf.keras.optimizers.Adam(1e-4)
metrics = ['accuracy']
model.compile(loss="categorical_crossentropy",optimizer=optimizer,metrics=metrics)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_accuracy'),
    tf.keras.callbacks.ModelCheckpoint(f'nn.h5',
                    monitor='val_accuracy', save_best_only=True)
]

history = model.fit(X_train,y_train,epochs=50, validation_split=0.2, callbacks=callbacks)


plot_accuracy(history)
plot_loss(history)

model = tf.keras.models.load_model('nn.h5')
y_pred = model.predict(X_test)
y_pred = np.argmax(y_pred, axis=1)
print(classification_report(y_test, y_pred, digits=4))