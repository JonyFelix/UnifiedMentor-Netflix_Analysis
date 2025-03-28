
'''

TO RUN IN PROGRAM AND OBTAIN VISUALZATIONS
STEP 1 DOWNLOAD THE FILE FROM DATA SET FOLDER
STEP 2 CHANGE THE df PATH TO YOUR FILE LOCATION
STEP 3 RUN THE CODE (COLAB,JUPYTER NOTEBOOK OR ANY OTHER ENVIROMENT)

'''

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def main():
    print("Welcome to My Project!\nNETFLIX DATA ANALYSIS")


    file_path = "netflix1.csv"  # Update this with the correct path
    net = pd.read_csv(file_path)

    net.head(20)


    # Count of Movies vs. TV Shows
    typeof = net['type'].value_counts()

    # Plot the distribution (Fixed Warning)
    plt.figure(figsize=(7, 5))
    sns.barplot(x=typeof.index, y=typeof.values, hue=typeof.index, palette='Set2', legend=False)
    plt.title("Distribution of Content by Type")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.show()



    # 2. Top 10 Genres
    net['genres'] = net['listed_in'].apply(lambda x: x.split(', '))
    all_genres = sum(net['genres'], [])  # Flatten the list
    genre_counts = Counter(all_genres)   # Count occurrences
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=genre_df['Count'].head(10), y=genre_df['Genre'].head(10), hue=genre_df['Genre'].head(10), palette='coolwarm', legend=False)
    plt.title("Top 10 Genres on Netflix")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.show()

    # 3. Films Released Over the Years
    yearly_additions = net['release_year'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=yearly_additions.index, y=yearly_additions.values, marker='o', color='red')
    plt.title("Films Released Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Films")
    plt.grid(True)
    plt.show()

    # 4. Top 10 Directors (Excluding "Not Given")
    filtered_net = net[net['director'] != "Not Given"]
    top_directors = filtered_net['director'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(y=top_directors.index, x=top_directors.values, hue=top_directors.index, palette='Blues_d', legend=False)
    plt.title("Top 10 Directors with Most Films on Netflix")
    plt.xlabel("Number of Films")
    plt.ylabel("Director")
    plt.show()

    # 5. Movie Duration Distribution
 
    # Convert 'duration' column to string before replacing 'min'
    net['duration'] = net['duration'].astype(str).str.replace(' min', '', regex=False)
    net['duration'] = pd.to_numeric(net['duration'], errors='coerce')  # Convert to number

    # Filter only movies (since TV Shows have 'Seasons' instead of duration in minutes)
    movies = net[net['type'] == 'Movie']

    # Plot distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(movies['duration'].dropna(), bins=30, kde=True, color='purple')
    plt.title("Movie Duration Distribution on Netflix")
    plt.xlabel("Duration (Minutes)")
    plt.ylabel("Count")
    plt.show()

    # 6. Most Popular Genres in Top 5 Countries
    net_exploded = net.assign(genres=net['listed_in'].str.split(', ')).explode('genres')
    top_countries = net['country'].value_counts().head(5).index
    filtered_net = net_exploded[net_exploded['country'].isin(top_countries)]
    genre_by_country = filtered_net.groupby(['country', 'genres']).size().reset_index(name='count')
 
    plt.figure(figsize=(25, 6))
    sns.barplot(x='genres', y='count', hue='country', data=genre_by_country, palette='Set1')
    plt.xticks(rotation=45)
    plt.title("Most Popular Genres in Top 5 Content-Producing Countries")
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.legend(title="Country")
    plt.show()

    # 7. Netflix Content Additions by Month
    # Convert 'date_added' to datetime first
    net['date_added'] = pd.to_datetime(net['date_added'], format='%d-%m-%Y', errors='coerce')

    net['month_added'] = net['date_added'].dt.month
    monthly_additions = net['month_added'].value_counts().sort_index()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_data = pd.DataFrame({"Month": months, "Count": monthly_additions.values})

    plt.figure(figsize=(12, 6))
    sns.barplot(x="Month", y="Count", hue="Month", data=monthly_data, palette='coolwarm', legend=False)
    plt.title("Netflix Content Additions by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Titles Added")
    plt.show()
 
 

if __name__ == "__main__":
   main()
