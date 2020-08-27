from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from termcolor import colored
import argparse
import subprocess
from os import remove
from sys import argv


def create_parser():
    parser = argparse.ArgumentParser(description="A python script to backup files to the Google Drive.")
    parser.add_argument("--file", help="The filepath of the file to be uploaded.")
    parser.add_argument("--updir", help="The google drive directory to upload the file to.")
    return parser


def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("/home/c41/PycharmProjects/GoogleDriveBackup/google_credentials.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("/home/c41/PycharmProjects/GoogleDriveBackup/google_credentials.txt")
    return gauth


def generate_directory_id(drive, path):
    folder_list = drive.ListFile(
            {"q": "title='%s' and mimeType='application/vnd.google-apps.folder' and trashed=false" % path}
    ).GetList()
    folder_id = None
    for folder in folder_list:
        if folder["title"] == path:
            folder_id = folder["id"]
            return folder_id
    if folder_id is None:
        folder_id = drive.CreateFile({"title": path, "mimeType": "application/vnd.google-apps.folder"})
        folder_id.Upload()
        folder_id = folder_id["id"]
    return folder_id


def backup_file(drive, filename, directory_id):
    file_to_backup = drive.CreateFile({"title": filename, "parents": [{"id": directory_id}]})
    try:
        file_to_backup.SetContentFile(filename)
    except FileNotFoundError:
        print(f"{colored('Error: ', 'red')}file does not exist!")
        exit(1)
    file_to_backup.Upload()
    print(f"{colored(f'{filename}', 'blue')} was backed up to ", end="")
    print(colored(drive.CreateFile({'id': directory_id})['title'], 'green'))
    print(colored("Backup was successful :)", "cyan"))


def main():
    if argv.__len__() < 1:
        print(f"{colored('Error: ', 'red')}no arguments were given!")
        exit(1)
    subprocess.Popen(
        "cp /home/c41/PycharmProjects/GoogleDriveBackup/client_secrets.json ./",
        shell=True,
        stderr=subprocess.PIPE
    )
    parser = create_parser()
    args = parser.parse_args()
    filename = args.file
    directory = args.updir
    drive = GoogleDrive(authenticate_drive())
    google_directory = generate_directory_id(drive, directory)
    backup_file(drive, filename, google_directory)
    pwd = subprocess.Popen(
        "pwd",
        shell=True,
        stdout=subprocess.PIPE
    )
    if pwd.stdout.readline().decode("utf-8").strip("\n") != "/home/c41/PycharmProjects/GoogleDriveBackup":
        remove("client_secrets.json")


if __name__ == "__main__":
    main()
