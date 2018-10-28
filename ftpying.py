import os
import shutil
from zipfile import ZipFile as zf
from ftplib import FTP
ftp=FTP('FTP Location')
ftp.login(user='username',passwd='password')
ftp.cwd('dailyfeeds')
filelists=ftp.nlst()
folder_lists=open("log.txt","r").readline()
logs=open('log.txt',"a")
dir='EnY_HTMLs\\'
html_file_List=[]
if os.path.exists(dir):
    print("Directory Exists")
else:
    os.mkdir(dir)

for filename in filelists:
    ftp.cwd('dailyfeeds')
    if '.zip' in filename and filename not in folder_lists:
        print("Downloading from following location: ")
        print(ftp.pwd())
        local_file=os.path.join(dir,filename)
        file=open(local_file,'wb')
        ftp.retrbinary('RETR '+ filename ,file.write)
        print(filename,' file got downloaded to ',local_file)
        file.close()
        htm_file=local_file.split('EnY_HTMLs\\')[1][0:int(len(local_file.split('EnY_HTMLs\\')[1])-4)]+'.htm'
        src_htm=dir+htm_file
        html_file=local_file.split('EnY_HTMLs\\')[1][0:int(len(local_file.split('EnY_HTMLs\\')[1])-4)]+'.html'
        dest_html=dir+html_file
        zipf_ref=zf(local_file,'r')
        zipf_ref.extract(htm_file,dir)
        zipf_ref.close()
        'os.remove(local_file)'
        os.rename(dir+htm_file,dir+html_file)
        html_file_List.append(dir+html_file)
        logs.write(filename+", ")
    elif '.htm' in filename and filename not in folder_lists:
        print("Downloading from following location: ")
        print(ftp.pwd())
        local_file=os.path.join(dir,filename)
        file=open(local_file,'wb')
        ftp.retrbinary('RETR '+ filename ,file.write)
        print(filename,' file got downloaded to ',local_file)
        file.close()
        htm_file=local_file.split('EnY_HTMLs\\')[1]
        src_htm=dir+htm_file
        html_file=local_file.split('EnY_HTMLs\\')[1][0:int(len(local_file.split('EnY_HTMLs\\')[1])-4)]+'.html'
        dest_html=dir+html_file
        os.rename(src_htm,dest_html)
        html_file_List.append(dest_html)
        logs.write(filename+", ")
        'shutil.copy(src_htm,dest_html)'
    elif '.csv' in filename:
        print("not needed")
    else:
        ftp.cwd(filename)
        folder=ftp.pwd().split('/')[-1]+'\\'
        daily_feed_Loc=dir+folder
        zip_folder=daily_feed_Loc+'zips\\'
        if filename in folder_lists:
            print(filename+" Already Downloaded")
            continue
        else:
            os.mkdir(daily_feed_Loc)
            os.mkdir(zip_folder)
        if 'safe' in ftp.nlst():
            print("Downloading from following location: ")
            ftp.cwd('safe')
            filelist = [] #to store all files
            ftp.retrlines('LIST',filelist.append)
            if 'total 0' not in filelist[-1]:
                print(ftp.pwd())
                files=ftp.nlst()
                'logs.write("Files downloaded from "+ftp.pwd()+"\n")'
                logs.write(ftp.pwd().split('dailyfeeds/')[1].split('/safe')[0]+", ")
                for f in files:
                    if '.zip' in f :
                        local_file=os.path.join(zip_folder,f)
                        'local_file=os.path.join(daily_feed_Loc,f)'
                        file=open(local_file,'wb')
                        ftp.retrbinary('RETR '+ f ,file.write)
                        print(f,' file got downloaded to ',local_file)
                        file.close()
                        htm_file=local_file.split('zips\\')[1][0:int(len(local_file.split('zips\\')[1])-4)]+'.htm'
                        "htm_file=local_file.split(folder)[1][0:int(len(local_file.split(folder)[1])-4)]+'.htm'"
                        src_htm=daily_feed_Loc+htm_file
                        html_file=local_file.split('zips\\')[1][0:int(len(local_file.split('zips\\')[1])-4)]+'.html'
                        "html_file=local_file.split(folder)[1][0:int(len(local_file.split(folder)[1])-4)]+'.html'"
                        dest_html=daily_feed_Loc+html_file
                        zipf_ref=zf(local_file,'r')
                        zipf_ref.extract(htm_file,daily_feed_Loc)
                        zipf_ref.close()
                        'os.remove(local_file)'
                        os.rename(src_htm,dest_html)
                        'logs.write(f+" Downloaded from "+ftp.pwd()+"\n")'

                    elif '.htm' in f:
                        local_file=os.path.join(daily_feed_Loc,f)
                        file=open(local_file,'wb')
                        ftp.retrbinary('RETR '+ f ,file.write)
                        print(f,' file got downloaded to ',local_file)
                        file.close()
                        htm_file=local_file.split(folder)[1]
                        src_htm=daily_feed_Loc+htm_file
                        html_file=local_file.split(folder)[1][0:int(len(local_file.split(folder)[1])-4)]+'.html'
                        dest_html=daily_feed_Loc+html_file
                        os.rename(src_htm,dest_html)
                        'logs.write(f+" Downloaded from "+ftp.pwd()+"\n")'
                        'shutil.copy(src_htm,dest_html)'
            else:
                shutil.rmtree(daily_feed_Loc, ignore_errors=True)
                print(ftp.pwd()+" folder is empty.")
                'logs.write(ftp.pwd()+" folder is empty."+"\n")'
                logs.write(ftp.pwd().split('dailyfeeds/')[1].split('/safe')[0]+", ")

        else:
            shutil.rmtree(daily_feed_Loc, ignore_errors=True)
            print("Safe folder not present in: "+ftp.pwd())

ftp.quit()

print("All file Copied to ",dir)
