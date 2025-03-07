ClassActors

Project Description

ClassActors is an AI-based actor recognition system that identifies actors from an image. The model analyzes an input image and predicts which actor it matches from a predefined dataset. The dataset currently supports identification for five Indian actors. The system provides a confidence percentage indicating the likelihood of a match.

##Features

Accepts an image as input and predicts the actor's name.

Uses a trained machine learning model to classify actors.

Provides a confidence score for each prediction.

Can be expanded to include more actors in the future.

##Installation

Prerequisites

Ensure you have the following installed:

Python 3.x

Required dependencies (install using the command below)

##Setup

1. Go into the directory: 'cd classActors'

2. Install dependencies: 'pip install -r model/requirements.txt'

3. Run the server: 'python3 server/server.py'

4. Open HTML file through on your browser

##Usage

The server hosts an API that takes an image as input and returns the predicted actor's name with confidence scores.

Send an image via an HTTP request to the server.

Example API request (using cURL): curl -X POST -F "file=@image.jpg" http://localhost:5000/predict

The server responds with:
	{
		"actor": Varun Dhawan",
		"confidence": 92.5
	}

##Project Structure

classActors/
│── server/               			# Backend server scripts
│   ├── server.py        			# Main server script
│   ├── util.py          			# Helper functions
│   ├── wavelet.py       			# Preprocessing module
│   ├── artifacts/       			# Model files
│       ├── saved_model.pkl  			# Trained model
│       ├── class_dictionary.json  		# Actor labels
│── model/               			# Model training scripts
│   ├── actors_classifier_model.ipynb  		# Training notebook
│   ├── requirements.txt  			# Python dependencies
│── google_image_scrapping/  			# Scripts for dataset collection
│   ├── image_scraper.py
│── images_dataset/      			# Training images


##Technologies Used

Python

Flask (for API server)

Scikit-learn, OpenCV, NumPy (for image processing & model training)

Jupyter Notebook (for model development)

HTML, CSS, JavaScript (for website development)

##Contributors

Harsh Patel




