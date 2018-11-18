'''
Created on Nov 1, 2018
Upload and Download to google drive
@author: nantha
'''


from Authenticate import Authentication
from Authenticate import Watcher


if __name__ == '__main__':
    gauthObject = Authentication()
    gdrive = gauthObject.authenticate()
    
    if gdrive is not None:
        watcher = Watcher()
        watcher.register(gdrive)
        
    
        