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
 
 * Resources
 
 This folder contains former scripts used for testing and development, 
 along with some of the old concept ideas. These are outdated files and are only for reference.
 
 
 
 ### How-to Set up:
 
 Installing the browser extension is currently only supported locally (It's not on the store yet) but 
 the process is fairly easy. 
 
 1. Go to about:debugging in your firefox browser
 2. Click on Load Temporary Add-On
 3. Selection either manifest.json or background.js from inside the Extension folder
 
 The extension should now be loaded
 
 ### Using the extension
 
 Select any body of text and right click. In the right click menu there should be an addtional button in the dropdown named EzRead.
  Clicking it should send any collected text over to the PythonAnywhere flask app which will then create a new document with a summary in the currently signed in Google Drive.
  
  ### Important Google Account Notice
  
  Currently the OAuth2 needed to create documents in Google Drive is only run server side. That means that only the
   account of token.pickle and credtenitals.json will recieve this document. In a later date this will be either  be 
   handled in the JavaScript extension on the client side, or patched server side.
   
  ### How is this Summary made?
  In simple terms: Each sentence is given a score which is computed from a graph of k-most 'similar sentences'. Then they are ranked and posted based on there scored.
  Right now the max output is 7 sentences. So any text smaller than that is rather pointless. A setting variable may come in the future to change how big the summary should be. 
  A better and more detailed paper can be found at <https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf>
