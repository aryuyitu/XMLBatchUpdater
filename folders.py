import os
import shutil #this might not be needed since copy tree does not work
from distutils.dir_util import copy_tree #this will be needed for the copy tree function
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import zipfile
import lxml.etree as ET #lxml needs to be installed with the command: pip3 install lxml https://lxml.de/tutorial.html
import uuid
from datetime import datetime

#all of the print statements are there for sanity oft he user. Nothing else shows up while the function is running
#so to see if the process is running the user can look at the cmd

def browse(e_title,entry_location,label_location): #this function will browse files, then replace the entry text and mark which file you have chosen
    if (e_title == "Select File"):
        f_path = askopenfilename(initialdir="/", title=e_title)
    else:
        f_path = filedialog.askdirectory(initialdir="/", title=e_title)
    entry_location.delete(0, "end") 
    entry_location.insert(0, f_path)
    label_location.config(text = "You have chosen: " + get_name(f_path)) 

def get_name(path): #this function will take the path, then return the name of the file/folder
    path_split = path.split('/')
    return path_split[len(path_split)-1]    

def copy(source_dir, destination_dir, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk): #this function will copy the contents of the source into the dest folder, including all folders and zip files
    print("running the copy function") #for testing
    if(copy_everything_chk):
        copy_tree(source_dir,destination_dir)
    else:
        for filename in os.listdir(source_dir):
            file = os.path.join(source_dir, filename)
            if os.path.isfile(file):
                if(filename.endswith(".xml") or (filename.endswith(".zip") and copy_zips_chk)):
                    shutil.copy2(file,destination_dir)
            elif(copy_folders_chk): #its a folder, so make a new folder with the same filename, then run the copy function again, except the destination will be the new folder name
                new_folder_path = destination_dir + "/" + filename
                os.mkdir(new_folder_path)
                copy(file, new_folder_path, copy_zips_chk, extract_zips_chk, copy_folders_chk, False)

def get_parent_directory(path):
    name = len(get_name(path))
    parent = path[:len(path)-name-1]
    return (parent)

def can_read(path):
    return (os.access(path, os.R_OK))

def can_write(path):
    return (os.access(path, os.W_OK))

def update(xsl_file_path, parameters_file_path, update_dir, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk, updatelog_path): #this function will run if all the checks pass, and the files are successfully copied to the destination folder
    for filename in os.listdir(update_dir):
        file = os.path.join(update_dir, filename) #i think this is the path to the file currently being iterated
        if os.path.isfile(file): #if its a file:
            if (filename.endswith(".xml")):#if it is an xml file:
                update_parameters(parameters_file_path,filename)
                update_xml(file,xsl_file_path,updatelog_path,parameters_file_path)
            elif ((filename.endswith(".zip") and copy_zips_chk)): #make new folder for the zip, and extract everything in there
                new_folder_name = filename[:len(filename)-4]
                new_folder_path = update_dir + "/" + new_folder_name
                os.mkdir(new_folder_path)
                try: #testing incase there is an error extracting the files
                    with zipfile.ZipFile(file, 'r') as zip_ref: #extract the documents into that new folder
                        zip_ref.extractall(new_folder_path)
                except:
                    with open(updatelog_path, "a") as updatelog:
                        updatelog.write("Error occurred trying to extract the contents from: " + file +"\n\n")
                else:
                    os.remove(file) #delete the old zip file
                    update(xsl_file_path, parameters_file_path, new_folder_path, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk, updatelog_path)
                    if not(extract_zips_chk): #then you need to zip it back up, and delete the temp folder
                        #print('trying to zip') for testing
                        shutil.make_archive(new_folder_path, 'zip', new_folder_path)
                        shutil.rmtree(new_folder_path)
        elif(copy_folders_chk): #(this is the folder case)
            folder_path = update_dir + "/" + filename
            update(xsl_file_path, parameters_file_path, folder_path, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk, updatelog_path)

