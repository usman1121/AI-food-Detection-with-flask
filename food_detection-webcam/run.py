from app import food_detection
app = food_detection()
if __name__ == "__main__":
    app.run(debug=True, port=8080)