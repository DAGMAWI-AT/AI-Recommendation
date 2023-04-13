import pandas as pd
import numpy as np


from sklearn.decomposition import TruncatedSVD

from flask import Flask, jsonify

app = Flask(__name__)

columns = ['id','user_id','product_id','rating','status']
product_reviews = pd.read_csv('product_reviews.csv',sep='\t', names=columns)

columns = ['id','title','slug','stock','size','condition','status','purchasing','price','discount','is_featured','Catagories','child_id','brand']
products = pd.read_csv('products.data.csv' , encoding='latin-1',names=columns)

merged_data = pd.merge(product_reviews,products, on='id')

data_pivot_table = merged_data.pivot_table(index='user_id',values='rating', columns ='title',fill_value=0)

transposed_data = data_pivot_table.values.T

SVD = TruncatedSVD(n_components=12)
resultant_matrix = SVD.fit_transform(transposed_data)

correlation_matrix = np.corrcoef(resultant_matrix)

titles = data_pivot_table.columns
products_list = list(titles)
 # list of all movies




@app.route('/<string:title>', methods=['GET'])
def get_recommendation(title):
    if title in products_list:
        products_index = products_list.index(title)
        products_corr = correlation_matrix[products_index]
        recommendation = list(titles[(products_corr > 0.7) & (products_corr < 1)])
        return jsonify(recommendation)
    else:
       return "Error: product not on the list", 404
    
if __name__ == '__main__':
    app.run(debug=True)