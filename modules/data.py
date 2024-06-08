import dearpygui.dearpygui as dpg #Import module of dearpygui
import os #Import module for operating system

###Global variables
#Saves path file of recipients
singlePath_1 = ''
#Saves path files of body (TXT or HTML)
singlePath_2 = ''
#Saves what kind of service of SMTP (i.e Gmail,Outlook,Yahoo) -> If the token is a file returns ''
smtpServices = ''
#If the token is typed by user. Saves the string
tokenSave = ''
#If the token is a file. Saves the file path.
tokenPath = ''
#Saves the email of sender
usermail = ''
#Saves the subject of email.
subject = ''
#If user uploads many files (i.e. pictures and PDF files), it saves paths of them 
multiPath = []
#Bcc or To (defect value)
hidecopy = False
#Recompilation of all values of for sending a email
senderValues = []

#Get values from interface  -> Return a list
def getData() -> list:
    """
    This function gets value of: 
        author email: useremail (str)
        
        subject of email: subject (str) -> Dearpygui doesn't allow utf-8 as an input.
        
        valueToken: Gets value of a string (input by user)
        
        manualRecipient: (Receives the recipients)
                    If there is not a recipient -> ''
                    If user types the recipient -> str
                    If recipients are into a file -> saves  file path
        
        bodyFormat: (Receives the body of email)
                    if the body is empty or user types it -> '' || str
                    if the body is into a file -> saves  file path (str)
        
        tokenValue: (receives the value of token or fiel path):
                    if the token is typed by user  -> (str)
                    if the token is into a file -> file path (str)
        
        sendervalues: (receives all of the above values). It saves on a list.
    """
    global usermail,subject,senderValues
    usermail = dpg.get_value('useremail')
    subject = dpg.get_value('subject')
    valueFile = dpg.get_value('fileoptions')
    valueToken = dpg.get_value('token')
    manualRecipient = ''
    bodyFormat = ''
    tokenValue = ''
    fileFormat = []
    if dpg.get_value('recipient')== 'None':
        manualRecipient = ''
    elif dpg.get_value('recipient') == 'Manual':
        manualRecipient = dpg.get_value('valuerR')
    elif dpg.get_value('recipient') == 'File':
        manualRecipient = singlePath_1
    if dpg.get_value('bodyoptions') == 'Manual Text':
        bodyFormat = dpg.get_value('bodyS')
        
    elif dpg.get_value('bodyoptions') == 'By TXT file' or dpg.get_value('bodyoptions') == 'HTML (Not use images embebed)':
        bodyFormat  = singlePath_2
    if valueFile == 'Not':
        fileFormat = []
    elif dpg.get_value('fileoptions') == 'Pictures' or dpg.get_value('fileoptions') == 'PDF' or dpg.get_value('fileoptions') == 'Both' :
        fileFormat  = multiPath
    if dpg.get_value('listsmtp')=="Gmail" or dpg.get_value('listsmtp')== 'Outlook' or dpg.get_value('listsmtp')=='Yahoo':
        tokenValue = tokenSave
    if valueToken == 'By file':
        tokenValue = tokenPath
    senderValues = [usermail,subject,manualRecipient,bodyFormat,fileFormat,tokenValue,smtpServices,hidecopy]
    return senderValues
    
#Function for button for values of recipient
def recipientOptions() -> None:
    """
    This function gets the value of button of recipient:
    
    None -> Shows button with option of None, hides bar of recipient to write manually, hides option to attach a file
    
    Manual -> Shows bar of recipient to write manually, and hides button to attach a file and button of None
    
    File -> Opens the file dialog and hides None and manually recipient
    
    """
    valueOption = dpg.get_value('recipient')
    if valueOption == 'None':
        dpg.configure_item('valuerR',show=False)
        dpg.configure_item('fileup',default_value="",show=False)
        dpg.configure_item('file_dialog_id',show=False)
    elif valueOption == 'Manual':
        dpg.configure_item('valuerR',show=True)
        dpg.configure_item('fileup',default_value="",show=False)
        dpg.configure_item('file_dialog_id',show=False)
    elif valueOption == 'File':
        dpg.configure_item('valuerR',show=False)
        dpg.configure_item('file_dialog_id',show=True)
