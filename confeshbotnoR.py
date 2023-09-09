'''
Playing around with confesh data
10/06/22
'''

# Import statements
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os
from collections import Counter
 

def main():
    ''' Set-up'''
    # Set up chrome driver
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # to open the url in the browser, wait to try and avoid unloaded pages
    driver.get('https://smith.confesh.com/?key=aafa9ca6b3a77702385de9c13d70265b')
    time.sleep(10)
    
    ''' Variables I want to reset every start'''
    # Dictionary to check what's a new post/comment
    newdic = {}
    # Counters
    newposts = 0
    newcomments = 0
    # Prevents first round counts from fucking up my data ***
    firstround = True
                    
    
    ''' Data collection loop '''
    # Infinite Loop
    while(True):
        ''' Variables I want to reset every <time interval> '''
        # this is just to get the time at the time of web scraping
        now = datetime.now()
                
        if ('date' in locals()):
            if (date != now.strftime("%m-%d-%Y")):
                # Makes daily folder if it doesn't exist for graphs and stuff
                if not (os.path.exists(f'fold_{date}')):
                    os.mkdir(f'fold_{date}')
                
                # Makes a daily unbiased text log for word analysis ***
                if not (os.path.exists(f'fold_{date}/Confesh_posts_{date}.csv')):
                    df = pd.DataFrame.from_dict(newdic, orient="index")
                    df.to_csv(f'fold_{date}/Confesh_posts_{date}.csv')
                    
                # move csv
                os.rename(f'Confesh_{date}.csv', f'fold_{date}/Confesh_{date}.csv')
                # make plot
                os.system(f'Rscript word_cloud_noactorsent.R Confesh_posts_{date}.csv fold_{date} {date}')
                # resets daily dictionary
                newdic = {}
            
        current_time = now.strftime("%H:%M:%S")
        date = now.strftime("%m-%d-%Y")
        
        # Dictionary that gets turned into spreadsheet
        post_outer = {}
         
        # Makes daily cache file if it doesn't exist for post archives
        if not (os.path.exists(f'Confesh_{date}.csv')):
            with open(f'Confesh_{date}.csv', 'w+') as cache:
                cache.write('Index,Post,Comments,Date\n')
       
                
        # Makes activity log csv if i delete it (should not change daily)
        if not (os.path.exists(f'activity_times.csv')):
            with open(f'activity_times.csv', 'w+') as log:
                log.write('Date,Time,NewPosts,NewComments\n')
        
        ''' Data collection '''
        # Exception handling to handle unexpected changes
        try:
            # puts in check so the loop stops at end of page (15 posts)
            esc = 16
            check = 0
            # resets counter every <time interval>
            newposts = 0
            newcomments = 0
            
            # get content
            content = driver.page_source
            soup = BeautifulSoup(content, "lxml")
            
            ''' Post by post loop '''
            # gathers data on every post contatiner
            for a in soup.findAll('ul', attrs={'class':'secret-container'}):
                # pulls post content and number of comments
                name = a.find('div', attrs={'class':'confession'})
                comment = a.find('span')
                 
                ''' Checks how many new comments/posts there are (is it new?) '''
                # if we've seen the post today
                if name.text in newdic.keys():
                    # pulls how many comments there were last time seen
                    oldcom = newdic[name.text]
                    # if there are more comments now, updates dictionary and comment count
                    if ((int(comment.string) - int(oldcom)) > 0):
                        newdic.update({ name.text : comment.string})
                        newcomments += (int(comment.string) - int(oldcom))
                              
                # if we haven't seen the post today
                else:
                    # if it is the first round of the day, all posts will be new. if it isn't, changes are recorded
                    if (firstround == False):
                        newcomments += int(comment.string)
                        newposts += 1
                    # updates the dictionary with the comment and its count
                    newdic.update({name.text : comment.string})
                     
                # updates dataframe dictionary (only 15 posts) ???
                post_outer.update({name.text : int(comment.string)})
                
                ''' Completion check '''
                # checks if we are done with page (cycled through 15 top posts)
                check += 1
                if (check == esc - 1):
                    #firstround = False
                    break
        # Keeps going if weirdness
        except:
            continue
        
        ''' Saved information '''
        if (newcomments > 0 or newposts > 0 or firstround == True):
            # Makes dataframe from dictionary
            df = pd.DataFrame(list(post_outer.items()), columns=['Post', 'Comments'])
            # Adds time to the dataframe
            df[2] = pd.Series([current_time for x in range(len(df.index))], dtype = 'string')
            # Adds it into a csv for the day
            df.to_csv(f'Confesh_{date}.csv', mode='a', header=False)
            
            # Also records how many changes were made
            with open("activity_times.csv", 'a') as act:
                act.write(f'{date},{current_time},{newposts},{newcomments}\n')
                
        else:
            with open(f'Confesh_{date}.csv', mode='a') as content:
                content.write(f'-1,No new posts,N/a,{current_time}\n')
            with open("activity_times.csv", 'a') as act:
                act.write(f'{date},{current_time},{newposts},{newcomments}\n')
                
        
        # Terminal checker
        print(f'At time: {current_time} IST')
        firstround = False
        
        
        ''' <Time interval> '''
        # Controls the interval in which data is collected (in seconds)
        #30 min = 1800
        # 1740
        time.sleep(1740)
        driver.refresh()
        time.sleep(60)
        
        

main()


