import pysftp
import os
import tkFileDialog
from Tkinter import *
import tkMessageBox
import threading
import paramiko

def askDirectory():
    dest = str(tkFileDialog.askdirectory())
    dest = dest.replace('/','\\')
    destinationText.delete(0,END)
    destinationText.insert(0,dest)
    
def askFile():
    dest = str(tkFileDialog.asksaveasfilename())
    dest = dest.replace('/','\\')
    destinationText.delete(0,END)
    destinationText.insert(0,dest)
    
def ask():
    if isDir.get() == 1:
        askDirectory()
    else:
        askFile()

connection = None
def connectOrRetry(hostname, username, password):
    while True:
        try:
            connection =  pysftp.Connection(hostname, username=username, password=password)
            print 'Connected To '+ hostname
            return connection
        except paramiko.ssh_exception.SSHException:
            print 'Connection Failed, Retrying'
        
def downloadSFTP():
    username = usernameText.get()
    password = passwordText.get()
    hostname = hostnameText.get()
    source = sourceText.get()
    destination = destinationText.get()

    if not username or not password or not hostname or not destination:
        tkMessageBox.showinfo("Downloader", "Missing Arguments") 
        return

    if isDir.get() == 1:
        if source[-1] is not '/':
            source = source+'/'
        downloaderThread = threading.Thread(target=get_r_wrapper, args = (hostname, username, password, source, destination))
    else:
        downloaderThread = threading.Thread(target=get_wrapper, args = (hostname, username, password, source, destination))


    downloaderThread.daemon = True
    downloaderThread.start()

    tkMessageBox.showinfo("Downloader", "Sync Started")

def get_r_wrapper(hostname, username, password, source, destination):
    connection = connectOrRetry(hostname, username, password)
    while True:
        try:
            connection.get_r(source, destination, preserve_mtime=True)
        except paramiko.ssh_exception.SSHException:
            connection = connectOrRetry(hostname, username, password)

def get_wrapper(hostname, username, password, source, destination):
    connection = connectOrRetry(hostname, username, password)
    while True:
        try:
            connection.get(source, destination, preserve_mtime=True)
        except paramiko.ssh_exception.SSHException:
            connection = connectOrRetry(hostname, username, password)
            
if __name__ == "__main__":

    root = Tk()
    
    root.title("SFTP Downloader")
    root["padx"] = 40
    root["pady"] = 20       

    textFrame = Frame(root)
    
    hostname = Label(textFrame)
    hostname["text"] = "Hostname:"
    hostname.grid(row=0,column=0)

    hostnameText = Entry(textFrame)
    hostnameText["width"] = 50
    hostnameText.grid(row=0,column=1)
    
    username = Label(textFrame)
    username["text"] = "Username:"
    username.grid(row=1,column=0)

    usernameText = Entry(textFrame)
    usernameText["width"] = 50
    usernameText.grid(row=1,column=1)
    
    password = Label(textFrame)
    password["text"] = "Password:"
    password.grid(row=2,column=0)

    passwordText = Entry(textFrame)
    passwordText["width"] = 50
    passwordText.grid(row=2,column=1)
    
    source = Label(textFrame)
    source["text"] = "Source:"
    source.grid(row=3,column=0)

    sourceText = Entry(textFrame)
    sourceText["width"] = 50
    sourceText.grid(row=3,column=1)
    
    isDir = IntVar()
    isDirectory = Checkbutton(textFrame, text = 'Are You Downloading A Directory?', variable = isDir)
    isDirectory.grid(row=4, column=0)
    
    destination = Label(textFrame)
    destination["text"] = "Destination:"
    destination.grid(row=5,column=0)

    destinationText = Entry(textFrame)
    destinationText["width"] = 50
    destinationText.grid(row=5,column=1)
    
    destinationButton = Button(textFrame, text='Browse', command=ask).grid(row=5,column=2)
    
    textFrame.pack()

    button = Button(root, text="Start Sync", command=downloadSFTP)
    button.pack() 
    
    root.mainloop()