#Function to get information from buttons -> Not retunr values
def callback(sender,app_data) -> None:
    """
    This function receives sender and app_data (values of end-user)
    Sender sends a event id:
                        'file_dialog_id': Opens internal file browser and gets the file of recipients (TXT,CSV,XLSX)
                        
                        'txt_dialog_id': Saves the body of email (Only file type TXT) 
                        
                        'html_dialog_id: Saves the body of email (Only file  type HTML)
                        
                        'multi_file_pictures': Saves path of pictures choosen by user, up to 10 files (.png,.gif,.jpg,.jpeg) 
                        
                        'pdf_dialog_id:  Saves path of PDF files choosen by user, up to 10 files.
                        
                        'multi_files': Saves path both of them as pictures and PDF files (up to 10 files)
                        
                        'token_discover': Saves the path file of token
    """
    global singlePath_1
    global singlePath_2
    global multiPath
    global tokenPath
    if sender == 'file_dialog_id':
        dpg.configure_item('fileup',default_value="File uploaded: {}".format(app_data['file_name']),show=True)
        singlePath_1 = app_data['file_path_name']
    elif sender == 'txt_dialog_id' or sender== 'html_dialog_id':
        dpg.configure_item('bodyfileup',default_value="File uploaded: {}".format(app_data['file_name']),show=True)
        singlePath_2 = app_data['file_path_name']
    elif sender == 'multi_file_pictures' or sender == 'multi_files' or sender == 'pdf_dialog_id':
        multiPath = list(app_data['selections'].values())
        fileNames = list(app_data['selections'].keys())
        dpg.configure_item('filesattached',default_value="File(s) uploaded: {}".format(len(fileNames)),show=True)
    elif sender == 'token_discover':
        tokenPath = app_data['file_path_name']
        dpg.configure_item('tokenfile',default_value="Token file uploaded: {}".format(app_data['file_name']),show=True)
    
#Function for button for values of body email
def bodyOptions():
    """
    This function gets the value of button of body email:
    
    Manual Text -> Shows bar of body to write manually, hides as file dialog and its message
    
    By TXT file -> Hides bar of body to write manually, hides file dialog but opens txt_dialog_id
    
    'HTML (Not use images embebed)' -> Hides bar of body to write manually, hides file dialog but opens html_dialog_id
    
    """
    valueOption = dpg.get_value('bodyoptions')
    if valueOption == 'Manual Text':
        dpg.configure_item('bodyS',show=True)
        dpg.configure_item('bodyfileup',default_value="",show=False)
        dpg.configure_item('file_dialog_id',show=False)
    elif valueOption == 'By TXT file':
        dpg.configure_item('bodyS',show=False)
        dpg.configure_item('bodyfileup',default_value="",show=False)
        dpg.configure_item('txt_dialog_id',show=True)
    elif valueOption == 'HTML (Not use images embebed)':
        dpg.configure_item('bodyS',show=False)
        dpg.configure_item('bodyfileup',show=True)
        dpg.configure_item('html_dialog_id',show=True)
        dpg.configure_item('file_dialog_id',show=False)

#Function of button to attach files
def filesAttached():
    """
    This function gets the paths to attach files for sending a email.
    
    Not -> Doesn't attach files to email.
    
    Pictures -> shows multi_file_pictures dialog  but doesn't show file dialog as its message

    PDF -> shows pdf_dialog_id dialog  but doesn't show file dialog as its message
    
    Both -> shows multi_files dialog and its message but doesn't show file dialog
    
    """
    valueOption = dpg.get_value('fileoptions')
    if valueOption == 'Not':pass
    elif valueOption == 'Pictures':
        dpg.configure_item('filesattached',default_value="",show=False)
        dpg.configure_item('multi_file_pictures',show=True)
        dpg.configure_item('file_dialog_id',show=False)
    elif valueOption == 'PDF':
        dpg.configure_item('filesattached',default_value="",show=True)
        dpg.configure_item('pdf_dialog_id',show=True)
        dpg.configure_item('file_dialog_id',show=False)
    elif valueOption == 'Both':
        dpg.configure_item('filesattached',show=True)
        dpg.configure_item('multi_files',show=True)
        dpg.configure_item('file_dialog_id',show=False)

#Function to check the value of token
def tokenValue():
    """
    This function gets the path of token (TXT, .pem, .key) or the user input.
    Also return smtp service value to global variable (GMAIL, OUTLOOK, YAHOO)
    
    Manual -> Hides the option "Uplaod token using a file" and shows input for user.
        -> Gets the option of smtp service, if any  option wasn't selected, then returns ''
    
    By File -> Saves the path where is the file, and smtp service returns ''

    
    """
    global smtpServices
    global tokenSave
    valueOption = dpg.get_value('token')
    listValueOption = dpg.get_value('listsmtp')
    if valueOption == 'Manual':
        dpg.configure_item('tokenfile',default_value="",show=False)
        dpg.configure_item('listsmtp',show=True)
        dpg.configure_item('token_discover',show=False)
        dpg.configure_item('sender',show=True)
        if listValueOption == 'Gmail' and valueOption:
            tokenSave = dpg.get_value('tokeninput')
            dpg.configure_item('passinput',show=False)
            dpg.configure_item('tokeninput',show=True)
            dpg.configure_item('listsmtp',default_value="Gmail")
            smtpServices = 'smtp.gmail.com'
            
        elif listValueOption == 'Outlook':
            dpg.configure_item('passinput',show=True)
            dpg.configure_item('tokeninput',show=False)
            dpg.configure_item('listsmtp',default_value="Outlook")
            smtpServices = 'smtp-mail.outlook.com'
            tokenSave = dpg.get_value('passinput')
        elif listValueOption == 'Yahoo':
            dpg.configure_item('listsmtp',default_value="Yahoo")
            dpg.configure_item('passinput',show=True)
            dpg.configure_item('tokeninput',show=False)
            smtpServices = 'smtp.mail.yahoo.com'
            tokenSave = dpg.get_value('passinput')
        else:
            tokenSave = dpg.get_value('tokeninput')
    elif valueOption == 'By file':
        dpg.configure_item('tokenfile',default_value="",show=False)
        dpg.configure_item('listsmtp',show=False)
        dpg.configure_item('token_discover',show=True)
        dpg.configure_item('sender',show=True)
        dpg.configure_item('passinput',show=False)
        dpg.configure_item('tokeninput',show=False)
        smtpServices = ''

