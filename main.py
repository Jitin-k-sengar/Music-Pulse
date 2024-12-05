
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from Ui import *
from PyQt5.QtCore import Qt
import sys
import re
from tkinter import messagebox
from threading import Thread
import random
from youtubesearchpython import VideosSearch
from PyQt5.QtGui import QPixmap
import requests
import json
from pytube import YouTube
from pydub import AudioSegment
import os
import yt_dlp
import pygame
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global Active_Tab,SSongs_urls,Sthumbnail_urls,Stitles
Active_Tab = ""
SSongs_urls=[]
Sthumbnail_urls=[]
Stitles=[]


class window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ****************** Transparent Window *******************
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # **********************************************************
        
        self.Page_Selection()
        
        self.ui.otp_button.clicked.connect(self.Send_OTP)
        
        self.ui.Submit_button.clicked.connect(self.Submit_Setup)
        
        self.MenuBar()
        
        self.Home_Screen(event=self.mousePressEvent)
        
        self.ui.Next_page_btn.clicked.connect(self.Next_Button)
        
        self.ui.previous_page_btn.clicked.connect(self.Previous_Button)
        
        self.ui.Search_btn.clicked.connect(self.User_Search)
        
        self.Frame_MousePress()
        
        self.playing = False
        
        self.ui.Play_Pause_btn.clicked.connect(self.play_pause)
        
        self.ui.Next_Song_btn.clicked.connect(self.Forward_song)
        
        self.ui.Previous_Song_btn.clicked.connect(self.Backward_song)
        
        self.ui.mp3_btn.clicked.connect(self.Download_mp3_format)
        
        self.ui.mp4_btn.clicked.connect(self.Video)
        
        self.ui.Favourite_btn.clicked.connect(self.Add_Favourite)
        
        self.Current_favourite_Songs()
        
        self.ui.Exit_btn.clicked.connect(self.close_app)
        
        self.ui.Minimize_btn.clicked.connect(self.Minimize_app)
        
        self.ui.Exit_btn_2.clicked.connect(self.close_app)
        
        self.ui.Minimize_btn_2.clicked.connect(self.Minimize_app)
        
    # **********  Close Application **************************
    def close_app(self):
        self.close()
    # ********************************************************
        
    # ********** Minimize Application ************************
    def Minimize_app(self):
        self.showMinimized()
    # ********************************************************
        
    # ************** Email Validation *******************************
    
    def Validate_Email(self,email):
        # Regular expression for basic email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            return False
        
    # ****************************************************************
    
    # ************** Send Email **************************************
    
    def Send_Email(self,from_Email,to_Email,Subject,body,app_Password):
        
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_Email
        msg['To'] = to_Email
        msg['Subject'] = Subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Connect to the SMTP server and start TLS
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            
            # Log in to the SMTP server
            server.login(from_Email, app_Password)
            
            # Send the email
            server.send_message(msg)
            
        except Exception as e:
            messagebox.showerror("Email Service","Something Went Wrong!")
            
        finally:
            # Terminate the SMTP session
            server.quit()
        
    # *****************************************************************
        
    # *************** Generate OTP ************************************
    
    def Generate_OTP(self):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return otp
    
    # ******************************************************************
    
    # **************** Send OTP Verification to User *******************
    
    def Send_OTP(self):
        def Send_otp_Thread():
            if self.ui.Name_txt.text() != "":
                if self.ui.Email_txt.text() != "":
                    email = self.ui.Email_txt.text()
                    if self.Validate_Email(email):
                        global otp
                        otp = self.Generate_OTP()
                        subject = "Email Verification - Music Mine"
                        body = f"Dear {self.ui.Name_txt.text()},\n\nTo complete your verification process, please use the following One-Time Password (OTP)\n\n{otp}\n\nFor Security reasons, do not share this code with anyone.\n\nIf you did not request this, please disregard this email.\n\nThank you,\n\nMusic Mine Team"
                        self.Send_Email("jitin.k.sengar@gmail.com",email,subject,body,"pypx gpdx urbf onpu")
                        messagebox.showinfo("OTP Verification",f"OTP Sent Successfully to {email}")
                    else:
                        messagebox.showerror("Music Mine","Invalid Email Address")
                else:
                    messagebox.showerror("Music Mine","Please Enter Email Address")
            else:
                messagebox.showerror("Music Mine","Please Enter Your Name")
        Thread(target=Send_otp_Thread).start()
      
    # ******************************************************************
    
    # ***************** Submit Setup ***********************************
    
    def Submit_Setup(self):
        def submit_setup_thread():
            if self.ui.otp_txt.text() != "":
                if self.ui.otp_txt.text() == otp:
                    
                    with open('Json//Setup.json','r') as file:
                        data = json.load(file)
                        
                    data["User Details"]["Name"] = self.ui.Name_txt.text()
                    data["User Details"]["Email"] = self.ui.Email_txt.text()
                    
                    with open('Json//Setup.json','w') as file:
                        json.dump(data, file, indent=4)
                        
                    messagebox.showinfo("Music Mine","Music Mine Setup Complete Successfully")
                    self.ui.stackedWidget.setCurrentIndex(1)
                else:
                    messagebox.showerror("Music Mine","Invalid OTP")
            else:
                messagebox.showerror("Music Mine","Please Enter OTP")
        Thread(target=submit_setup_thread).start()
        
    # *******************************************************************
    
    # ****************** Select Page ************************************
    
    def Page_Selection(self):
        def page_selection_thread():
            with open('Json//Setup.json','r') as file:
                data = json.load(file)
                
                Name = data["User Details"]["Name"]
                Email = data["User Details"]["Email"]
                
            if Name != "" and Email != "":
                self.ui.stackedWidget.setCurrentIndex(1)
            else:
                self.ui.stackedWidget.setCurrentIndex(0)
        Thread(target=page_selection_thread).start()
            
    # ********************************************************************
        
    # ****************** Get Urls, thumbnail, title ***********************
    
    def youtube_search(self,query,max):
    
        videos_search = VideosSearch(query, limit=max)
        result = videos_search.result()
        videos = result['result']
        
        Songs_urls=[]
        thumbnail_urls=[]
        titles=[]
        
        for video in videos:
            Songs_urls.append(video['link'])
            thumbnail_urls.append(video['thumbnails'][0]['url'])
            titles.append(video['title'])
                    
        return Songs_urls , thumbnail_urls , titles
        
    # **********************************************************************
    
    # ******************* Home Page Working ********************************
    
    def Home_Screen(self,event):
        def Home_Screen_thread():
            global Active_Tab
            Active_Tab = "Home_Menu"
            try:
                self.clear_all()
            except:
                pass
            self.ui.Home_Menu.setStyleSheet("color: rgb(255, 0, 79);\n""font: 10pt \"Arial Rounded MT Bold\";")
            self.ui.Search_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
            self.ui.Favourite_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            for i in img_labels:
                img_label = getattr(self.ui,i)
                try:
                    img_label.show()
                except:
                    pass
                
            global HSongs_urls, Hthumbnail_urls, Htitles
            HSongs_urls,Hthumbnail_urls,Htitles = self.youtube_search(max=18,query="Trending single track Songs")
            
            for img_label_name, thumbnail_url, song_url, title_label_name, title in zip(img_labels, Hthumbnail_urls[0:9], HSongs_urls[0:9], title_labels, Htitles[0:9]):
                img_label = getattr(self.ui, img_label_name)
                title_label = getattr(self.ui, title_label_name)
                image_data = requests.get(thumbnail_url).content
                pixmap = QPixmap()
                img_label.setScaledContents(True)
                pixmap.loadFromData(image_data)
                img_label.setPixmap(pixmap)
                img_label.setAccessibleDescription(song_url)
                words = title.split()
                title = " ".join(words[:10])
                title_label.setText(title)
        Thread(target=Home_Screen_thread).start()
        
    # **********************************************************************
    
    # ******************** Search Screen Working ***************************
    
    def Search_Screen(self,event):
        def Search_Screen_thread():
            global Active_Tab,SSongs_urls,Sthumbnail_urls,Stitles
            if Active_Tab!="Search_Menu" and len(SSongs_urls) != 0:
                Active_Tab = "Search_Menu"
                try:
                    self.clear_all()
                except:
                    pass
                self.ui.Search_Menu.setStyleSheet("color: rgb(255, 0, 79);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Home_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Favourite_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
                title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
                for i in img_labels:
                    img_label = getattr(self.ui,i)
                    try:
                        img_label.show()
                    except:
                        pass
                for img_label_name, thumbnail_url, song_url, title_label_name, title in zip(img_labels, Sthumbnail_urls[0:9], SSongs_urls[0:9], title_labels, Stitles[0:9]):
                        img_label = getattr(self.ui, img_label_name)
                        title_label = getattr(self.ui, title_label_name)
                        image_data = requests.get(thumbnail_url).content
                        pixmap = QPixmap()
                        img_label.setScaledContents(True)
                        pixmap.loadFromData(image_data)
                        img_label.setPixmap(pixmap)
                        img_label.setAccessibleDescription(song_url)
                        words = title.split()
                        title = " ".join(words[:10])
                        title_label.setText(title)
        Thread(target=Search_Screen_thread).start()
        
    # **********************************************************************
        
    def User_Search(self):
        def User_Search_thread():
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            
            if self.ui.Search_txt.text() != "":
                self.clear_all()
                global Active_Tab
                Active_Tab = "Search_Menu"
                self.ui.Search_Menu.setStyleSheet("color: rgb(255, 0, 79);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Home_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Favourite_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                global SSongs_urls, Sthumbnail_urls, Stitles
                SSongs_urls,Sthumbnail_urls,Stitles = self.youtube_search(max=18,query=self.ui.Search_txt.text())
                
                for img_label_name, thumbnail_url, song_url, title_label_name, title in zip(img_labels, Sthumbnail_urls[0:9], SSongs_urls[0:9], title_labels, Stitles[0:9]):
                    img_label = getattr(self.ui, img_label_name)
                    title_label = getattr(self.ui, title_label_name)
                    image_data = requests.get(thumbnail_url).content
                    pixmap = QPixmap()
                    img_label.setScaledContents(True)
                    pixmap.loadFromData(image_data)
                    img_label.setPixmap(pixmap)
                    img_label.setAccessibleDescription(song_url)
                    words = title.split()
                    title = " ".join(words[:10])
                    title_label.setText(title)
                    
        Thread(target=User_Search_thread).start()
        
    def MenuBar(self):
        def MenuBar_thread():
            self.ui.Home_Menu.mousePressEvent = self.Home_Screen
            self.ui.Search_Menu.mousePressEvent = self.Search_Screen
            self.ui.Favourite_Menu.mousePressEvent = self.Favourite
        Thread(target=MenuBar_thread).start()
        
    # ******************** When Next Page Button Clicked ************************************
    
    def Next_Button(self):
        def Next_Button_thread():
            
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            
            # ***************** For Home Menu ************************************************
            if Active_Tab == "Home_Menu":
                Last_url = self.ui.T9.accessibleDescription()
                index = HSongs_urls.index(Last_url)
                if index != 17:
                    self.clear_all()
                    for i,img_label,title_label in zip(range(9,19),img_labels,title_labels):
                        img_label = getattr(self.ui, img_label)
                        title_label = getattr(self.ui, title_label)
                        try:
                            image_data = requests.get(Hthumbnail_urls[i]).content
                            pixmap = QPixmap()
                            img_label.setScaledContents(True)
                            pixmap.loadFromData(image_data)
                            img_label.setPixmap(pixmap)
                        except:
                            pass
                        img_label.setAccessibleDescription(HSongs_urls[i])
                        title = Htitles[i]
                        words = title.split()
                        title = " ".join(words[:10])
                        title_label.setText(title)
                else:
                    pass
                
            elif Active_Tab == "Search_Menu":
                Last_url = self.ui.T9.accessibleDescription()
                index = SSongs_urls.index(Last_url)
                if index != 17:
                    self.clear_all()
                    for i,img_label,title_label in zip(range(9,19),img_labels,title_labels):
                        img_label = getattr(self.ui, img_label)
                        title_label = getattr(self.ui, title_label)
                        try:
                            image_data = requests.get(Sthumbnail_urls[i]).content
                            pixmap = QPixmap()
                            img_label.setScaledContents(True)
                            pixmap.loadFromData(image_data)
                            img_label.setPixmap(pixmap)
                        except:
                            pass
                        img_label.setAccessibleDescription(SSongs_urls[i])
                        title = Stitles[i]
                        words = title.split()
                        title = " ".join(words[:10])
                        title_label.setText(title)
            elif Active_Tab == "Favourite_Menu":
                Active_labels = []
                Last_url = self.ui.T9.accessibleDescription()
                print(Last_url)
                if Last_url != "" and len(Fthumbnail_urls) > 8:
                    index = FSongs_urls.index(Last_url)
                    self.clear_all()
                    for i in img_labels:
                        img_label = getattr(self.ui,i)
                        try:
                            img_label.show()
                        except:
                            pass
                    try:
                        for i,img_label_name,title_label in zip(range(index+1,index+10),img_labels,title_labels):
                            img_label = getattr(self.ui, img_label_name)
                            title_label = getattr(self.ui, title_label)
                            try:
                                image_data = requests.get(Fthumbnail_urls[i]).content
                                pixmap = QPixmap()
                                img_label.setScaledContents(True)
                                pixmap.loadFromData(image_data)
                                img_label.setPixmap(pixmap)
                            except:
                                pass
                            img_label.setAccessibleDescription(FSongs_urls[i])
                            Active_labels.append(img_label_name)
                            title = Ftitles[i]
                            words = title.split()
                            title = " ".join(words[:10])
                            title_label.setText(title)
                    except:
                        pass
                        
                
                for i in img_labels:
                    if i in Active_labels:
                        continue
                    else:
                        img_label = getattr(self.ui, i)
                        img_label.hide()
                
            # ********************************************************************************
            
            
        Thread(target=Next_Button_thread).start()
        
    # ****************************************************************************************
    
    # ******************** When Previous Page Button Clicked *********************************
    
    def Previous_Button(self):
        def Previous_Button_thread():
            
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            
            # ******************* For Home Menu ************************************************
            if Active_Tab == "Home_Menu":
                first_url = self.ui.T1.accessibleDescription()
                index = HSongs_urls.index(first_url)
                if index == 9:
                    self.clear_all()
                    for i,img_label,title_label in zip(range(0,9),img_labels,title_labels):
                        img_label = getattr(self.ui, img_label)
                        title_label = getattr(self.ui, title_label)
                        try:
                            image_data = requests.get(Hthumbnail_urls[i]).content
                            pixmap = QPixmap()
                            img_label.setScaledContents(True)
                            pixmap.loadFromData(image_data)
                            img_label.setPixmap(pixmap)
                        except:
                            pass
                        img_label.setAccessibleDescription(HSongs_urls[i])
                        title = Htitles[i]
                        words = title.split()
                        title = " ".join(words[:10])
                        title_label.setText(title)
            # **********************************************************************************
            
            elif Active_Tab == "Search_Menu":
                first_url = self.ui.T1.accessibleDescription()
                index = SSongs_urls.index(first_url)
                if index == 9:
                    self.clear_all()
                    for i,img_label,title_label in zip(range(0,9),img_labels,title_labels):
                        img_label = getattr(self.ui, img_label)
                        title_label = getattr(self.ui, title_label)
                        try:
                            image_data = requests.get(Sthumbnail_urls[i]).content
                            pixmap = QPixmap()
                            img_label.setScaledContents(True)
                            pixmap.loadFromData(image_data)
                            img_label.setPixmap(pixmap)
                        except:
                            pass
                        img_label.setAccessibleDescription(SSongs_urls[i])
                        title = Stitles[i]
                        words = title.split()
                        title = " ".join(words[:10])
                        title_label.setText(title)
            elif Active_Tab == "Favourite_Menu":
                Active_labels = []
                Last_url = self.ui.T1.accessibleDescription()
                if Last_url != "" and len(Fthumbnail_urls) > 8:
                    index = FSongs_urls.index(Last_url)
                    self.clear_all()
                    for i in img_labels:
                        img_label = getattr(self.ui,i)
                        try:
                            img_label.show()
                        except:
                            pass
                    try:
                        for i,img_label_name,title_label in zip(range(index-9,index),img_labels,title_labels):
                            img_label = getattr(self.ui, img_label_name)
                            title_label = getattr(self.ui, title_label)
                            try:
                                image_data = requests.get(Fthumbnail_urls[i]).content
                                pixmap = QPixmap()
                                img_label.setScaledContents(True)
                                pixmap.loadFromData(image_data)
                                img_label.setPixmap(pixmap)
                            except:
                                pass
                            img_label.setAccessibleDescription(FSongs_urls[i])
                            Active_labels.append(img_label_name)
                            title = Ftitles[i]
                            words = title.split()
                            title = " ".join(words[:10])
                            title_label.setText(title)
                    except:
                        pass
                        
                
                for i in img_labels:
                    if i in Active_labels:
                        continue
                    else:
                        img_label = getattr(self.ui, i)
                        img_label.hide()
                            
                            
            
        Thread(target=Previous_Button_thread).start()
    
    # *****************************************************************************************
        
    # ****************** When Need to clear the Title and tumbnail Box ************************
    
    def clear_all(self):
        def clear_all_thread():
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            
            for img, label in zip(img_labels,title_labels):
                img_label = getattr(self.ui, img)
                title_label = getattr(self.ui, label)
                img_label.setPixmap(QPixmap())
                title_label.setText("")
        Thread(target=clear_all_thread).start()
        
    # *****************************************************************************************
    
    # ******************* Connect Frame with mousepressEvent **********************************
    
    def Frame_MousePress(self):
        img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
        
        
        for i in img_labels:
            frame = getattr(self.ui, i)
            frame.mousePressEvent = self.Play_Song
            
    # ******************************************************************************************
    
    # ******************** Play Selected Song in Background *************************************
        
    def Play_Song(self,event):
        
        def play_song_thread():
            
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                pygame.quit()
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/play Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.Play_Pause_btn.setIcon(icon9)
            except:
                pass
            
            self.ui.Play_Pause_btn.setDisabled(True)
            
            label = QApplication.widgetAt(event.globalPos())
            if isinstance(label, QLabel):
                if label.accessibleDescription():
                    url = label.accessibleDescription()
                    self.ui.label_2.setAccessibleDescription(url)
                    if url in HSongs_urls:
                        index = HSongs_urls.index(url)
                        thumbnail = Hthumbnail_urls[index]
                    elif url in SSongs_urls:
                        index = SSongs_urls.index(url)
                        thumbnail = Sthumbnail_urls[index]
                    elif url in FSongs_urls:
                        index = FSongs_urls.index(url)
                        thumbnail = Fthumbnail_urls[index]
                        
                    title = YouTube(url).title
                    
                    Singer = YouTube(url).author
                    image_data = requests.get(thumbnail).content
                    pixmap = QPixmap()
                    self.ui.label_2.setScaledContents(True)
                    pixmap.loadFromData(image_data) 
                    self.ui.label_2.setPixmap(pixmap)
                    self.ui.label_3.setText(title)
                    self.ui.label_4.setText(Singer)
                    icon9 = QtGui.QIcon()
                    icon9.addPixmap(QtGui.QPixmap("Icons/Loading Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.ui.Play_Pause_btn.setIcon(icon9)
        
        Thread(target=play_song_thread).start()
        Thread(target=self.Download_mp3).start()
        
    # ********************************************************************************************
    
    # ********************* When Forward Button Clicked ******************************************
        
    def Forward_play(self,url):
        
        def Forward_play_thread():
            
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                pygame.quit()
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/play Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.Play_Pause_btn.setIcon(icon9)
                self.ui.Play_Pause_btn.setDisabled(True)
            except:
                pass
            self.ui.label_2.setAccessibleDescription(url)
            if url in HSongs_urls:
                index = HSongs_urls.index(url)
                thumbnail = Hthumbnail_urls[index]
            elif url in SSongs_urls:
                index = SSongs_urls.index(url)
                thumbnail = Sthumbnail_urls[index]
                
            title = YouTube(url).title
            
            Singer = YouTube(url).author
            image_data = requests.get(thumbnail).content
            pixmap = QPixmap()
            self.ui.label_2.setScaledContents(True)
            pixmap.loadFromData(image_data) 
            self.ui.label_2.setPixmap(pixmap)
            self.ui.label_3.setText(title)
            self.ui.label_4.setText(Singer)
            icon9 = QtGui.QIcon()
            icon9.addPixmap(QtGui.QPixmap("Icons/Loading Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.Play_Pause_btn.setIcon(icon9)
        
        Thread(target=Forward_play_thread).start()
        Thread(target=self.Download_mp3).start()
        
    # *********************************************************************************************
    
    # ******************** Pause and unpause Song **************************************************
        
    def play_pause(self):
        
        if pygame.mixer.get_init():
            if self.playing:
                pygame.mixer.music.pause()
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/play Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.Play_Pause_btn.setIcon(icon9)
                global pause
                pause = True
            else:
                pygame.mixer.music.unpause()
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/Pause Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.Play_Pause_btn.setIcon(icon9)
                pause = False
            self.playing = not self.playing
            
    # **********************************************************************************************
            
    def Download_mp3(self):
        time.sleep(0.5)
        url = self.ui.label_2.accessibleDescription()
        try:
            os.remove("temp.mp4")
            os.remove("temp.mp3")
        except:
            pass
        YouTube(url).streams.get_audio_only().download(filename="temp.mp4")
        time.sleep(0.5)
        audio = AudioSegment.from_file("temp.mp4", format="mp4")
        audio.export("temp.mp3", format="mp3")
        time.sleep(1)
        Thread(target=self.play_mp3).start()
        
    def play_mp3(self):
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        self.ui.Play_Pause_btn.setDisabled(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("Icons/Pause Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.Play_Pause_btn.setIcon(icon9)
        
    def Forward_song(self):
        if self.ui.label_2.accessibleDescription() != "":
            current_song = self.ui.label_2.accessibleDescription()
            if current_song in HSongs_urls:
                index = HSongs_urls.index(current_song)
                if index < 17:
                    self.Forward_play(HSongs_urls[index+1])
            elif current_song in SSongs_urls:
                index = SSongs_urls.index(current_song)
                if index < 17:
                    self.Forward_play(SSongs_urls[index+1])
                
    def Backward_song(self):
        if self.ui.label_2.accessibleDescription() != "":
            current_song = self.ui.label_2.accessibleDescription()
            if current_song in HSongs_urls:
                index = HSongs_urls.index(current_song)
                if index >0:
                    self.Forward_play(HSongs_urls[index-1])
            elif current_song in SSongs_urls:
                index = SSongs_urls.index(current_song)
                if index > 0:
                    self.Forward_play(SSongs_urls[index-1])
    
    def Download_mp3_format(self):
        def Download_mp3_format_thread():
            if self.ui.label_2.accessibleDescription() != "":
                url = self.ui.label_2.accessibleDescription()
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/Active Mp3 Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.mp3_btn.setIcon(icon9)
                YouTube(url).streams.get_audio_only().download(output_path="c:\\Users\\Jitin\\Downloads\\",filename=f"{YouTube(url).title}.mp3")
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/Mp3 Download Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.mp3_btn.setIcon(icon9)
        Thread(target=Download_mp3_format_thread).start()
    
    def Video(self):
        def Video_thread():
            if self.ui.label_2.accessibleDescription() != "":
                
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/Active Mp4 Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.mp4_btn.setIcon(icon9)
                
                path = "c:\\Users\\Jitin\\Downloads\\"
                options = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': f'{path}/%(title)s.%(ext)s',
                    'n_threads': 8,  # Use multiple threads for downloading
                    'concurrent_fragments': 5,  # Number of fragments to download concurrently
                    'http_chunk_size': 10*1024*1024,  # Size of each chunk to download
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    url = self.ui.label_2.accessibleDescription()
                    info_dict = ydl.extract_info(url, download=False)
                    ydl.download([url])
                    
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("Icons/Mp4 Download Icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.mp4_btn.setIcon(icon9)
                
        Thread(target=Video_thread).start()
    
    def Add_Favourite(self):
        def Add_Favouite_thread():
            if self.ui.label_2.accessibleDescription() != "":
                url = self.ui.label_2.accessibleDescription()
                with open("Json//Favourite.json",'r') as file:
                    data = json.load(file)
                    
                    Current_list = list(data["Favourite Songs"]["Favourite"])
                    
                if url in Current_list:
                    messagebox.showinfo("Music Mine Lite",f"{YouTube(url).title} Already in Favourite List")
                else:
                    data["Favourite Songs"]["Favourite"].append(url)
                    
                    with open("Json//Favourite.json", 'w') as file:
                        json.dump(data, file, indent=4)
                        
                    messagebox.showinfo("Music Mine Lite",f"{YouTube(url).title} Added to Favourite List")
                
                file.close()
        Thread(target=Add_Favouite_thread).start()
            
    def get_video_details(self,song_urls):
        titles = []
        thumbnail_urls = []
        
        for url in song_urls:
            video_search = VideosSearch(url, limit=1)
            result = video_search.result()
            video = result['result'][0]
            titles.append(video['title'])
            thumbnail_urls.append(video['thumbnails'][0]['url'])
        
        return thumbnail_urls, titles
                
    def Favourite(self,event):
        def Favourite_thread():
            
            img_labels = ["T1","T2","T3","T4","T5","T6","T7","T8","T9"]
            title_labels = ["TL1","TL2","TL3","TL4","TL5","TL6","TL7","TL8","TL9"]
            
            Active_labels = []
            
            def Task1():
                global Active_Tab
                Active_Tab = "Favourite_Menu"
                self.ui.Favourite_Menu.setStyleSheet("color: rgb(255, 0, 79);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Home_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                self.ui.Search_Menu.setStyleSheet("color: rgb(255, 255,255);\n""font: 10pt \"Arial Rounded MT Bold\";")
                try:
                    self.clear_all()
                except:
                    pass
                
            Thread(target=Task1).start()
            

            global Fthumbnail_urls, Ftitles, FSongs_urls
            Fthumbnail_urls, Ftitles = self.get_video_details(Current_list)
            FSongs_urls = Current_list
            
            for img_label_name, thumbnail_url, song_url, title_label_name, title in zip(img_labels, Fthumbnail_urls, FSongs_urls, title_labels, Ftitles):
                img_label = getattr(self.ui, img_label_name)
                title_label = getattr(self.ui, title_label_name)
                image_data = requests.get(thumbnail_url).content
                pixmap = QPixmap()
                img_label.setScaledContents(True)
                pixmap.loadFromData(image_data)
                img_label.setPixmap(pixmap)
                img_label.setAccessibleDescription(song_url)
                Active_labels.append(img_label_name)
                words = title.split()
                title = " ".join(words[:10])
                title_label.setText(title)
                
            for i in img_labels:
                if i in Active_labels:
                    continue
                else:
                    img_label = getattr(self.ui, i)
                    img_label.hide()
                    
        Thread(target=Favourite_thread).start()
        
    def Current_favourite_Songs(self):
        def Current_Favourite_Songs_thread():
            global Current_list
            while True:
                with open("Json//Favourite.json",'r') as file:
                    data = json.load(file)
                    
                Current_list = list(data["Favourite Songs"]["Favourite"])
        Thread(target=Current_Favourite_Songs_thread).start()
                    
            
                
            
            
            
    
    
    
    
app = QApplication(sys.argv)
gui = window()
gui.show()
sys.exit(app.exec_())