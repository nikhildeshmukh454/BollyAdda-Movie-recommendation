import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

class KNN:
    def __init__(self):
        pass

    def process_genres_and_casts(self, df, genre_col, cast_col, direct_col):
        def expand_genres_casts(row):
            genres = row[genre_col].split(', ')
            casts = row[cast_col].split(', ')
            direct = row[direct_col].split(',')

            while len(genres) < 3:
                genres.append(genres[-1])
            while len(casts) < 4:
                casts.append(casts[-1])

            selected_genres = genres[:3]
            selected_casts = casts[:4]
            selected_direct = direct[0]

            return selected_genres + selected_casts + [selected_direct]

        expanded_cols = df.apply(expand_genres_casts, axis=1, result_type='expand')
        expanded_cols.columns = ['genre1', 'genre2', 'genre3', 'cast1', 'cast2', 'cast3', 'cast4', 'direct']
        result_df = pd.concat([df, expanded_cols], axis=1)

        return result_df

    def predict(self, data, movie_name):
        Year = data[['year']]
        data1 = data.drop(['year', 'movie_id'], axis=1)
        data1_processed = self.process_genres_and_casts(data1, 'genre', 'cast', 'director')
        data1_processed.drop(['genre', 'cast', 'director'], axis=1, inplace=True)
        data1_processed = pd.concat([data1_processed, Year], axis=1)

        self.label_encoder = LabelEncoder()

        for column in ['genre1', 'genre2', 'genre3', 'cast1', 'cast2', 'cast3', 'cast4', 'direct', 'year']:
            data1_processed[column] = self.label_encoder.fit_transform(data1_processed[column])

        self.data1 = data1_processed  # Store preprocessed data for later use
        self.data = data  # Store original data for later use
        
        # Create mapping of movie names to indices
        self.moviemap = {movie: index for index, movie in data['movie_name'].items()}

        point = self.moviemap[movie_name]
        testcase = self.data1.iloc[point]

        nbg = {}
        for index, row in self.data1.iterrows():
            dis = 0
            for i in range(2, 11):
                feature_value_row = int(row[i])
                feature_value_testcase = int(testcase[i])

                if isinstance(feature_value_row, (int, float)) and isinstance(feature_value_testcase, (int, float)):
                    dis += (feature_value_row - feature_value_testcase) ** 2
                else:
                    print(f"Non-numeric value encountered: row[{i + 2}]={feature_value_row}, testcase[{i + 2}]={feature_value_testcase}")

            nbg[index] = dis ** 0.5  # Calculate the Euclidean distance for each row

        nbg = dict(sorted(nbg.items(), key=lambda item: item[1]))
        first_10_values = list(nbg.keys())[:10] 
        
        # Collect details of the top 10 movies
        top_movies_str = ""
        for index in first_10_values:
            if index in self.data.index:
                movie_details = self.data.loc[index]
                top_movies_str += (
                    f"Movie Name: | {movie_details['movie_name']} | "
                    f"Year: | {movie_details['year']} | "
                    f"Genre: | {movie_details['genre']} | "
                    f"Director: | {movie_details['director']} | "
                    f"Cast: | {movie_details['cast']} | "
                    "?"
                )
            else:
                print(f"Index {index} not found in data")

        return top_movies_str

# Load the dataset
data = pd.read_csv("IMDB-Movie-Dataset(2023-1951) (2).csv")

# Create an instance of the KNN class
knn_model = KNN()

# print(knn_model.predict(data=data,movie_name="Student of the Year 2"))

# Save the model to a pickle file
with open('knn_obj.pkl', 'wb') as file:
    pickle.dump(knn_model, file)
