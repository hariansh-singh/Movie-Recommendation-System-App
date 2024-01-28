@app.route('/suggestions', methods=['POST'])
# def get_suggestions():
#     user_input = request.form.get('movie_input', '')

#     # Filter movies based on  input
#     filtered_movies = [title for title in df['title'] if user_input.lower() in title.lower()]

#     suggestions = filtered_movies[:5]

#     return jsonify({'suggestions': suggestions})