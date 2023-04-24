import os
from passlib.hash import sha512_crypt
import zipfile
class Services_User:
    def checkUser(seld,userName,userPassword):
        shadow = '/etc/shadow'
        os.system('sudo -S chmod o+r /etc/shadow')
        with open(shadow, 'r') as f:
            lines = f.readlines()
        os.system('sudo -S chmod o-r /etc/shadow')
        for line in lines:
            if (userName == line.split(':')[0]):
                hashed = sha512_crypt.hash(userPassword)
                if sha512_crypt.verify(userPassword, hashed):
                    return True
        return False
    def nb_files(uself,userName):
        user_dir = '/home/'+userName
        nbfiles = 0
        for dirictories, name_of_dir, files in os.walk(user_dir):
            #print(dirnames)
            nbfiles += len(files)
        #print(file_count)
        return nbfiles
    def nb_dir(self,userName):
        user_dir = '/home/'+userName
        nbdir = 0
        for dirictories, name_of_dir, files in os.walk(user_dir):
            nbdir += len(name_of_dir)
        return nbdir
    def total_size(self,userName):
        user_dir = '/home/'+userName
        nbtotal = 0
        for dirictories, name_of_dir, files in os.walk(user_dir):
            nbtotal += len(name_of_dir)
            nbtotal += len(files)
        return nbtotal
    def rechercher(self,userName,fileName):
        user_dir = '/home/'+userName
        dirs=[]
        for dirictories, name_of_dir, files in os.walk(user_dir):
            if(fileName in files):
                dirs.append(os.path.abspath(fileName))
        print(dirs)
        return dirs
    def getDirectories(self,userName):
        user_dir = '/home/'+userName
        dirs = []
        if os.path.isdir(user_dir):
            dirs = [d for d in os.listdir(user_dir)]
        return dirs
    def getDirectoriesall(self,userName):
        user_dir = '/home/'+userName
        dirs = [d for d in os.listdir(user_dir)]
        return dirs
    def download(self,username):
        home_dir = os.path.expanduser('/home/'+username)
        zip_filename = "/home/"+username+"/"+username+".zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, home_dir))
    def getFiles(self,userName):
        user_dir = '/home/'+userName
        files = [d for d in os.listdir(user_dir) if(os.path.isfile(os.path.join(user_dir,d)))]
        return files
    def firstPath(newPath):
        return '/home/'+newPath
if __name__ == '__main__':
    #print(Services_User().checkUser('med','1234'))
    Services_User().total_size('mohammed')
    #print(Services_User().rechercher('mohammed', 'login.html'))

