This project uses MediaPipe for real-time hand tracking and a machine learning model to detect finger taps. Based on the index finger’s tapping motion, it classifies each tap as a DOT (.) or DASH (-), builds Morse code sequences, and decodes them into human-readable text.

📌 Features
🖐️ Real-time hand tracking using MediaPipe
🤖 AI-powered classifier to detect dots and dashes
🔠 Morse code decoding to readable text
🎥 Live webcam input
💡 Easy toggle for start/stop detection and reset

🧠 How It Works
Tracks your index finger using the webcam.
Detects downward and upward motion (a "tap").
Measures tap duration, velocity, and other features.
Classifies each tap as a dot or dash using a trained ML model.
Converts Morse code into text using a dictionary.


Install dependencies with:
pip install opencv-python, mediapipe


Controls:
Key	Function
d	- Toggle detection
r	- Reset Morse code
q	- Quit the program

📄 Morse Code Reference
Morse	Letter		Morse	Letter
.-	A		         
 -... B           -.-.	C
-..	D		           .  	E
..-.	F	         	--.  	G
....	H		        ..	  I
.---	J	         	-.- 	K
.-..	L	          --  	M
-.	N		          --- 	O
.--.	P	      	  --.-	Q
.-.	R		          ...	  S
-	T		            ..-	  U
...-	V		        .--	  W
-..-	X		        -.--	Y
--..	Z			