def initial_parameters(num_of_guids, full_document_name, parameters_file_dir): #full_document_name should have .xml at the end
    #this function will create the initial parameters document
    current_datetime = datetime.now()
    parameters = ET.Element('parameters')

    filename = ET.SubElement(parameters, "filename")
    filename.text = full_document_name

    currentdate = ET.SubElement(parameters, "currentdate")
    currentdate.text = ("%s-%s-%s" % (current_datetime.strftime("%d"),current_datetime.strftime("%m"),current_datetime.strftime("%Y")))

    currenttime = ET.SubElement(parameters, "currenttime")
    currenttime.text = current_datetime.strftime("%X")

    guids_parent = ET.SubElement(parameters, "GUIDs")

    for i in range(num_of_guids):
        guid = ET.SubElement(guids_parent, "GUID")
        guid.text = str(uuid.uuid4()) #this can be changed based on the type of guid needed

    print(ET.tostring(parameters, pretty_print=True).decode("UTF-8")) #for testing

    with open(parameters_file_dir,"w") as file: #need to make this into a file
        file.write(ET.tostring(parameters, pretty_print=True).decode("UTF-8"))
    
def update_parameters(parameters_file_path, filename): #this function will edit the parameters file
    current_datetime = datetime.now()
    with open(parameters_file_path, "r") as file:#open the file:
        parameters = ET.fromstring(file.read())
    for element in parameters.iter():#iterate through all elements in xml file provided:
        if (element.tag == 'GUID'):
            element.text = str(uuid.uuid4())
            #print('edited guid')
        elif (element.tag == 'filename'):
            element.text = filename
            #print('edited filename')
        elif (element.tag == 'currentdate'):
            element.text = ("%s-%s-%s" % (current_datetime.strftime("%d"),current_datetime.strftime("%m"),current_datetime.strftime("%Y")))
            #print('edited current date')
        elif (element.tag == 'currenttime'):
            element.text = current_datetime.strftime("%X")
            #print('edited current time')

    print(ET.tostring(parameters, pretty_print=True).decode("UTF-8")) #for testing
    
    with open(parameters_file_path,"w") as file: #need to make this into a file
        file.write(ET.tostring(parameters, pretty_print=True).decode("UTF-8"))

def update_xml(xml_file_path,xsl_file_path,updatelog_path,parameters_file_path): #this updates the xml file, and writes over it at the end
    print('updating the xml right now!')
    updatelog = open(updatelog_path, "a")
    updatelog.write("Attempting to update " + xml_file_path +" by running against: " + get_name(xsl_file_path) +"\n")
    print("Attempting to update " + xml_file_path +" by running against: " + get_name(xsl_file_path))
    xslt = ET.parse(xsl_file_path)
    try:
        dom = ET.parse(xml_file_path)
    except:
        updatelog.write("Error occurred while parsing " + xml_file_path + "\n\n")
        print("Error occurred while parsing " + xml_file_path)
    else:
        try: 
            transform = ET.XSLT(xslt)
            newdom = transform(dom)
        except:
            updatelog.write("Error occurred while transforming " + xml_file_path + "\n\n")
            print("Error occurred while transforming " + xml_file_path)
        else:
            updatelog.write("Parameters used: \n")
            with open(xml_file_path,"w") as file:
                file.write(ET.tostring(newdom, pretty_print=True).decode("UTF-8"))
            with open(parameters_file_path, "r") as parameters:
                updatelog.write(parameters.read())
            updatelog.write("Successfully updated. \n\n")
            print("Successfully updated.")
    updatelog.close()


#---------------testing here---------------#
#IncrementVersionNumber
#brokenxsl

#try:
#    xsl_test = ET.parse("C:/Users/alexa/UWaterloo/Textbooks/IncrementVersionNumber.xsl")
#    ET.XSLT(xsl_test)
#except:
#    print('an error occurred')
