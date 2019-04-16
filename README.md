### EzRead
Students in technical and scientific disciplines often struggle to read
textbooks that are systematically overfilled with examples and proofs of reasonings. To aid in
applications of reading where only general concepts need to be understood, EzRead will
deliver streamlined summarizations of text that can be used as in place of a guide for reading, or as a helpful aid during post reading reflection.




### Repo Details
The following are included in this Repo
* Extension

This folder contains the unpacked web extension for firefox. 
The extension consists of a manifest file, javascript script, and any resources and references used

 * Webserver
 
 This folder contains the web app that is currently being hosted on  WinkKurt.pythonanywhere.com
 The web app is made in Python flask, runs in 2.7. TextRank.py is the textranking summary script being used to process 
 data while worker.py is the Flask itself and handling of OAuth2.
 
 Both Token.pickle and credentials are not required as they are created by worker.py. However they can be used to bypass having to request the first set of
 permissions for the user.