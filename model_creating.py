import tensorflow as tf
from dataset import dataset

if __name__ == '__main__':
    dataset = dataset()
    inputs = dataset.inputs
    outputs = dataset.outputs

    model = tf.keras.Sequential([
                tf.keras.layers.Dense(units=256, input_shape=(9,), activation='relu'),
                tf.keras.layers.Dropout(0.1),
                tf.keras.layers.Dense(units=256, activation='relu'),
                tf.keras.layers.Dropout(0.1),
                tf.keras.layers.Dense(units=9, activation='sigmoid')])
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mean_squared_error')
    model.fit(inputs, outputs, epochs=200, validation_split=0.1)
    model.save('model_file')
