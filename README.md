# Retrieve-materials-from-Google-Classroom
users can access their google classroom materials uploaded by their faculties on various classroom's and retrieve them with ease

HELLO!!
This project was created using Google drive and classroom API

Dependencies:
Kindly run the following command in the command prompt with pip and python prior installed
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

User must create a file named credentials.json in the working directory and credentials should be availed from google cloud platform (GCP), where user must create their credeentials via Oauth client ID and further enable Google Classroom api and Google Drive api in that. After that those credentials should be pasted into credentials.json file that was earlier created.
Empty directory named "downloadedMaterial", empty file named "DownloadLinks.txt" have to be also initialise in working directory.

Using this API anyone can access all their classroom that they are enrolled in and further could what all latest materials are
uploaded by various professors and TA's, moreover, if you want to download those files then you can download multiple files in
one go as compared to the original classroom where you have to open each file and then open them in the drive from there you have to 
download them. we have simplified this process to one step only also students can easily in a list format view all the materials 
if they wish to do so instead of viewing them separately which is a pain to do so.

Usage:
Run api.py file after completing dependencies and in the first run you will be prompted to connect it with the Gmail account for classroom
access, kindly give access from the account which is associated with classroom.
Then in the menu of the main program, you can wish to see the materials corresponding to a classroom or download them if you wish
to download them then they will be in a downloadMaterial folder

Contributors:
1)Naman Aggarwal
https://github.com/naman-1
2)Ahmed Hanoon
https://github.com/hanoon02
