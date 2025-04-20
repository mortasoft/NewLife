# Read File

import ftplib

# Read TXT File
def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()
    
def connect_ftp(url, user, passw):
    try:
        # Connect to the FTP server
        ftp = ftplib.FTP(url)
        ftp.login(user, passw)
        print(ftp.getwelcome())
        ftp.quit() # Close the connection
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True
    
# Process each line of the file
def process_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            try:
                lines = line.split(':')
                if len(lines) == 4:
                    url = lines[1].replace('//', '').strip()
                    user = lines[2].strip()
                    passw = lines[3].strip()
                    connect_ftp(url, user, passw)
                if len(lines) == 5:
                    url = lines[1].replace('//', '').strip()
                    user = lines[2].strip()
                    passw = lines[4].strip()
                    connect_ftp(url, user, passw)
            except Exception as e:
                print(f"Error: {e}")
                continue
                

process_file('file.txt')