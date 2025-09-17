def label_binary(predictions):
    return (predictions > 0).astype(bool)
