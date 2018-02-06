# EC500 - Building Software

Twitter Summarization Slideshow Creator

The TwitterSummarization.py file is a compilation of gVision.py and myTweep.py.
The overall function is as follows: the program asks for an input of a twitter handle.
It then uses OAuth with the Twitter API, then grabs the last 100 tweets from that user's
profile. It scans these tweets and pulls 5 pictures (if less than five, the program says
so. If none, the program throws an error).

Next, the pictures are downloaded and sent to another function that sends them to the google
API. The image is analyzed, and information is pulled and stored into a local text file.
Then FFMPEG converts the image into a short .mp4. This is repeated for all five images.
Lastly, FFMPEG concatenates all movie files into a 10 second slideshow, and finishes by deleting
the extra files.

Twitter API:
To use the twitter API, you must create a Twitter API project to receive OAuth credentials. I stored them in a 
text file line after line so that the program can read the inputs instead of hardcoding them in.

Google API:
1. Create a service account https://cloud.google.com/docs/authentication/getting-started
2. Install google-cloud-storage (only works with v1.6.0?)
3. Set GOOGLE_APPLICATION_CREDENTIALS variable (https://cloud.google.com/docs/authentication/getting-started)
	Windows example: >set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\abbot\Desktop\Everything\College\Building_Software\API_Exercise\MFP-75c79c884e32.json
	Note: Be careful storing the credentials file and setting the credentials path.

FFMPEG:
I downloaded ffmpeg and added the installation directory to PATH. Additionally, the program uses "ffmpy", which
can be downloaded with a simple "pip install ffmpy". This allows ffmpeg commands to be called in the script.