import os
#from cryptography.fernet import Fernet
from pathlib import Path



class File_man():
    def __init__(self, **kwargs):
        pass

    def clean_data(self, data, delim):
        n_data = data[2:-2]
        n_list = n_data.split(str(delim))
        return n_list

    def read_file(self, file_name, delim):
        if file_name:
            try:
                with open(file_name, "r") as rf:
                    data = rf.readlines()
                    rf.close()
                    return (self.clean_data(str(data), delim))
            except Exception as e:
                print("[READ_FILE]:[ERROR]\n>   ", str(e))
                return "NOT_FOUND"


    def write_file(self, file_name, data, delim, rwm):
        text = ""
        fc = self.check_file(file_name)

        if fc == False:
            os.system('touch ' + file_name)
            print("FILE_MADE: ", str(file_name))
            fc = True

        if fc == True:
            if type(data) == str:
                #print("WRITING STR:: ", str(data))
                text = data +str(delim)
            elif type(data) == list:
                for _ in data:
                    if len(str(_)) > 0:
                        text += str(_) + str(delim)
                    else:
                        break
                #print("WRITING LIST:: ", str(data))
            elif type(data) == str and len(data) == 0:
                text = ""
            #print(f'TEXT_TO_WRITE: \n> {text} \n> [To]: {file_name}')      
            with open(file_name, rwm) as wf:
                wf.write(text)
                wf.close()
            return

    def check_file(self, file_name):
        path_to_file = file_name
        path = Path(path_to_file)
        if path.is_file():
            #print(f'[file exists] : {file_name}')
            return True
        else:
            #print(f'![file does not exists]! : {file_name}')
            return False


    def check_folder(self, folder_name):
        if not os.path.isdir(folder_name):
            print(f"Error: {folder_name} does not exist")
            return False
        return True



    def make_dir(self, target_folder):
        try:
            is_fold = self.check_folder(target_folder)
            if is_fold == False:
                os.system('mkdir ' + target_folder)
                print("[DIR_MADE]:", str(target_folder))
            return
        except Exception as e:
            print("[ERROR]:[MAKE_FOLDER]", str(e))


    def get_file_data(self, dir):
        # Initialize an empty string to store the file data
        data = ''

        # Loop through the files in the directory
        for filename in os.listdir(directory):
          # Open the file and read its contents
          with open(os.path.join(directory, filename), 'r') as f:
            file_data = f.read()
            # Append the file data to the string, separated by the delimiter
            data += file_data + '@%$'

        # Print the resulting string
        print(data)

 #   def load_key(self):   
 #       """
 #       Loads the key from the current directory named `key.key`
 #       """
 #       return open("login.txt", "rb").read()
#
#
 #   def write_key():
 #       """
 #       Generates a key and save it into a file
 #       """
 #       key = Fernet.generate_key()
 #       with open("key.key", "wb") as key_file:
 #           key_file.write(key)    