#Function to send with (Bcc or To)
def ccBcc():
    #Gets the boolean value.
    global hidecopy
    valueOption = dpg.get_value('ccbc')
    if valueOption == 'CC' or hidecopy==True:
        hidecopy = False
        return hidecopy
    elif valueOption == 'BCC' or hidecopy == False or hidecopy==True:
        hidecopy = True
        return hidecopy
#Functon to convert Bytes to MB
def bytesToMb(pathSizeBytes) ->float:
    """
    This function gets values of files (in bytes) and converts to MB and returns a float
    """
    file_size_kb = pathSizeBytes /1024
    file_size_mb = file_size_kb/1024
    return file_size_mb

def sizeFiles():
    """
    This function verify if the files were attached, returns the sum of all of them in MB
    If size's files is over 25.0 MB the button of sender will disappear since someone musn't send a email over
    25.0 MB. Check for every smtp service documentation. If there are not files attached so return 0.0MB.
    """
    if singlePath_2=='' and len(multiPath)==0:
        dpg.configure_item('filesizes',default_value='Size of email: {} MB'.format(0.0))
    elif singlePath_2!='' and len(multiPath)==0:
        file_info = os.stat(singlePath_2)
        file_size_bytes = file_info.st_size
        file_size_mb = bytesToMb(file_size_bytes)
        if file_size_mb> 25.0:
            dpg.configure_item('sender',show=False)
            dpg.configure_item('filesizes',default_value=f'Size of email: {file_size_mb:0.2f} MB')
        else:
            dpg.configure_item('filesizes',default_value=f'Size of email: {file_size_mb:0.2f} MB')
    elif singlePath_2!='' and len(multiPath)!=0:
        file_info_pth1 = os.stat(singlePath_2)
        sizes_files  = [os.path.getsize(element) for element in multiPath]
        sizes_files = sum(sizes_files)
        file_size_bytes = file_info_pth1.st_size + sizes_files
        file_size_mb = bytesToMb(file_size_bytes)
        if file_size_mb> 20.0:
            dpg.configure_item('sender',show=False)
            dpg.configure_item('filesizes',default_value=f'Size of email: {file_size_mb:0.2f} MB')
        else:
           dpg.configure_item('filesizes',default_value=f'Size of email: {file_size_mb:0.2f} MB')
    else:
        file_info = os.stat(singlePath_2)
        file_size_bytes = file_info.st_size
        file_size_mb = bytesToMb(file_size_bytes)
        dpg.configure_item('filesizes',default_value=f'Size of email: {file_size_mb:0.2f} MB')

#Function for reset button
def resetAll():
    global smtpServices,tokenSave,tokenPath,hidecopy
    #Returns default values for useremail and recipients
    dpg.configure_item('useremail',default_value='')
    dpg.configure_item('subject',default_value='')
    dpg.configure_item('valuerR',default_value='')
    dpg.configure_item('recipient',default_value='')
    #Returns default values for body and clean the path if any file was saved
    dpg.configure_item('valuerR',show=False)
    dpg.configure_item('fileup',default_value="",show=False)
    dpg.configure_item('bodyoptions',default_value='')
    dpg.configure_item('bodyS',default_value="",show=True)
    dpg.configure_item('bodyfileup',default_value="",show=False)
    #Cleans the path if any files were attached
    dpg.configure_item('fileoptions',default_value='')
    dpg.configure_item('filesattached',default_value="",show=False)
    dpg.configure_item('multi_file_pictures',show=False)
    #Returns default values for token and clean the path if any file was saved
    dpg.configure_item('tokeninput',default_value='',show=True)
    dpg.configure_item('tokenfile',default_value='')
    dpg.configure_item('token',default_value='')
    dpg.configure_item('passinput',default_value='',show=False)
    #Returns default values for global variables
    smtpServices = ''
    tokenSave = ''
    tokenPath = ''
    dpg.configure_item('file_dialog_id',show=False)
    #Returns default values for the list of smtp values
    dpg.configure_item('listsmtp',default_value="Gmail",show=True)
    #Returns default value for empty file
    dpg.configure_item('filesizes',default_value='Size of email: {}'.format(0.0))
    #Returns to 'To' and default value for the button
    hidecopy = False
    dpg.configure_item('ccbc',default_value='')
    #Process bar return value to 0 and its overlay is 0%
    dpg.set_value('Pbar', 0)
    dpg.configure_item('Pbar',overlay=f'0%')
#Destroy the main window and exit program
def close():
    dpg.stop_dearpygui()