import dearpygui.dearpygui as dpg #Import library of dearpygui for interfaces
from modules.data import recipientOptions #Call funcion to show or not values of recipients
from modules.data import callback # Call function to display the file browser
from modules.data import bodyOptions #Call function to save path or input of email body
from modules.data import filesAttached #Call function to save the path files if any file was attached
from modules.data import tokenValue #Gets values for token input or by path file
from modules.data import ccBcc #Return a boolean value if is Bcc or To
from modules.data import sizeFiles #Checks the total size of files attached
from modules.data import resetAll #Clean all options and returns default values
from modules.data import close #Quit the program
from modules.smtp import smtpSender #Module to send information to a class (smtpsender)

#Class for windows
class windowsManger:
    def __init__(self):
        #Creates a context
        self.context = dpg.create_context() 
        #Saves the path of image
        self.__pictureStartup = dpg.load_image(file="./src/emailLogo.jpeg")
        #Gets values of the image
        self.width, self.height, self.channels, self.data = self.__pictureStartup 
        #Radio button options to add recipients
        self.__radioButtonOptions = ["None","Manual", "File"] 
        #Radio button options to add a body
        self.__radioButtonBody = ["Manual Text","By TXT file","HTML (Not use images embebed)"] 
        #Radio button options to attaching files
        self.__radioButtonFiles = ["Not","Pictures","PDF","Both"]
        #Radio button options to get token
        self.__radioToken = ["Manual", "By file"]
        #SMTP services available
        self.__smtpServices = ["Gmail","Outlook","Yahoo"]
        #Recipients optinos with Bcc or CC
        self.__smtpCCBCC = ["CC","BCC"]
    #Private method to import a picture
    def __showImage(self):
        #Create texture
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=self.width, height=self.height, default_value=self.data,tag="texture_tag")
    #Private method to show file browser and kind of files.
    def __fileUpload(self):
        #File dialog id: Show optons for recipient file (i.e TXT, CSV, Excel file)
        with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", callback= callback ,width=700 ,height=400):
            dpg.add_file_extension("Source files (*.txt *.csv *.xlsx){.txt,.csv,.xlsx}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".txt", color=(255, 0, 255, 255), custom_text="[txt]")
            dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")
            dpg.add_file_extension(".xlxs", color=(0, 255, 0, 255), custom_text="[Excel]")
        #txt_dialog_id: Show optons to add a file for body (i.e TXT) and HTML is html_dialog_id
        with dpg.file_dialog(directory_selector=False,show=False,tag='txt_dialog_id',callback=callback, width=700,height=400):
            dpg.add_file_extension("Source files (*.txt){.txt}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".txt", color=(255, 0, 255, 255), custom_text="[txt]")
        with dpg.file_dialog(directory_selector=False,show=False,tag='html_dialog_id',callback=callback, width=700,height=400):
            dpg.add_file_extension("Source files (*.html){.html}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".html", color=(255, 0, 255, 255), custom_text="[html]")
        #Shows options to add pictures, PDF files or both
        with dpg.file_dialog(directory_selector=False, show=False, callback=callback, file_count=10, tag="multi_file_pictures", width=700 ,height=400):
            dpg.add_file_extension("", color=(255, 150, 150, 255))
            dpg.add_file_extension("Source files (*.png *.jpg *.jpeg *.gif){.png,.jpg,.jpeg,.gif}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".png", color=(255, 255, 0, 255))
            dpg.add_file_extension(".jpg", color=(255, 0, 255, 255))
            dpg.add_file_extension(".jpeg", color=(0, 255, 0, 255))
            dpg.add_file_extension(".gif", color=(0, 0, 255, 255))
        with dpg.file_dialog(directory_selector=False,show=False,tag='pdf_dialog_id',callback=callback, width=700,height=400):
            dpg.add_file_extension(".pdf", color=(255, 0, 255, 255), custom_text="[pdf]")
        with dpg.file_dialog(directory_selector=False, show=False, callback=callback, file_count=10, tag="multi_files", width=700 ,height=400):
            dpg.add_file_extension("", color=(255, 150, 150, 255))
            dpg.add_file_extension("Source files (*.png *.jpg *.jpeg *.gif *.pdf){.png,.jpg,.jpeg,.gif,.pdf}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".png", color=(255, 255, 0, 255))
            dpg.add_file_extension(".jpg", color=(255, 0, 255, 255))
            dpg.add_file_extension(".jpeg", color=(0, 255, 0, 255))
            dpg.add_file_extension(".gif", color=(0, 0, 255, 255))
            dpg.add_file_extension(".pdf", color=(255, 0, 255, 255), custom_text="[pdf]")
        #Shows options to add a token or password .txt,.pem,.key
        with dpg.file_dialog(directory_selector=False, show=False, callback=callback, file_count=10, tag="token_discover", width=700 ,height=400):
            dpg.add_file_extension("Source files (*.txt *.pem *.key){.txt,.pem,.key}", color=(0, 255, 0, 255))
            dpg.add_file_extension(".txt", color=(255, 0, 255, 255), custom_text="[txt]")
            dpg.add_file_extension(".pem", color=(0, 255, 0, 255), custom_text="[pem]")
            dpg.add_file_extension(".key", color=(255, 0, 255, 255), custom_text="[key]")
    #Private method to show a popup
    def __popupsEnd(self):
        #Shows a popup if all emails were sent and the data sent was right 
        with dpg.window(label="Email(s) sent", modal=True, show=False, tag="modal_id", no_title_bar=True,autosize=True):
            dpg.add_text("All emails were sent!")
            dpg.add_separator()
            with dpg.group():
                dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("modal_id", show=False),pos=(40,40))
            ModalWindow_width = dpg.get_item_width('modal_id')
            ModalWindow_height = dpg.get_item_height('modal_id')
            dpg.set_item_pos('modal_id', [int((800/2 - ModalWindow_width/2)), int((700/2 - ModalWindow_height/2))])
        #Shows a popup if any error was ocurred 
        with dpg.window(label='Error',modal=True,show=False,tag='error_id',no_title_bar=True,autosize=True):
            dpg.add_text("Oops! Maybe you didn't fill some blank spaces or your data is wrong, make sure your information is right")
            dpg.add_text("All emails were sent!")
            dpg.add_separator()
            with dpg.group():
                dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("error_id", show=False),pos=(350,60))
            ModalWindow_width = dpg.get_item_width('error_id')
            ModalWindow_height = dpg.get_item_height('error_id')
            dpg.set_item_pos('error_id', [int((800/2 - ModalWindow_width/2)), int((750/2 - ModalWindow_height/2))])
    #Method to show all interface and buttons
    def startWindow(self):
        self.__fileUpload() #Private method to open file browser
        self.__showImage() #Private method to show main image
        self.__popupsEnd()#Private method to show the popops
        #Create main window
        with dpg.window(tag="Main Menu"):
            #Shows main image
            dpg.add_image('texture_tag',width=200,height=200,indent=260)
            #Shows text
            dpg.add_text("Welcome!")
            #Creates a group to type author email and subject
            with dpg.group(horizontal=True):
                dpg.add_text("Author Email: ")
                dpg.add_input_text(on_enter=True,hint="Your Email" ,tag='useremail',width=210,height=210)
                dpg.add_text("Subject: ")
                dpg.add_input_text(on_enter=True,hint='Enter your subject',tag='subject',width=350,height=350)
            #Creates a group to add recipients by user or using a plain text
            dpg.add_text("Add recipient emails by:")
            with dpg.group(horizontal=True):
                dpg.add_radio_button(self.__radioButtonOptions,label='Recipients',callback=recipientOptions,horizontal=True,tag='recipient')
                dpg.add_input_text(show=False,callback=recipientOptions,tag='valuerR',width=200,height=200,hint="Add a recipient")
            dpg.add_text(default_value='No file selected',show=False,tag='fileup')
            #Creates a group to add a body by user or attaching a file (TXT or HTML)
            dpg.add_text("Body Format: ")
            with dpg.group(horizontal=False):
                dpg.add_radio_button(self.__radioButtonBody,callback=bodyOptions,label='Body Options',horizontal=True,tag='bodyoptions')
                dpg.add_input_text(show=True,callback=bodyOptions,tag='bodyS',hint='Type your body text')
                dpg.add_text(default_value='No file selected',show=False,tag='bodyfileup')
            #Creates a group to attach files (pictures or PDF files)
            dpg.add_text("(OPTIONAL) Add pictures, PDF Files or both: ")
            dpg.add_radio_button(self.__radioButtonFiles,callback=filesAttached,label='File Options',horizontal=True,tag='fileoptions')
            dpg.add_text(default_value='No file selected',show=False,tag='filesattached')
            dpg.add_text("ADD TOKEN/ USER-PASSWORD (You need)")
            #Creates a group to add a token
            with dpg.group(horizontal=True):
                dpg.add_radio_button(self.__radioToken,callback=tokenValue,label='Token',horizontal=True,tag='token')
                dpg.add_text("Services: ")
                dpg.add_text(default_value='No file selected',show=False,tag='tokenfile')
                dpg.add_input_text(hint='Type your email password',width=240,height=240,show=False,tag='passinput',password=True)
                dpg.add_input_text(hint='Type your token without spaces',width=240,height=240,show=True,tag='tokeninput',password=True)
                dpg.add_listbox(items=self.__smtpServices,num_items=1,callback=tokenValue,tag='listsmtp', width=100,indent=450,show=True,default_value='Gmail',tracked=True)
            #Creates a group to update the size of email if any file was uploaded
            with dpg.group(horizontal=True):
                dpg.add_text("CC/BCC:")
                dpg.add_radio_button(self.__smtpCCBCC,callback=ccBcc,label='',horizontal=True,tag='ccbc')
                dpg.add_text(default_value='Size of email: {}'.format(0.0),tag='filesizes',show=True)
                dpg.add_button(label='Update sizes',callback=sizeFiles)
            #Creates a group for process bar status
            with dpg.group(horizontal=True):
                dpg.add_progress_bar(label='Progress bar',tag='Pbar',default_value=0.0,width=800,height=15,overlay="0%")
            #Creates a group to send the data to a class, reset values or exit program
            with dpg.group(horizontal=True):
                dpg.add_button(label='Send',callback=smtpSender,tag='sender',show=False,width=100,height=50,indent=480,pos=(800,580))
                dpg.add_button(label='Quit!',callback=close,tag='quit',show=True,width=100,height=50,indent=600,pos=(800,580))
                dpg.add_button(label='Reset!',callback=resetAll,tag='reset',show=True,width=100,height=50,indent=350)
        #Create a viewport with icons and size of screen
        dpg.create_viewport(title='SMTP SENDER', width=850, height=700,small_icon='./src/email-sent.png',large_icon='./src/email-sentL.png',resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        #Set main menu as primary window
        dpg.set_primary_window("Main Menu",True)
        dpg.start_dearpygui()
        dpg.destroy_context()