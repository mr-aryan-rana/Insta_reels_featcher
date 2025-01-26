import logging
from flask import Flask, request, jsonify, render_template
import instaloader
from flask_cors import CORS  # Import CORS to enable cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize instaloader
loader = instaloader.Instaloader()

@app.route('/')
def index():
    return render_template('index.html')  # Renders the frontend

@app.route('/fetch-video', methods=['POST'])
def fetch_video():
    url = request.form.get('url')  # Get the URL sent from frontend

    if not url:
        return jsonify({"error": "Please provide a valid URL"})

    # Check if the URL matches the Instagram post or reel format
    if not (url.startswith("https://www.instagram.com/p/") or url.startswith("https://www.instagram.com/reel/")):
        return jsonify({"error": "Invalid Instagram URL. Ensure it is a valid post or reel URL."})

    try:
        # Extract shortcode from the Instagram URL
        shortcode = url.split("/")[-2]

        # Fetch the post or reel using the shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        # Check if it is a video (either from a post or reel)
        if post.is_video:
            video_url = post.video_url
            logging.debug(f"Video URL: {video_url}")
            return jsonify({"video_url": video_url})

        else:
            return jsonify({"error": "No video found at the provided URL"})

    except instaloader.exceptions.InstaloaderException as e:
        logging.error(f"Instagram error: {str(e)}")
        return jsonify({"error": f"Instagram error: {str(e)}. The post or reel may be restricted or unavailable."})

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An error occurred. Please try again."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)