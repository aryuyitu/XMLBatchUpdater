import tkinter as tk
from tkinter import DISABLED #disabled will allow me to disable a check button, use mes
import folders

def main():
    def enter_data():
        #fn_chk = filename_check_var.get()
        #cur_date_chk = current_date_check_var.get()
        copy_zips_chk = into_zip_check_var.get()
        extract_zips_chk = extract_zip_files_check_var.get()
        copy_folders_chk = into_folders_check_var.get()
        copy_everything_chk = copy_everything_check_var.get()
        valid_xsl = True

        num_guids = int(guid_entry.get())
        xml_path = xml_entry.get()
        xsl_path = xsl_entry.get()
        new_path = new_fol_entry.get()

        new_path_directory = folders.os.listdir(new_path)
        xml_path_directory = folders.os.listdir(xml_path)
        #need to make a case where the folder is empty, or read and write permissions are disabled
        parameters_dir = folders.get_parent_directory(xsl_path)
        parameters_file_dir = (parameters_dir + "/" + "Parameters.xml")
        folders.initial_parameters(num_guids,'dummy_name',parameters_file_dir)

        try: #this is to make sure the that xsl file is valid; if it can be parsed and transformed
            xsl_test = folders.ET.parse(xsl_path)
            folders.ET.XSLT(xsl_test)
        except:
            valid_xsl = False
            print("something went wrong with the xsl file") #for testing

        if (num_guids < 0) or (num_guids > max_guid):
            tk.messagebox.showwarning(title="Error", message="Please enter the number of GUIDs from 0-100000.")
        elif not(xml_path and folders.os.path.isdir(xml_path)):
            tk.messagebox.showwarning(title="Error", message="Please enter a valid path to the XML folder.")
        elif not(xsl_path and xsl_path.endswith(".xsl")): #add the filetype for xsl files
            tk.messagebox.showwarning(title="Error", message="Please enter a valid path to the XSL file.")
        elif not(new_path and folders.os.path.isdir(new_path)):
            tk.messagebox.showwarning(title="Error", message="Please enter a valid path for the new folder.")
        elif len(new_path_directory) != 0:
            tk.messagebox.showwarning(title="Error", message="Please enter an empty folder for the new folder.")
        elif len(xml_path_directory) == 0:
            tk.messagebox.showwarning(title="Error", message="Please do not enter an empty folder for the XML folder.")
        elif not(folders.can_read(xml_path)):
            tk.messagebox.showwarning(title="Error", message="The program does not have read access to the XML folder")
        elif not(folders.can_write(new_path)):
            tk.messagebox.showwarning(title="Error", message="The program does not have write access to the new folder")
        elif not(valid_xsl):
            tk.messagebox.showwarning(title="Error", message="There was an error with the XSL file.")
        elif not(folders.can_write(xsl_path)):
            tk.messagebox.showwarning(title="Error", message="The program does not have read access to the xsl folder")
        elif not(folders.can_read(xsl_path)):
            tk.messagebox.showwarning(title="Error", message="The program does not have write access to the xsl folder")
        else:
            if(tk.messagebox.askyesno("Initial checks complete", "Do you want to continue the process?")):
                print("the path to the xml folder is: ", xml_path, "with the name of the file being: ", folders.get_name(xml_path))
                print("the path to the xsl file is: ", xsl_path, " with the name being: ", folders.get_name(xsl_path))
                print("and the place for the new files will be: ", new_path, " with the name being: ", folders.get_name(new_path))
                print("number of guids: ", num_guids)
                folders.copy(xml_path, new_path, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk)
                print("copy function is complete")

                updatelog_path = (new_path + "/" + folders.get_name(new_path) + "_" + folders.get_name(xsl_path) + "_updatelog.txt" )
                folders.update(xsl_path, parameters_file_dir, new_path, copy_zips_chk, extract_zips_chk, copy_folders_chk, copy_everything_chk, updatelog_path)
                tk.messagebox.showinfo("Complete", "The whole operation has been completed") 


    #for speeding up the testing process; return to empty when done testing
    #initial_xml_path = "C:/Users/alexa/UWaterloo/Textbooks/source"
    #initial_xsl_path = "C:/Users/alexa/UWaterloo/Textbooks/IncrementVersionNumber.xsl"
    #initial_new_path = "C:/Users/alexa/UWaterloo/Textbooks/destination"

    initial_xml_path = ""
    initial_xsl_path = ""
    initial_new_path = ""

    window = tk.Tk()          
    window.title("XML Batch Updater Tool")

    #------------Frames------------#
    frame = tk.Frame(window)
    frame.pack()

    #------------Description------------#
    desc_frame = tk.Frame(frame)
    desc_frame.grid(row=0, column=0)

    description = tk.Label(desc_frame, text="This tool updates a batch of XML files located inside a folder, using the XSL file specified")
    description.pack()

    #------------XML Frame------------#
    xml_loc_frame = tk.Frame(frame)
    xml_loc_frame.grid(row=1, column=0)

    xml_desc = tk.Label(xml_loc_frame, text="Choose the folder location of XML files to be updated:")
    xml_entry = tk.Entry(xml_loc_frame)
    xml_entry.insert(0,initial_xml_path) #this was for testing purposes
    xml_browse = tk.Button(xml_loc_frame, text="Browse...", command=lambda: folders.browse("Select Folder", xml_entry, xml_chosen))
    xml_chosen = tk.Label(xml_loc_frame, text="")

    xml_desc.grid(row=0, column=0, columnspan=2)
    xml_entry.grid(row=1, column=0, columnspan=2, sticky="ew")
    xml_browse.grid(row=1, column=2)
    xml_chosen.grid(row=2,column=0)
    #------------XSL Frame------------#
    xsl_loc_frame = tk.Frame(frame)
    xsl_loc_frame.grid(row=2, column=0)

    xsl_desc = tk.Label(xsl_loc_frame, text="Choose the XSL file to be run against the XML files:")
    xsl_entry = tk.Entry(xsl_loc_frame)
    xsl_entry.insert(0,initial_xsl_path) #this was for testing purposes
    xsl_browse = tk.Button(xsl_loc_frame, text="Browse...", command=lambda: folders.browse("Select File", xsl_entry, xsl_chosen))
    xsl_chosen = tk.Label(xsl_loc_frame, text="")

    xsl_desc.grid(row=0, column=0, columnspan=2)
    xsl_entry.grid(row=1, column=0, columnspan=2, sticky="ew")
    xsl_browse.grid(row=1, column=2)
    xsl_chosen.grid(row=2,column=0)
    #------------New Folder Frame------------#
    new_fol_frame = tk.Frame(frame)
    new_fol_frame.grid(row=3, column=0)

    new_fol_desc = tk.Label(new_fol_frame, text="Choose the location for all the new, updated files to be stored:")
    new_fol_entry = tk.Entry(new_fol_frame)
    new_fol_entry.insert(0,initial_new_path) #this was for testing purposes
    new_fol_browse = tk.Button(new_fol_frame, text="Browse...", command=lambda: folders.browse("Select Folder", new_fol_entry, new_fol_chosen))
    new_fol_chosen = tk.Label(new_fol_frame, text="")

    new_fol_desc.grid(row=0, column=0, columnspan=2)
    new_fol_entry.grid(row=1, column=0, columnspan=2, sticky="ew")
    new_fol_browse.grid(row=1, column=2)
    new_fol_chosen.grid(row=2,column=0)

    #------------Check Boxes Frame------------#
    check_frame = tk.Frame(frame)
    check_frame.grid(row=4, column=0)

    #setting int variables for the checkboxes (either 1 or 0)
    #filename_check_var = tk.IntVar()
    #current_date_check_var = tk.IntVar()
    #current_time_check_var = tk.IntVar()
    into_zip_check_var = tk.IntVar()
    into_folders_check_var = tk.IntVar()
    extract_zip_files_check_var = tk.IntVar()
    copy_everything_check_var = tk.IntVar()


    #filename_check = tk.Checkbutton(check_frame, text="Include Filename",                       variable=filename_check_var)
    #current_date_check = tk.Checkbutton(check_frame, text="Include Current Date and Time", variable=current_date_check_var)
    #current_time_check = tk.Checkbutton(check_frame, text="Include Current Date and Time", variable=current_date_check_var)
    copy_everything_check = tk.Checkbutton(check_frame, text="Copy every file (including non .xml files) into new folder",  variable=copy_everything_check_var)
    into_zip_check = tk.Checkbutton(check_frame, text="Update .xml files inside .zip files",                                variable=into_zip_check_var)
    extract_zip_files_check = tk.Checkbutton(check_frame, text="Extract .xml files from .zip files into the new folder",    variable=extract_zip_files_check_var)
    into_folders_check = tk.Checkbutton(check_frame, text="Update Files inside Sub-Folders",                                variable=into_folders_check_var)
    
    guid_lbl = tk.Label(check_frame, text="Number of GUIDs per file:")
    max_guid = 100000
    guid_entry = tk.Spinbox(check_frame, from_=0, to=max_guid)

    #filename_check.grid(row=0, column=0, sticky='w')
    #current_date_check.grid(row=1, column=0, sticky='w')
    #current_time_check.grid(row=2, column=0, sticky='w')
    guid_lbl.grid(row=0,column=0,sticky='w')
    guid_entry.grid(row=1,column=0,sticky='w')
    copy_everything_check.grid(row=2,column=0,sticky='w')
    into_zip_check.grid(row=3, column=0, sticky='w')
    extract_zip_files_check.grid(row=4, column=0, sticky='w')
    into_folders_check.grid(row=5, column=0, sticky='w')
    
    

    #------------run Frame------------#
    run_frame = tk.Frame(frame)
    run_frame.grid(row=5, column=0)

    run_btn = tk.Button(run_frame, text="Run", command=lambda: enter_data())
    cancel_btn = tk.Button(run_frame, text="Cancel", command=window.destroy)

    run_btn.grid(row=0,column=0, sticky='e')
    cancel_btn.grid(row=0,column=1, sticky='e')

    #setting the padding for all widgets and frames
    for frames in frame.winfo_children():
        frames.grid_configure(sticky='news',padx=20,pady=10)
        for widgets in frames.winfo_children():
            widgets.grid_configure(padx=10)

    window.mainloop()


if __name__ == "__main__":
    main()