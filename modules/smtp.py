import smtplib #Email library
from email import policy  #Methods that control the behavior of various components of the e-mail packet
from email.message import EmailMessage #Send a notification to Email
from email.mime.text import MIMEText # Multipurpose Internet Mail Extensions (MIME) - Text
from email.mime.multipart import MIMEMultipart # Base system for the other MIME functionalities
from email.mime.base import MIMEBase #base class for all specific subclasses Message
from email.mime.image import MIMEImage #Sending images
from email.mime.application import MIMEApplication # It is used to represent MIME message objects of main type 
from email import encoders #For more than one file the byte size can be compressed. 
import os #To open options in the operating system
import pandas as pd # To get values from an Excel or csv file and return them with the recipient's e-mails
import pathlib # To get path of some files attached
import re,time # To user regex and sleep opton to send a email
from modules.data import getData # To get the values of interface (list)
import dearpygui.dearpygui as dpg #Using dearpygui to manipulate the process bar

#Clase emailSender
class smtpsender:
    def __init__(self,data):
        """
        Method __init__(self,data) where data is a list.
        
            self.__usermail = gets first parameter (author email) -> Private attribute (str)
            self.subject = gets subject of email (str)
            self.__recipient = gets the path to a file (TXT,Excel, CSV) or the result of an entry
            self.body = gets the path to a file (TXT) or the result of an entry
            self.fileformat = gets the path of files attached
            self.__token = gets the path to a file(TXT,PEM,KEY) or the result of an entry
            self.__smtpService = gets any smtp services (gmail, outlook, Yahoo) or return a ''
            self.bcc = Boolean value for Bcc or CC
            self.port = default port for smtp service
            self.__visbility = To change Bcc or To -> (str)
            self.readBody = To get the content of self.body
            self.__recipients = To get data and save into a list
            self.__readToken = To get the content of self.__token
        """
        self.__usermail = data[0]
        self.subject = data[1]
        self.__recipient = data[2]
        self.body = data[3]
        self.fileFormat = data[4]
        self.__token = data[5]
        self.__smtpService = data[6]
        self.bcc = data[7]
        self.port = 587 #Puerto de smtp
        self.__visibility = ''
        self.readBody = ''
        self.__recipients = []
        self.__readToken = ''
    #Progress bar private method
    def __processBar(self,fast):
        """
        Method to upload a progress bar (0% to 100%)
        fast -> float value for time.sleep
        """
        i = 0
        while i<=100:
            dpg.set_value('Pbar',1/100*i)
            dpg.configure_item('Pbar',overlay=f'{i:0.1f}%')
            i += 1
            time.sleep(fast)
    #Private method if any error was ocurred
    def __error(self):
        #Calls popup and show a message 
        dpg.configure_item('error_id',show=True)
    #Private method if self.__error is called
    def __emptyBar(self):
        #Configure values of process bar to empty if any error was ocurred 
        dpg.set_value('Pbar', 0)
        #Return value to 0%
        dpg.configure_item('Pbar',overlay=f'0%')
    #Private method if all emails were sent
    def __running(self):
        #Calls popup and show a message 
        return dpg.configure_item("modal_id", show=True)
    #Verify if a request is a file or not
    def __isAFile(self,request):
        if os.path.isfile(request):return True
        else:return False
    #If subject is empty changes to 'This an Email'
    def subjectisEmpty(self):
        if self.subject == '':
            self.subject = 'This an Email'
            return self.subject
        else:return self.subject
    #Gets the path of recipients and return a list. If there isn't any recipient, then return [self.__useremail]
    def __emailSenders(self):
        #Verify if is a file. If it is True then, it gets the suffix
        if self.__isAFile(self.__recipient):
            self.path = pathlib.Path(self.__recipient)
            self.suffix = "".join(self.path.suffixes)
            try:
                #For Excel file
                if self.suffix == '.xlsx':
                    df = pd.read_excel(self.path)
                    #Searching by Email column
                    if ('Email' in df):
                        self.__recipients = [i for i in df['Email']]
                        return self.__recipients #return a list of recipients
                    else:
                        #If the column not exist 'Email' return to same user
                        self.__recipients = [self.__usermail]
                        return self.__recipients
                #For CSV file
                elif self.suffix == '.csv':
                    df = pd.read_csv(self.path)
                    if ('Email' in df):
                        self.__recipients = [i for i in df['Email']]
                        return self.__recipients#return a list of recipients
                    else:
                         #If the column not exist 'Email' return to same user
                         self.__recipient = [self.__usermail]
                         return self.__recipients
                #For TXT file
                elif self.suffix == '.txt':
                    #Opens the file and search by linespace
                    with open(self.__recipient,'r') as file:
                        #Read the file
                        self.emails = file.read()
                        #Split and save every linespace
                        self.__recipients = self.emails.split('\n')
                        return self.__recipients #return a list of recipients
            except:
                #If the file doesn't exist
                self.__recipients = [self.__usermail]
                return self.__recipients
        #If the file is not a file
        else:
            #Saves the entry and return a list
            self.__recipients = [self.__recipient]
            return self.__recipients
    #Method for body format
    def bodyContext(self):
        #Checks if is a file by the path
        if self.__isAFile(self.body):
            #Opens the file (TXT or HTML)
            with open(self.body,'r',encoding='utf-8') as file:
                #Saves the content to self.readBody
                self.readBody = file.read()
            return self.readBody
        else:
            #Returns the content of a entry
            self.readBody = self.body
            return self.readBody
    #Search domain if self.___smtpService = ' '
    def __smtpGet(self):
        #Using regex for search the email domain and return it
        self.domain = re.search(r"@[\w.]+",self.__usermail).group()
        if self.domain == '@gmail.com':
            self.__smtpService = 'smtp.gmail.com'
            return self.__smtpService
        elif self.domain == '@outlook.com' or self.domain == '@hotmail.com':
            self.__smtpService = 'smtp-mail.outlook.com'
            return self.__smtpService
        elif self.domain == '@yahoo.com':
            self.__smtpService = 'smtp.mail.yahoo.com'
            return self.__smtpService
        else:
            #If the domain doesn't exist then returns to 'localhost'
            self.__smtpService == 'localhost'
            return self.__smtpService
    #Gets the token
    def tokenKey(self):
        #If is not a file or the entry is empty then return -1
        if self.__token == '' and self.__smtpService == '' and self.__isAFile(self.__token)==False:
            return -1
        #Verify if the token is a file
        elif self.__isAFile(self.__token):
            #Opens the file and save the token
            with open(self.__token) as tkn:
                self.__readToken = tkn.read()
                #Gets smtp service
                self.__smtpGet()
                return self.__readToken
        #If the token isn't a file and the entry
        elif self.__smtpService=='' and self.__isAFile(self.__token)==False:
            #Gets smtp services from useremail
            self.__smtpGet()
            self.__readToken = self.__token
            return self.__readToken
        else:
            #If the entry is not empty then it saves on self.__readToken
            self.__readToken = self.__token
            return self.__readToken
    #Change whether it is Bcc or 'To'
    def __changeVisibility(self):
        if self.bcc==False:
            self.__visibility = 'To'
            return self.__visibility
        else:
            self.__visibility = 'Bcc'
            return self.__visibility
    #Email sender data. Sending a email
    def __emailSendingOptions(self):
        #Sends a email only with text, token entry and subject entry given by user
        if ((self.__isAFile(self.body)==False or self.__isAFile(self.body)==True) and len(self.fileFormat)==0) and (self.__isAFile(self.__token) or self.tokenKey()!=-1):
            self.__changeVisibility()
            if not self.__isAFile(self.body):
                #initializes the message (object)
                try:
                    email = EmailMessage()
                    #Obtains the necessary parameters for the email
                    email['From'],email[self.__visibility],email["subject"] = self.__usermail,self.__recipients,self.subject
                    email.set_content(self.readBody)
                    #Two-step verification to send the email
                    with smtplib.SMTP(self.__smtpService,self.port) as smtpService:
                        #Safety layer ttls
                        smtpService.starttls()
                        #Gets email and password (not for login)
                        smtpService.login(self.__usermail,self.__readToken)
                        #Send the email as a clear text
                        smtpService.sendmail(self.__usermail,self.__recipients,email.as_string())
                        #End of smtp
                        smtpService.quit()
                    #Start Process bar with time.sleep(0)
                    self.__processBar(fast=0)
                    #Popup 'All emails were sent'
                    self.__running()
                except:
                    #If any data is wrong
                    self.__processBar(fast=0)
                    #Popup 'Error'
                    self.__error()
                    #Progres bar doesn't start
                    self.__emptyBar()
            else:
                #If the body is a file
                if self.body.endswith('.txt'):
                    self.__changeVisibility()
                    try:
                        #Add the data of body
                        msg = MIMEMultipart(policy=policy.default)
                        msg['Subject'] = self.subject
                        msg['From'] = self.__usermail
                        msg[self.__visibility] = self.__recipients
                        # Configures the email body with text and adds it in UTF-8 format.
                        msg.attach(MIMEText((self.readBody.encode('utf-8')), 'plain','utf-8'))
                        # Creates an SMTP object
                        smtp = smtplib.SMTP(self.__smtpService, self.port)
                        # Authenticate on the SMTP server
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(self.__usermail, self.__readToken)
                        smtp.send_message(msg)
                        smtp.quit()
                        self.__processBar(0.5)
                    except:
                        #This an exception
                        self.__processBar(0)
                        self.__error()
                        self.__emptyBar()
                    #If the file is html
                elif self.body.endswith('.html'):
                    self.__changeVisibility()
                    try:
                        msg = MIMEMultipart(policy=policy.default)
                        msg['Subject'] = self.subject
                        msg['From'] = self.__usermail
                        msg[self.__visibility] = self.__recipients
                        # Configures the email body with text and adds it in UTF-8 format.
                        msg.attach(MIMEText(self.readBody, 'html','utf-8'))
                        # Creates an SMTP object
                        smtp = smtplib.SMTP(self.__smtpService, self.port)
                        # Authenticate on the SMTP server
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(self.__usermail, self.__readToken)
                        smtp.send_message(msg)
                        smtp.quit()
                        self.__processBar(0.5)
                        self.__running()
                    except:
                        self.__processBar(0)
                        self.__error()
                        self.__emptyBar()
            #To upload files 
        elif ((self.__isAFile(self.body)==False or self.__isAFile(self.body)==True) and len(self.fileFormat)!=0) and (self.__isAFile(self.__token) or self.tokenKey()!=-1):
            self.__changeVisibility()
            try:
                msg = MIMEMultipart(policy=policy.default)
                msg['Subject'] = self.subject
                msg['From'] = self.__usermail
                msg[self.__visibility] = self.__recipients
                for files in self.fileFormat:
                    #If the suffix is a picture 
                    if files.endswith('.png') or files.endswith('.jpg') or files.endswith('.gif') or files.endswith('.jpeg'):
                        with open(files, 'rb') as f:
                            # Create a MIMEImage object
                            image = MIMEImage(f.read())
                            encoders.encode_base64(image)
                            # Set the attachment name
                            image.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(files).split('/')[-1]))
                            # The file is attached to the e-mail
                            msg.attach(image)
                    #if the suffix is a PDF file
                    elif files.endswith('.pdf'):
                        #If the pdf can read the path
                        with open(files, 'rb') as pdf:
                            #Denotes for PDF files
                            filePdf = MIMEApplication(pdf.read(),_subtype="pdf")
                            encoders.encode_base64(filePdf)
                            #Get the name from the path
                            filePdf.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(files).split('/')[-1]))
                            #Added to the body of the email
                            msg.attach(filePdf)
                    else:pass
                # Configures the email body with text and adds it in UTF-8 format.
                if self.body.endswith('.txt') or self.__isAFile(self.body)!=True:
                    msg.attach(MIMEText((self.readBody.encode('utf-8')), 'plain','utf-8'))
                elif self.body.endswith('.html'):
                    #To attach a html file
                    msg.attach(MIMEText(self.readBody, 'html','utf-8'))
                # Creates an SMTP object
                smtp = smtplib.SMTP(self.__smtpService, self.port)
                # Authenticate on the SMTP server
                smtp.ehlo()
                smtp.starttls()
                smtp.login(self.__usermail, self.__readToken)
                smtp.send_message(msg)
                smtp.quit()
                #Slow process to send a emial
                self.__processBar(0.6)
                self.__running()
            except:
                self.__processBar(0)
                self.__error()
                self.__emptyBar()
        else:
            self.__processBar(0)
            self.__error()
            self.__emptyBar()
    def emailSending(self):
        try:
            #Initializes the values and reassigns them if necessary in the methods
            self.subjectisEmpty()
            self.__emailSenders()
            self.bodyContext()
            self.tokenKey()
            if self.__usermail == '' and self.subject != '' and self.__recipients ==[''] and self.readBody == '' and self.fileFormat == [] and (self.__readToken==-1 or self.__readToken==''):
               #Empty fields
               self.__processBar(0)
               self.__error()
               self.__emptyBar()
            elif self.__usermail!='' and self.subject != '':
                self.__emailSendingOptions()
            else:
                #If any field is empty
                self.__processBar(0)
                self.__error()
                self.__emptyBar()
        except:
            self.__processBar(0)
            self.__error()
            self.__emptyBar()

#Function to initialize the class
def smtpSender():
    #Gets data from the interface
    task = smtpsender(data=getData())
    task.emailSending()