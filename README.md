# LOCA
The main backend for the LOCA app, written in Python and Flask.

## What is LOCA?
LOCA is an app allows anybody to point their phone camera at an interesting object, snap a picture of it, and learn more about the story behind it. We used a combination of GPS location data and Google Cloud's Vision API to take any image snapped of a fixture and identify in our database what the object is. The app is able to identify any fixture by first considering all the known fixtures within a fixed radius around the user, and then considering the similarity between known images of those fixtures and the image sent in by the user.

Users also have the ability to browse interesting fixtures in the area around them, add new fixtures and stories by themselves, or modify and add to existing stories with their own information and experiences.

In addition to user-generated content, we also wrote scripts that scraped Wikipedia for geographic location, names, and descriptions of interesting monuments from around the New Haven community. The data we scraped was used both for testing purposes and to serve as initial data for the app, to encourage early adoption.

## Installing

Download the project and run the following to install the Python dependencies:

`pip install -r requirements.txt`

You will need to download `config.json` for the authentication secrets and include it in your root directory.

In addition, initialize the loca-vision submodule with the command `git submodule update --init --recursive`
