from flask import Flask, render_template, request
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the vader_lexicon for sentiment analysis
nltk.download("vader_lexicon")

app = Flask(__name__)

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Enhanced food database with ingredients



    # Enhanced food database with ingredients
food_database = {
    "happy": {
        "vegetarian": {
            "diabetes": [
                {"name": "Low-Sugar Fruit Salad", "ingredients": ["fruits", "honey"]},
                {"name": "Grilled Veggie Platter", "ingredients": ["zucchini", "bell peppers", "olive oil"]}
            ],
            "none": [
                {"name": "Ice Cream Sundae", "ingredients": ["milk", "sugar", "cashews"]},
                {"name": "Chocolate Cake", "ingredients": ["flour", "cocoa", "milk"]},
                {"name": "Vegetarian Pizza", "ingredients": ["cheese", "tomato", "flour"]}
            ]
        },
        "non_vegetarian": {
            "diabetes": [
                {"name": "Grilled Chicken Salad", "ingredients": ["chicken", "lettuce", "olive oil"]},
                {"name": "Baked Salmon", "ingredients": ["salmon", "lemon", "herbs"]}
            ],
            "none": [
                {"name": "Pepperoni Pizza", "ingredients": ["pepperoni", "cheese", "flour"]},
                {"name": "Chicken Burger", "ingredients": ["chicken", "bun", "lettuce"]},
                {"name": "Shrimp Tacos", "ingredients": ["shrimp", "tortilla", "salsa"]}
            ]
        }
    },
    "sad": {
        "vegetarian": {
            "diabetes": [
                {"name": "Quinoa Salad", "ingredients": ["quinoa", "cucumber", "mint"]},
                {"name": "Steamed Broccoli Bowl", "ingredients": ["broccoli", "garlic", "lemon"]}
            ],
            "none": [
                {"name": "Mac and Cheese", "ingredients": ["pasta", "cheese", "milk"]},
                {"name": "Vegetable Soup", "ingredients": ["carrots", "potatoes", "onions"]},
                {"name": "Garlic Breadsticks", "ingredients": ["flour", "garlic", "butter"]}
            ]
        },
        "non_vegetarian": {
            "diabetes": [
                {"name": "Turkey Lettuce Wraps", "ingredients": ["turkey", "lettuce", "avocado"]},
                {"name": "Grilled Fish Tacos", "ingredients": ["fish", "cabbage", "lime"]}
            ],
            "none": [
                {"name": "Chicken Alfredo", "ingredients": ["chicken", "pasta", "cream"]},
                {"name": "Beef Stroganoff", "ingredients": ["beef", "mushrooms", "cream"]},
                {"name": "Fried Chicken", "ingredients": ["chicken", "flour", "oil"]}
            ]
        }
    },
    "angry": {
        "vegetarian": {
            "diabetes": [
                {"name": "Spicy Lentil Soup", "ingredients": ["lentils", "tomatoes", "spices"]},
                {"name": "Chili Stir-Fried Veggies", "ingredients": ["broccoli", "carrots", "chili sauce"]}
            ],
            "none": [
                {"name": "Chili Cheese Fries", "ingredients": ["potatoes", "cheese", "chili"]},
                {"name": "Spicy Paneer Wrap", "ingredients": ["paneer", "tortilla", "spices"]},
                {"name": "Stuffed Bell Peppers", "ingredients": ["bell peppers", "cheese", "rice"]}
            ]
        },
        "non_vegetarian": {
            "diabetes": [
                {"name": "Spicy Grilled Shrimp", "ingredients": ["shrimp", "garlic", "spices"]},
                {"name": "Hot Chicken Wings", "ingredients": ["chicken", "hot sauce", "butter"]}
            ],
            "none": [
                {"name": "Buffalo Chicken Pizza", "ingredients": ["chicken", "cheese", "buffalo sauce"]},
                {"name": "Spicy Beef Kebabs", "ingredients": ["beef", "onions", "spices"]},
                {"name": "Peri-Peri Chicken", "ingredients": ["chicken", "peri-peri sauce", "lemon"]}
            ]
        }
    },
    "neutral": {
        "vegetarian": {
            "diabetes": [
                {"name": "Spinach Salad", "ingredients": ["spinach", "walnuts", "vinaigrette"]},
                {"name": "Mushroom Stir-Fry", "ingredients": ["mushrooms", "soy sauce", "garlic"]}
            ],
            "none": [
                {"name": "Grilled Cheese Sandwich", "ingredients": ["bread", "cheese", "butter"]},
                {"name": "Pasta Primavera", "ingredients": ["pasta", "tomatoes", "zucchini"]},
                {"name": "Veggie Wrap", "ingredients": ["tortilla", "lettuce", "hummus"]}
            ]
        },
        "non_vegetarian": {
            "diabetes": [
                {"name": "Chicken Caesar Salad", "ingredients": ["chicken", "lettuce", "parmesan"]},
                {"name": "Grilled Cod", "ingredients": ["cod", "lemon", "herbs"]}
            ],
            "none": [
                {"name": "Meatball Sub", "ingredients": ["meatballs", "cheese", "bread"]},
                {"name": "Classic Hamburger", "ingredients": ["beef", "bun", "lettuce"]},
                {"name": "Chicken Quesadilla", "ingredients": ["chicken", "cheese", "tortilla"]}
            ]
        }
    }
}
    # Similarly define other moods ("sad", "angry", "neutral")


# Helper functions
def detect_mood(user_input):
    sentiment = sia.polarity_scores(user_input)
    if sentiment["compound"] >= 0.5:
        return "happy"
    elif sentiment["compound"] <= -0.5:
        return "angry"
    elif sentiment["compound"] > -0.5 and sentiment["compound"] < 0:
        return "sad"
    else:
        return "neutral"


def recommend_food(mood, preference, allergies, medical_condition):
    if mood in food_database and preference in food_database[mood]:
        # Get food options based on medical condition
        condition_based_options = food_database[mood][preference].get(medical_condition, food_database[mood][preference]["none"])
        
        # Filter options based on allergies and ingredients
        filtered_food = [
            food["name"] for food in condition_based_options
            if not any(allergen.lower() in food["ingredients"] for allergen in allergies)
        ]
        
        if filtered_food:
            return random.choice(filtered_food)
    return "We couldn't find a match, but how about trying something new?"

# Routes
@app.route("/")
def home():
    return render_template("mood.html")


@app.route("/allergies", methods=["POST"])
def allergies():
    user_input = request.form.get("user_input")
    mood = detect_mood(user_input)
    return render_template("allergies.html", mood=mood)


@app.route("/medical", methods=["POST"])
def medical():
    mood = request.form.get("mood")
    allergies = request.form.getlist("allergies")
    return render_template("medical.html", mood=mood, allergies=allergies)


@app.route("/recommendation", methods=["POST"])
def recommendation():
    mood = request.form.get("mood")
    allergies = request.form.getlist("allergies")
    medical_condition = request.form.get("medical_condition")
    preference = request.form.get("preference")
    food_suggestion = recommend_food(mood, preference, allergies, medical_condition)
    return render_template(
        "recommendation.html", mood=mood, food_suggestion=food_suggestion
    )


if __name__ == "__main__":
    app.run(debug=True)