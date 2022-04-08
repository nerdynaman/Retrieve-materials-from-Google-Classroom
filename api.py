import os.path
import itertools
import os
import io
import json
import shutil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/drive.readonly']


def get_cred():  # To get the credential
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def driveDownload(creds=get_cred()):  # To download from drive using links from txt file
    with open('DownloadLinks.txt', 'r') as links:
        ids = links.readlines()
    service = build('drive', 'v3', credentials=creds)
    counter = 1
    print('Please wait while Downloading')
    for eachId in ids:
        print('-'*50)
        print(f"Downloading file number {counter}")
        file_id = eachId.split()[0]
        name = " ".join(eachId.split()[1:])
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        dest = os.path.join('downloadedMaterial/', name)
        with open(dest, 'wb') as f:
            shutil.copyfileobj(fh, f)
        counter += 1


def classCodes(creds=get_cred()):  # To get all class codes
    courseDetails = {}
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    for course in courses:
        courseDetails[course['name']] = course['id']
    return courseDetails


# Using credential and user input, we return the course
def getCourseMaterials(creds, id):
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWorkMaterials().list(
        courseId=course_id[id], pageSize=10).execute()
    courses = results.get('courseWorkMaterial')
    tokenNext = results.get("nextPageToken")
    return courses, tokenNext


def nextPageMaterials(creds, id, next_token):  # To get next page of output
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWorkMaterials().list(
        courseId=course_id[id], pageSize=10, pageToken=next_token).execute()
    courses = results.get('courseWorkMaterial')
    tokenNext = results.get("nextPageToken")
    return courses, tokenNext


def viewMaterials():  # To get courses for each
    names = list(course_id.keys())
    course = int(input(
        f"Please choose which course material would you like to obtain: \n1. {names[0]}\n2. {names[1]}\n3. {names[2]}\n4. {names[3]}\n5. {names[4]}\n6. {names[5]}\nEnter your number: "))
    courseMaterial, token = getCourseMaterials(creds, names[course-1])
    try:
        printMaterials(courseMaterial)
    except:
        print("The course contains no materials")
    next = input("Do you wish to view the next page[Y/N]: ")
    while(next.upper() == "Y"):
        courseMaterial, token = nextPageMaterials(
            creds, names[course-1], token)
        try:
            printMaterials(courseMaterial)
        except:
            print("The course contains no materials")
        next = input("Do you wish to view the next page[Y/N]: ")
    else:
        pass


def printMaterials(courseMaterial):  # To print material for each page
    for i in courseMaterial:
        try:
            print("-"*50)
            print("Title: ", i['title'])
            for j in i['materials']:
                print("Material Name: ",
                      j["driveFile"]["driveFile"]["title"])
                print("Link: ", j["driveFile"]
                      ["driveFile"]["alternateLink"])
                print()
            print()
        except:
            print("-"*50)
            print("File could not be retrieved")


def downloadMaterial():  # To download materials from list
    files = []
    names = list(course_id.keys())
    course = int(input(
        f"Please choose which course material would you like to obtain: \n1. {names[0]}\n2. {names[1]}\n3. {names[2]}\n4. {names[3]}\n5. {names[4]}\n6. {names[5]}\nEnter your number: "))
    courseMaterial, token = getCourseMaterials(creds, names[course-1])
    try:
        t = downloadpage(courseMaterial, k)
        filePerPage = list(map(int, input(
            "Please enter the files you want to download: ").split()))
        files.append(filePerPage)
    except:
        print("The course contains no materials")
    next = input("Do you wish to view the next page[Y/N]: ")
    while(next == "Y"):
        courseMaterial, token = nextPageMaterials(
            creds, names[course-1], token)
        try:
            t = downloadpage(courseMaterial, t)
            filePerPage = list(map(int, input(
                "Please enter the files you want to download: ").split()))
            files.append(filePerPage)
        except:
            print("The course contains no materials")
        next = input("Do you wish to view the next page[Y/N]: ")
    else:
        pass
    with open("DownloadLinks.txt", "w") as d:
        for file in list(itertools.chain.from_iterable(files)):
            d.write(f"{links[file-1]}")
    pass


def downloadpage(courseMaterial, k):  # To view the download list per page
    for i in courseMaterial:
        try:
            print("-"*50)
            print("Title: ", i['title'])
            for j in i['materials']:
                print(f"{k}. Material Name: ",
                      j["driveFile"]["driveFile"]["title"])
                links.append(
                    f"{j['driveFile']['driveFile']['id']}" +
                    f" {j['driveFile']['driveFile']['title']}\n"
                )
                k += 1
        except:
            pass
    return k


def getClassCodes():  # Store the class IDs
    if os.path.isfile('className.txt'):
        with open('className.txt', 'r') as f:
            data = json.load(f)
        return data
    else:
        with open('className.txt', 'w') as f:
            data = classCodes()
            print(data)
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data


k = 1
links = []
course_id = getClassCodes()
creds = get_cred()
type = int(input(
    "Please choose the method by which you want to retrieve the files: \n1.View course materials directly\n2.Download course materials materials\nPlease enter the number: "))
if type == 1:
    viewMaterials()
elif type == 2:
    downloadMaterial()
    driveDownload()
