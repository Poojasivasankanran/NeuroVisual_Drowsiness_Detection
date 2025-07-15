# File: utils/transformer_utils.py
# Helper functions for formatting sequences for Transformer input

import numpy as np

def create_positional_encoding(seq_len, d_model):
    """
    Generates sinusoidal positional encoding matrix.
    """
    pos = np.arange(seq_len)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
    angle_rads = pos * angle_rates

    # Apply sin to even indices and cos to odd indices
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    
    return angle_rads

def prepare_sequence_window(data_list, seq_len=30):
    """
    Pads or trims blink sequences to match Transformer input size.
    """
    data = np.array(data_list[-seq_len:])  # Take last seq_len items
    if len(data) < seq_len:
        padding = np.zeros((seq_len - len(data), data.shape[1]))
        data = np.vstack((padding, data))
    return data.reshape(1, seq_len, -1)
