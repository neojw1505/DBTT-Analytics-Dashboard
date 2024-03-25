from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the data and preprocess it
df = pd.read_csv('./mattressrecommender.csv')
df.fillna(0, inplace=True)
item_names = df.columns[2:]

gender_encoder = OneHotEncoder()
gender_encoded = gender_encoder.fit_transform(df[['gender']])
gender_df = pd.DataFrame(gender_encoded.toarray(), columns=gender_encoder.categories_[0])
df_encoded = pd.concat([df.drop('gender', axis=1), gender_df], axis=1)

scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df_encoded)

# Images and prices dictionaries
images = {
    "aster": "https://shop.fourstar.com.sg/cdn/shop/products/DETENSEwebsitebedimagesbr.jpg?v=1606818855",
    "arrio": "https://shop.fourstar.com.sg/cdn/shop/products/DETENSEwebsitebedimagesarrioBR.jpg?v=1606818875",
    "apline": "https://shop.fourstar.com.sg/cdn/shop/products/DETENSEwebsitebedimagesaplineBR.jpg?v=1606818699",
    "aura": "https://shop.fourstar.com.sg/cdn/shop/products/DETENSEwebsitebedimagesbr.jpg?v=1606818855",
    "akoni": "https://shop.fourstar.com.sg/cdn/shop/products/DETENSEwebsitebedimagesakoniBR.jpg?v=1606818608"
}

prices = {
    "arrio_s": 1099.0,
    "arrio_ss": 1199.0,
    "arrio_q": 1599.0,
    "arrio_k": 1899.0,
    "aura_s": 1399.0,
    "aura_ss": 1599.0,
    "aura_q": 1999.0,
    "aura_k": 2299.0,
    "aster_s": 1599.0,
    "aster_ss": 1699.0,
    "aster_q": 2299.0,
    "aster_k": 2599.0,
    "akoni_s": 1899.0,
    "akoni_ss": 2099.0,
    "akoni_q": 2899.0,
    "akoni_k": 3399.0,
    "apline_s": 2399.0,
    "apline_ss": 2599.0,
    "apline_q": 3699.0,
    "apline_k": 4299.0
}

markup_percentage = 0.05  # 4% markup from ideal

pmp = {
    "arrio_s": 1099.0 * (1 - markup_percentage),
    "arrio_ss": 1199.0 * (1 - markup_percentage),
    "arrio_q": 1599.0 * (1 - markup_percentage),
    "arrio_k": 1899.0 * (1 - markup_percentage),
    "aura_s": 1399.0 * (1 - markup_percentage),
    "aura_ss": 1599.0 * (1 - markup_percentage),
    "aura_q": 1999.0 * (1 - markup_percentage),
    "aura_k": 2299.0 * (1 - markup_percentage),
    "aster_s": 1599.0 * (1 - markup_percentage),
    "aster_ss": 1699.0 * (1 - markup_percentage),
    "aster_q": 2299.0 * (1 - markup_percentage),
    "aster_k": 2599.0 * (1 - markup_percentage),
    "akoni_s": 1899.0 * (1 - markup_percentage),
    "akoni_ss": 2099.0 * (1 - markup_percentage),
    "akoni_q": 2899.0 * (1 - markup_percentage),
    "akoni_k": 3399.0 * (1 - markup_percentage),
    "apline_s": 2399.0 * (1 - markup_percentage),
    "apline_ss": 2599.0 * (1 - markup_percentage),
    "apline_q": 3699.0 * (1 - markup_percentage),
    "apline_k": 4299.0 * (1 - markup_percentage)
}

# Dictionary mapping short form sizes to full words
size_mapping = {'s': 'single', 'ss': 'super single', 'q': 'queen', 'k': 'king'}

def map_to_csv_header(item):
    model, size = item['model'], item['size']
    return f"{model}_{size_mapping.get(size, size)}"

def map_to_csv_header(item):
    model, size = item['model'], item['size']
    # Convert size to the appropriate abbreviation
    size_abbreviation = {'single': 's', 'super single': 'ss', 'queen': 'q', 'king': 'k'}.get(size.lower(), size.lower())
    return f"{model}_{size_abbreviation}"

unique_models = set(model.split('_')[0] for model in df.columns[2:])

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify({"models": list(unique_models)})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get user profile from JSON request body
        user_profile = request.json
        
        # Aggregate purchased items into a single dictionary
        items_bought = {}
        for item in user_profile['items_bought']:
            item_key = map_to_csv_header(item)
            items_bought[item_key] = 1  # Assuming each item is bought once
        
        user_profile['items_bought'] = items_bought

        # Convert gender to one-hot encoding
        user_gender_encoded = gender_encoder.transform([[user_profile['gender']]]).toarray()[0]

        # Create user profile vector
        user_profile_vector = [user_profile['age']] + list(user_gender_encoded)
        user_items_bought = user_profile['items_bought']
        for item in item_names:
            if item in user_items_bought:
                user_profile_vector.append(user_items_bought[item])
            else:
                user_profile_vector.append(0)

        # Scale the user profile vector
        user_profile_scaled = scaler.transform([user_profile_vector])

        # Find most similar users
        similarities = cosine_similarity(user_profile_scaled, df_scaled)
        similar_indices = similarities[0].argsort()[::-1]

        # Top recommendation
        top_index = similar_indices[1]  # Exclude user's own index
        top_recommendation = df.iloc[top_index][item_names].tolist()
        cosine_similarity_of_top = similarities[0][top_index]

        # Get recommended items based on top recommendation
        recommended_items = []
        for i, item in enumerate(item_names):
            if top_recommendation[i] == 1:
                recommended_items.append({
                    "model": item.split('_')[0], 
                    "size": size_mapping.get(item.split('_')[1], item.split('_')[1]), 
                    "image_url": images.get(item.split('_')[0], ""), 
                    "price": prices.get(item, "Price not available"),
                    "profit_maximising_price": pmp.get(item, "Unavailable")
                })

        return jsonify({
            "recommendation": recommended_items,
            "cosine_similarity": cosine_similarity_of_top
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5002)

