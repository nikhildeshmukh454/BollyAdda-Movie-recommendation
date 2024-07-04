import numpy as np
import pandas as pd

data = pd.read_csv("IMDB-Movie-Dataset(2023-1951) (2).csv")

# Randomly sample 100 movie names
sampled_data = data.sample(n=100)

for name in sampled_data['movie_name']:
    print(f'<option value="{name}">{name}</option>')

