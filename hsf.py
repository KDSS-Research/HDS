import requests
import os
import hashlib
from tqdm import tqdm
from urllib.parse import urlparse

def get_char_code(string):
    result = []
    for i in range(len(string)):
        if '�' in string[i]: #�
            result.append(0)
        else:
            result.append(ord(string[i]))
    return bytearray(result)
    
def download_file(url, filename):
    chunkSize = 1024
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        pbar = tqdm( unit="B", total=int( r.headers['Content-Length'] ) )
        for chunk in r.iter_content(chunk_size=chunkSize): 
            if chunk:
                pbar.update (len(chunk))
                f.write(chunk)
    return filename
    
class BrewError(Exception):
    pass
    
class DownloadError(Exception):
    pass

class hsf_downloader:
    def __init__(self, file, path_to_save='./'):
        self.file = file

        
        if not os.path.exists(file):
            raise DownloadError("File not exists.")
            
    def download(self):
        strs = open(self.file,'rb').read().split(b'\n')
        urld = strs[0].replace(get_char_code('�'),b'').decode()
        sha256 = strs[1].replace(get_char_code('�'),b'').decode()
        self.a = urlparse(urld)
        try:
            download_file(urld,os.path.basename(self.a.path))
        except:
            raise DownloadError("Link to download not working or blocked!")
        with open(os.path.basename(self.a.path),'rb') as f:
            data = f.read()
            sha256hash = hashlib.sha256(data).hexdigest()
        if sha256hash == sha256:
            print('Download complete and verified!')
        else:
            print('File Hash is not verified.')
class hsf_brew:
    def __init__(self, url, filename='brewed.hsf'):
        self.url = url
        self.fn = filename
    def brew(self):
        try:
            fcontent = requests.get(self.url)
        except:
            raise BrewError("Link to download not working or blocked!")
        try:
            os.mkdir('./temp')
        except:
            pass
        try:
            open('./temp/downloadedfile.bin','wb').write(fcontent.content)
        except:
            raise BrewError("Cant create temp file!")
        with open('./temp/downloadedfile.bin','rb') as f:
            data = f.read()
            sha256hash = hashlib.sha256(data).hexdigest()
        open(self.fn,'wb').write(get_char_code('���'+self.url+'���������������������\n'))
        open(self.fn,'ab').write(get_char_code('���'+sha256hash+'���������������������'))
        os.remove('./temp/downloadedfile.bin')
        os.rmdir('./temp')
        print('Brew completed!')