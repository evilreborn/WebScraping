import requests
import lxml.html as lh
import pandas as pd

url='http://WebUrl_From_which_you_want_to_scrap_table_data.com'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#Save the content of website under the variable doc
doc = lh.fromstring(page.content)

#Since the table data is tored row by row
#Parse each row separated by /tr tag
tr_elements = doc.xpath('//tr')

#To check each table row has same lenth or not
val=[len(T) for T in tr_elements[:12]]
print(val)
val=val[0]

#Create empty list
col=[]
i=0

#To save Header row (i.e. Titles of each column)
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print("{}:{}".format(i,name))
    col.append((name,[]))

#First row is header, Data is from 2nd row
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size val, the //tr data is not from our table 
    if len(T)!=val:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1
val=[len(C) for (title,C) in col]
print(val)

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

#To print the first 5 rows of the collected data
df.head()

'''
here i am saving data in csv format
save data in your desired format
eg. df.df.to_json('Filename.json')
'''
df.to_csv('Filename.csv')
