from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

popular_df = pickle.load(open('popular_df.pkl', "rb"))
pt = pickle.load(open('pt.pkl', "rb"))
books = pickle.load(open('books.pkl', "rb"))
similarity_score = pickle.load(open('similarity_score.pkl', "rb"))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", 
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_rating'].values),
                           )


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    n=10
    
    index= np.where(pt.index==user_input)[0][0]
    distances = similarity_score[index]
    # enumerates gin=ves index in list
    # lambda function for sorting on basis of distances not on index
    # we took top n books
    similar_items = sorted(list(enumerate(distances)), key=lambda x:x[1], reverse=True)[1:n+1]
    data =[]
    for it in similar_items:
        item=[]
        # print(it[0], "  ->  " , pt.index[it[0]])
        temp_df = books[books['Book-Title'] == pt.index[it[0]]]
        # no duplicate books
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    # data has been paased to recoomed.html
    # return data
    return render_template('recommend.html', data=data)

    # print(data)

    # return str(user_input)



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


if __name__ == '__main__':
    app.run(debug=True)