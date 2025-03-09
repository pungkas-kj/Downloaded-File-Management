
from os import scandir, rename 
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Bagian directory/tempat yang dituju atau source nya 
source_directory = "C:\\Users\\Admin\\Downloads"
dir_video ="C:\\Users\\admin\\Videos\\Downloads\\Video"
dir_audio = "C:\\Users\\admin\\Videos\\Downloads\\Audio"
dir_image = "C:\\Users\\Admin\\Videos\\Downloads\\Image photo"
dir_Zip = "C:\\Users\\Admin\\Videos\\Downloads\\ZIP Files"
dir_docs = "C:\\Users\\Admin\\Videos\\Downloads\\Documents"


image_extensions = [".jpg", ".jpeg", ".png"]# ".jpe", ".jif", ".jfif", ".jfi", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                   ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]

zip_extensions = [".zip"]

docs_extensions = [".doc", ".docx", ".odt",".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]



def make_unique(tujuan, nama):
    nama_file, extensi = splitext(nama)
    plus_counter = 1
    #Kalo file udah exist/ada sebelumnya, bakal nambahin nomor diujung nama file baru sebagai pembeda
    while exists (f"{tujuan}/{nama}") :
        nama = f"{nama_file}(str{(plus_counter)}){extensi}"
        plus_counter += 1

        return nama
    
def pindah_ke(tujuan, masuk, nama):
    if exists (f"{tujuan}/{nama}") :
        nama_unique = make_unique(tujuan,nama)
        namalama = join(tujuan,nama)
        nama_baru = join(tujuan, nama_unique)
        rename (namalama, nama_baru)
    move(masuk, tujuan) 


class pengubah(FileSystemEventHandler) :
    #Fungsi ini jalan kalau ada perubahan. misal download, file yang baru aja di downloaddan yang sudah ada di file download akan di pindahin sesuai tujuan yang di definisikan
    def on_modified(self, event):
        with scandir(source_directory) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry,name)
                self.check_video_files(entry,name)
                self.check_image_files(entry,name)
                self.check_zip_files(entry,name)
                self.check_docs_files(entry,name)


    def check_audio_files(self, entry, name): #Untuk cek semua file audio dengan extensi yang udah di definisikan
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                pindah_ke(dir_audio, entry, name) 
                logging.info ("File dipindahkan : {name}")

    def check_video_files(self, entry, name): #Untuk check semua file video
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                pindah_ke(dir_video, entry, name) 
                logging.info ("File video dipindahkan : {name}")

    def check_image_files(self, entry, name): #Untuk check semua file foto/image
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                pindah_ke(dir_image, entry, name) 
                logging.info ("File foto dipindahkan : {name}")

    def check_zip_files(self, entry, name):  #Untuk check semua file ZIP
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                pindah_ke(dir_Zip, entry, name) 
                logging.info ("File foto dipindahkan : {name}")

    def check_docs_files(self, entry, name):  #Untuk check semua file document
        for docs_extension in docs_extensions:
            if name.endswith(docs_extension) or name.endswith(docs_extension.upper()):
                pindah_ke(dir_docs, entry, name) 
                logging.info ("File document dipindahkan : {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_directory
    event_handler = pengubah()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    #PAKE CTRL+C BUAT BERHENTIIN CODE NYA DI TERMINAL