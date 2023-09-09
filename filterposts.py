'''
Playing around with confesh data
10/06/22
'''

# Import statements
from pathlib import Path
from datetime import datetime
import pandas as pd
import os
from collections import Counter

def makecsv(mfold, datestr):
    if (not os.path.exists(f'{mfold}/top_words_{datestr}.tiff')):
        print(f'{mfold}/top_words_{datestr}.tiff')
        # read csv
        date_df = pd.read_csv(f'{mfold}/Confesh_{datestr}.csv')
        
        # get the post with the most comments for each unique post
        posts_dic = date_df.sort_values('Comments', ascending=False).drop_duplicates(['Post']).set_index('Index')
        
        # drop data and N/a
        posts_dic = posts_dic.drop(columns=['Date'])
        posts_dic = posts_dic.drop(posts_dic[posts_dic.Comments == 'N/a'].index)
        
        # out with the old
        os.remove(f'{mfold}/Confesh_posts_{datestr}.csv')
        
        # save as new csv
        posts_dic.to_csv(f'{mfold}/Confesh_posts_{datestr}.csv')
        
        os.system(f'Rscript word_cloud_noactorsent.R Confesh_posts_{datestr}.csv fold_{datestr} {datestr}')
    
    else:
        pass

def makeweekcsv(mfold, datestr_list):
    if (os.path.exists(mfold) == False):
        os.mkdir(mfold)
        
        date_df_list = datestr_list.copy()
        for i in range(len(datestr_list)):
            print(datestr_list[i])
            date_df_list[i] = f'fold_{datestr_list[i]}/Confesh_posts_{datestr_list[i]}.csv'
        
        # get the post with the most comments for each unique post
        df = pd.concat(map(pd.read_csv, date_df_list), ignore_index=True)
        df = df.sort_values('Comments', ascending=False).drop_duplicates(['Post'])
        df = df.drop(columns=['Index'])
        #df = df.sort_values(by=['Comments'], ascending = False)
        # save as new csv
        df.to_csv(f'{mfold}/Confesh_posts_{mfold}.csv')
        
    #call analysis
    #os.system(f'Rscript word_cloud_noactorsent.R Confesh_posts_{mfold}.csv {mfold} {mfold}')
    #os.system(f'Rscript word_cloud_noactorsent.R Confesh_posts_{mfold}.csv {mfold} {mfold}')
    os.system(f'Rscript sentiment_analysis.R Confesh_posts_{mfold}.csv {mfold} {mfold}')
def makemastercsv():
    if (os.path.exists('master') == False):
        os.mkdir('master')
        
    date_list = [fold[fold.index('_')+1:] for fold in os.listdir(os.getcwd()) if fold.startswith('fold_')]
    date_df_list = date_list.copy()
    
    for i in range(len(date_list)):
        print(date_list[i])
        date_df_list[i] = f'fold_{date_list[i]}/Confesh_posts_{date_list[i]}.csv'
    
    # get the post with the most comments for each unique post
    df = pd.concat(map(pd.read_csv, date_df_list), ignore_index=True)
    df = df.sort_values('Comments', ascending=False).drop_duplicates(['Post'])
    df = df.drop(columns=['Index'])
    #df = df.sort_values(by=['Comments'], ascending = False)
    # save as new csv
    df.to_csv(f'master/Confesh_posts_master.csv')
        
    #call analysis
    os.system(f'Rscript sentiment_analysis.R Confesh_posts_master.csv master master')
    

    
def main():
    ''' Set-up'''
    
    #'''
    for folname in os.listdir(os.getcwd()):
        if folname.startswith('fold_'):
            datestr = folname[folname.index('_')+1:]
            makecsv(folname, datestr)
            
    '''
    makeweekcsv('Week1sa', ['10-24-2022', '10-25-2022', '10-26-2022', '10-27-2022', '10-28-2022', '10-29-2022', '10-30-2022'])
    makeweekcsv('Week2sa', ['10-31-2022', '11-01-2022', '11-02-2022', '11-03-2022', '11-04-2022', '11-05-2022', '11-06-2022'])
    makeweekcsv('Week3sa', ['11-07-2022', '11-08-2022', '11-09-2022', '11-10-2022', '11-11-2022', '11-12-2022', '11-13-2022'])
    makeweekcsv('Week4sa', ['11-14-2022', '11-15-2022', '11-16-2022', '11-17-2022', '11-18-2022', '11-19-2022', '11-20-2022'])
    makeweekcsv('Week5sa', ['11-21-2022', '11-22-2022', '11-23-2022', '11-24-2022', '11-25-2022', '11-26-2022', '11-27-2022'])
    
        '''
    makeweekcsv('Week6sa', ['11-28-2022', '11-29-2022', '11-30-2022', '12-01-2022', '12-02-2022', '12-03-2022', '12-04-2022'])
    
    #makeweekcsv('Week7sa', ['12-05-2022', '12-06-2022', '12-07-2022', '12-08-2022', '12-09-2022', '12-10-2022', '12-11-2022'])
    
    makemastercsv()
            
        
        

main()


