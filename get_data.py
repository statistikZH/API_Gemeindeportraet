### Description of script
#All publicly available data (Open Government Data – OGD) of the Statistical Office of the Canton of Zurich
#are extracted from the central JSON-file. By downloading and opening up every file, additional data can be
#extracted such as variable names that are not described in the metadata. Extracted is thus a combination
#between metadata and some information in the dataset.

# thoughts for improvement
# - much more metadata could be extracted
# - This could later be improved to save the data in a mysql-db.



import pandas as pd
import json
from urllib.request import urlopen
import csv
import wget
import os
import io

#import the central json file
url="https://www.web.statistik.zh.ch/data/zhweb.json"
json_url = urlopen(url)
data = json.load(json_url)
list_data=[]
for i,entry in enumerate(data['dataset']):
    #get for every dataset the urlname that is written in the respective node
    try:
        urlname=entry['distribution'][0]['downloadUrl']
    except:
        print("exception ocurred: no downloadurl in exected format")
        continue
    if urlname is not None:
        #select only the csv files, as there are also other kind of files
        if urlname[-4:]==".csv":
            filename='data/'+str(i)+'.csv'
            if os.path.exists(filename):
                os.remove(filename) # if exist, remove it directly
            try:
                wget.download(urlname,filename )
            except:
                print(i,"Download failed")
            mydelimiter=None

            #there was an issue with the encoding of the files, this is why latin-1 is used
            with io.open(filename, 'r', encoding="latin-1") as csvfile:
                #also we need an own csv-sniffer to well observe whether the file is ,-delimited or ;-delimited - both are currently used
                dialect = csv.Sniffer().sniff(csvfile.readline(), [',',';'])
                csvfile.seek(0)
                mydelimiter=dialect.delimiter
            try:
                file_in=pd.read_csv(filename,dialect.delimiter)
                if 'INDIKATOR_ID' not in file_in.columns:
                    print("this is not a gp file")
                    continue
                
                list_data.append([ urlname,entry['identifier'],entry['title'],entry['description'],file_in.THEMA_NAME.iloc[0],file_in.SET_NAME.iloc[0],file_in.SUBSET_NAME.iloc[0],file_in.EINHEIT_KURZ.iloc[0],file_in.EINHEIT_LANG.iloc[0]])
            except:
                print(i,"file could not be loaded")

    print(i)
    
    

#and the file with all the relevant metadata is saved here
df = pd.DataFrame(list_data, columns=['url','identifier','dataset_title','description','thema_name','set_name','subset_name','einheit_kurz','einheit_lang'])
df.to_csv('output/gp_overview.csv',index=False)
print("FINISHED")
