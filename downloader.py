from selenium.webdriver import ChromeService, ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

import requests
from tqdm import tqdm
from winsound import MessageBeep, MB_ICONASTERISK
from os.path import join, exists

from utils import ColorUtils
import settings



class VideoDownloader:
    def __init__(self, pDriver_Path: str) -> None:
        
        self.options = ChromeOptions()
        for arg in ["--headless=new", "--no-sandbox", "--disable-gpu", "--log-level=3", "--silent", "--disable-dev-shm-usage"]:
            self.options.add_argument(arg)
            
        self.driver =  Chrome(options=self.options, service=ChromeService(executable_path=pDriver_Path))
        
        self.get_link("https://rule34video.com") #for quick loading
    
    
    def get_download_link(self, pVideo_link: str) -> str:
        if self.get_link(pVideo_link):
            return self.locate_element("video[class='fp-engine']").get_attribute("src") 
        return "Internet Connection Error"
    
    def get_link(self, pLink: str) -> bool:
        try:
            self.driver.get(pLink)
            return True
        except WebDriverException:
            ColorUtils.Print_Colored(ColorUtils.Colors["Red"], "No Internet Connection!")
            return False
    
    
    def locate_element(self, pAttribute: str):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, pAttribute)
        except NoSuchElementException:
            try:
                return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, pAttribute)))
            except TimeoutException:
                raise TimeoutException(f"Element with attribute '{pAttribute}' not found on the page")
    
    def download_video(self, pVideo_link: str, pSave_Path: str) -> None:
        video_valid, video_name = self.is_valid(pVideo_link=pVideo_link)
        if video_valid:
            if exists(join(pSave_Path, video_name)):
                ColorUtils.Print_Colored(ColorUtils.Colors["Green"], "File already exist!")
                
            else:
                ColorUtils.Print_Colored(ColorUtils.Colors["Yellow"], "Searching..")
                                
                download_link = self.get_download_link(pVideo_link=pVideo_link) 
                    
                ColorUtils.Print_Colored(ColorUtils.Colors["Green"], f"Video Found!\nDownloading {video_name}...")
                
                self.download(pDownload_link=download_link, pVideo_name=video_name, pSave_Path=pSave_Path)
        else:
            ColorUtils.Print_Colored(ColorUtils.Colors["Red"], "Not a Valid Link!")
            
    def is_valid(self, pVideo_link: str) -> tuple[bool, str]:
        parts = pVideo_link.split('/')
        return (True, self.get_name(pParts=parts)) if "rule34video.com" in parts and "video" in parts else (False, None)
        
    def get_name(self, pParts: list) -> str:
        return pParts[:-1] if not pParts[-1] == "" else pParts[-2] + ".mp4"
        
    def download(self, pDownload_link: str, pVideo_name: str, pSave_Path: str) -> bool:

        try:
            response = requests.get(pDownload_link, stream=True)
            if response.status_code == 200:
                
                video_size = int(response.headers.get('content-length', 0))
                
                ColorUtils.Set_Color(ColorUtils.Colors["Blue"])
                progress_bar = tqdm(total=video_size, unit="B", unit_scale=True, desc="Downloading")
                
                with open(join(pSave_Path, pVideo_name), "wb") as file:
                    for chunk in response.iter_content(chunk_size=max(int(video_size * 0.01), 1024)):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))
                    
                    progress_bar.close()
                    ColorUtils.Reset_Color()
                    
                    ColorUtils.Print_Colored(ColorUtils.Colors["Green"], "Download Complete!")

                    if settings.Notify_Sound:
                        MessageBeep(MB_ICONASTERISK)

            else:
                ColorUtils.Print_Colored(ColorUtils.Colors["Red"], f"Failed to download: HTTP status code {response.status_code}")
        except requests.RequestException as e:
            ColorUtils.Print_Colored(ColorUtils.Colors["Red"], f"Download failed: {e}")
        
    def close_driver(self):
        if not self.driver == None:
            self.driver.quit()
            self.driver = None