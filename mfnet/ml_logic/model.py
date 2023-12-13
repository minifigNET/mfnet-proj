from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models as keras_models
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import numpy as np


def initialize_model(nb_labels=38): #Function to create a transfer learning model, we can chose number of labels and the base model

    """Create the base model out of DenseNet201"""

    base_model = MobileNetV2()

    # Adding Dropout layer
    x = layers.Dropout(0.5)(base_model.layers[-2].output)

    # Output layer
    outputs = layers.Dense(nb_labels, activation='softmax')(x)

    # Returns model
    return keras_models.Model(base_model.inputs, outputs)


def compile_model(model, learning_rate=0.0001):

    """Compile the model"""

    model.compile(loss = 'sparse_categorical_crossentropy',
             optimizer = Adam(learning_rate=learning_rate),
             metrics = ['accuracy'])

    print("✅ Model compiled")

    return model


def train_model(
    model,
    X_train,
    y_train,
    X_test,
    y_test,
    patience=10
    ):

    """fit the model and return the fitted model and history"""

    es = EarlyStopping(monitor = 'val_accuracy',
                                patience = patience,
                                mode = 'max',
                                restore_best_weights = True)
    history = model.fit(
        X_train,
        y_train,
        validation_data = (X_test,y_test),
        epochs = 100,
        verbose=2,
        shuffle=True,
        batch_size=4,
        callbacks = [es]
        )

    print(f"✅ Model trained with val_accuracy: {round(np.max(history.history['val_accuracy']), 2)}")

    return model,history

def evaluate_model(
        model,
        X,
        y,
    ):

    """Evaluate trained model"""

    if model is None:
        print(f"\n❌ No model to evaluate")
        return None

    metrics = model.evaluate(
        x=X,
        y=y,
        verbose=0,
        return_dict=True
    )
    loss = metrics["loss"]
    accuracy = metrics["accuracy"]

    print(f"✅ Model evaluated, accuracy: {round(accuracy, 2)}")

    return metrics
