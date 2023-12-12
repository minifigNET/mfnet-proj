from tensorflow.keras.applications.densenet import DenseNet201
from tensorflow.keras import layers, models as keras_models
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import numpy as np


def initialize_model(input_shape=(224,224,3),nb_labels=38): #Function to create a transfer learning model, we can chose number of labels and the base model

    """Create the base model out of DenseNet201"""

    base_model = DenseNet201(input_shape = input_shape,
                       include_top = False,
                       weights = 'imagenet',
                       classifier_activation='softmax')

    """disable training from already trained layers"""

    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = layers.Flatten()(x) # Flatten output
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(nb_labels, activation = 'softmax')(x) # Output layer

    print("✅ Model initialized")

    return keras_models.Model(base_model.input,x)


def compile_model(model, learning_rate=0.001):

    """Compile the model"""

    model.compile(loss = 'sparse_categorical_crossentropy',
             optimizer = Adam(learning_rate=learning_rate),
             metrics = ['accuracy'])

    print("✅ Model compiled")

    return model


def train_model(
    model,
    train_flow,
    validation_data,
    patience=10
    ):

    """fit the model and return the fitted model and history"""

    es = EarlyStopping(monitor = 'val_accuracy',
                                patience = patience,
                                mode = 'max',
                                restore_best_weights = True)
    reduce_lr = ReduceLROnPlateau(monitor='val_accuracy', factor=0.2,
                                patience=round(patience/3),
                                min_lr=0.00001)
    history = model.fit(
        train_flow,
        validation_data = validation_data,
        epochs = 100,
        verbose=2,
        callbacks = [es,reduce_lr]
        )

    print(f"✅ Model trained with val_accuracy: {round(np.max(history.history['val_accuracy']), 2)}")

    return model,history
