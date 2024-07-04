import pandas as pd
import pickle

class Filter:
    def __init__(self):
        self.Cast = "none"
        self.Director = "none"
        self.Genre = "none"
        self.Year = "none"
        self.Dic = {}
        self.top_movies = []

    def TOP(self, cast="none", director="none", genre="none", year="none", data=None):
        # Convert all inputs to strings
        self.Cast = str(cast)
        self.Director = str(director)
        self.Genre = str(genre)
        self.Year = str(year)
        self.Dic = {}

        if data is not None:
            # Create a new column with lists of cast members
            data['cast_list'] = data['cast'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
            self.top_movies = self.filter_data(data)
        return self.top_movies_to_string()
    
    def filter_data(self, data):
        # Apply filtering logic
        for index, row in data.iterrows():
            if self.Cast != "none" and self.Cast in row['cast_list']:
                self.update_dic(index, row['cast'])
            if self.Genre != "none" and self.Genre in row['genre']:
                self.update_dic(index, row['cast'])

        sorted_dic = sorted(self.Dic.items(), key=lambda x: x[1], reverse=True)
        top_movies = [
            (
                data.loc[index, 'movie_name'], 
                data.loc[index, 'year'], 
                data.loc[index, 'overview'], 
                data.loc[index, 'director'], 
                data.loc[index, 'cast']
            ) 
            for index, _ in sorted_dic[:10]  # Get the top 10 movies
        ]
        return top_movies

    def update_dic(self, index, cast):
        if index in self.Dic:
            self.Dic[index][0] += 1
        else:
            self.Dic[index] = [1, cast]

    def top_movies_to_string(self):
        if not self.top_movies:
            return "No top movies found."

        result = ""
        for movie in self.top_movies:
            result += (
                f"Movie Name: |  {movie[0]} | "
                f"Year: |  {movie[1]} | "
                f"Overview: |  {movie[2]} | "
                f"Director: |  {movie[3]} | "
                f"Cast: |  {movie[4]} | "
                "?"
            )
        return result

# Example usage
data = pd.read_csv("IMDB-Movie-Dataset(2023-1951) (2).csv")
recommender = Filter()

# Save the model to a pickle file
with open('filter_obj.pkl', 'wb') as file:
    pickle.dump(recommender, file)
