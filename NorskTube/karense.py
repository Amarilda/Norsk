import time
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def NorskTube():

    df = pd.read_csv('NorskTube/karense.csv')
    #find the oldest video to watch
    current_index = min(df[df.date_watched.isna() == True].index)

    #load chrome, install add blocker
    path_to_extension = "/Users/Edite/Library/Application Support/Google/Chrome/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.46.2_0"
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)

    # ChromeDriverManager - manage drivers automatically
    # chrome_options - 
    wd = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    wd.create_options()

    # daily dose of 5 videos
    for i in range(current_index, (current_index+5),1):
        url = df.loc[i, 'html']

        # for the first video
        if i == current_index:

            #load video, install Add Block, close Add Block tab, switch to the original tab
            wd.get(url)
            wd.switch_to.window(wd.window_handles[1])
            wd.close()
            wd.switch_to.window(wd.window_handles[0])
            
            #reject it all
            wait = WebDriverWait(wd, 5)
            xxpath = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div/div[6]/div[1]/ytd-button-renderer[1]/a/tp-yt-paper-button"
            wait.until(EC.element_to_be_clickable((By.XPATH, xxpath)))
            wd.find_element_by_xpath(xxpath).click()

        wd.get(url)

        # video statuss: 2 - paused, 1 - playing, 0 - done
        state = 2
        while state != 0:
            state = wd.execute_script("return document.getElementById('movie_player').getPlayerState()")
        
        # when video is done, timestamp date_watched
        df.loc[i,'date_watched'] = datetime.datetime.now()
        df.to_csv('NorskTube/karense.csv', index = False)

    # tidy up when you are done
    wd.quit()


if __name__ == '__main__':
    NorskTube()  