import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
import numpy as np
import h5py
import json
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import deserialize as deserialize_layer
from tensorflow.keras.optimizers import deserialize as deserialize_optimizer
from tensorflow.keras.utils import get_custom_objects

def load_model(filepath, custom_objects=None, compile=True):
    """
    Simplified version of TensorFlow's load_model function.
    Supports loading models saved in HDF5 format.
    """
    # Open the HDF5 file
    with h5py.File(filepath, 'r') as f:
        # Load the model configuration
        model_config = f.attrs.get('model_config')
        if model_config is None:
            raise ValueError('No model found in the file.')
        
        # Parse the model configuration
        model_config = json.loads(model_config.decode('utf-8'))
        
        # Register custom objects
        if custom_objects is not None:
            get_custom_objects().update(custom_objects)
        
        # Reconstruct the model architecture
        model = Model.from_config(model_config, custom_objects=custom_objects)
        
        # Load the model weights
        if 'model_weights' in f:
            weight_values = []
            for layer_name in model.layers:
                if layer_name in f['model_weights']:
                    layer_group = f['model_weights'][layer_name]
                    weights = [np.array(layer_group[weight]) for weight in layer_group]
                    weight_values.append(weights)
            
            # Set the weights for each layer
            model.set_weights(weight_values)
        
        # Load the optimizer and compile the model if requested
        if compile and 'training_config' in f.attrs:
            training_config = f.attrs['training_config']
            training_config = json.loads(training_config.decode('utf-8'))
            
            # Reconstruct the optimizer
            optimizer_config = training_config['optimizer_config']
            optimizer = deserialize_optimizer(optimizer_config, custom_objects=custom_objects)
            
            # Compile the model
            model.compile(
                optimizer=optimizer,
                loss=training_config['loss'],
                metrics=training_config['metrics'],
                loss_weights=training_config['loss_weights'],
                weighted_metrics=training_config['weighted_metrics'],
            )
        
        return model
    
# Custom Dice Loss function
def dice_loss(y_true, y_pred):
    smooth = 1e-6  # Smoothing constant to avoid division by zero
    intersection = tf.reduce_sum(tf.multiply(y_true, y_pred))
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    dice = (2. * intersection + smooth) / (union + smooth)
    return 1 - dice  # Return 1 - Dice coefficient for loss

# Load the pre-trained classification model (e.g., MobileNet)
def load_classification_model(model_path):
    model = load_model(model_path)
    return model

# Define the segmentation model (e.g., U-Net architecture)
def build_segmentation_model(input_size=(256, 256, 3)):
    inputs = Input(input_size)

    # Encoding path
    c1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    p1 = MaxPooling2D((2, 2))(c1)
    
    c2 = Conv2D(64, (3, 3), activation='relu', padding='same')(p1)
    p2 = MaxPooling2D((2, 2))(c2)
    
    c3 = Conv2D(128, (3, 3), activation='relu', padding='same')(p2)
    p3 = MaxPooling2D((2, 2))(c3)
    
    c4 = Conv2D(256, (3, 3), activation='relu', padding='same')(p3)
    p4 = MaxPooling2D((2, 2))(c4)

    # Bottleneck
    bottleneck = Conv2D(512, (3, 3), activation='relu', padding='same')(p4)

    # Decoding path
    u1 = UpSampling2D((2, 2))(bottleneck)
    c5 = Conv2D(256, (3, 3), activation='relu', padding='same')(u1)
    u2 = concatenate([c5, c4], axis=-1)

    u2 = UpSampling2D((2, 2))(u2)
    c6 = Conv2D(128, (3, 3), activation='relu', padding='same')(u2)
    u3 = concatenate([c6, c3], axis=-1)

    u3 = UpSampling2D((2, 2))(u3)
    c7 = Conv2D(64, (3, 3), activation='relu', padding='same')(u3)
    u4 = concatenate([c7, c2], axis=-1)

    u4 = UpSampling2D((2, 2))(u4)
    c8 = Conv2D(32, (3, 3), activation='relu', padding='same')(u4)
    u5 = concatenate([c8, c1], axis=-1)

    # Output layer
    output = Conv2D(1, (1, 1), activation='sigmoid')(u5)

    # Create the model
    model = tf.keras.Model(inputs, output)

    # Compile the model
    model.compile(optimizer=Adam(), loss=dice_loss, metrics=[dice_loss])

    return model

# Function to load the segmentation model
def load_segmentation_model(model_path):
    model = load_model(model_path, custom_objects={'dice_loss': dice_loss})
    return model

# Save and load the model functions
def save_model(model, model_path):
    model.save(model_path)

def load_model_from_file(model_path):
    return load_model(model_path, custom_objects={'dice_loss': dice_loss})
