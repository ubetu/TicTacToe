import tensorflow as tf
import numpy as np
tf.autograph.set_verbosity(0)

class neuro_model:
    def __init__(self):

        self.ai = tf.keras.models.load_model('model_file')
    def best_move(self, ttt):
        prediction = self.ai.predict(np.array([ttt.board.flatten()]))
        best_move, best_score = (), -1
        for y in range(3):
            for x in range(3):
                if (y, x) in ttt.valid_moves:
                    if (score := prediction[0][x + 3 * y]) > best_score:
                        best_score = score
                        best_move = (y,x)
        return best_score, best_move

