"""Step 3 of training: split the data into a training part and a test part."""
from sklearn.model_selection import train_test_split

from ml import config


def split_data(X, y):
    return train_test_split(X, y, test_size=config.TEST_SIZE,
<<<<<<< HEAD
                            random_state=config.RANDOM_STATE)
=======
                            random_state=config.RANDOM_STATE)
>>>>>>> origin/master
