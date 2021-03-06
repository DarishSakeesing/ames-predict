import pandas as pd
import numpy as np

def split(df, seed, frac):
    """Split the data into train, test splits
    
    Params:
    df: a pandas dataframe
    seed: a random seed number
    frac: the fraction of train
    """
    train, test = np.split(df.sample(frac=1, random_state=42), [int(.9*len(df))])
    
    return train, test