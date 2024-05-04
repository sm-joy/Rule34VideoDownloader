from os import makedirs
from os.path import exists

from downloader import VideoDownloader
from utils import ColorUtils
import settings

def main() -> int:
    #do it - make it so that if the user wants to download multiple files then use sub url accessing 

    if not exists(settings.SAVE_PATH):
        makedirs(settings.SAVE_PATH)
    
    driver = None
    
    while(True):
        ColorUtils.Print_Colored(ColorUtils.Colors["Green_Light"], "[1] Download A Video\n[2] Exit")
        
        option = ColorUtils.Scan_Colored(ColorUtils.Colors["White"], "Choose Option (type 1 or 2) -> ")
        
        
        if option == '2':
            break
        elif option == '1':
            
            if driver == None:
                driver = VideoDownloader(pDriver_Path=settings.DRIVER_PATH)

            link_text = ColorUtils.Scan_Colored(ColorUtils.Colors["White"], "Type the link here -> ")
            
            driver.download_video(pSave_Path=settings.SAVE_PATH , pVideo_link=link_text)
        else:
            ColorUtils.Print_Colored(ColorUtils.Colors["Red"], "\nInvaid Option!")
    
    
    if not driver == None:
        driver.close_driver()
        
    return 0

if __name__ == "__main__":
    main()
