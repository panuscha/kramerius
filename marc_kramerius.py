import pandas as pd
from pymarc import map_xml
path = "nkc.xml.gz"
# open the file
# with open(path, 'r', encoding="utf8") as f:
#     data = f.read()

# Bs_data = BeautifulSoup(data, "xml")
# print(Bs_data)
results = {'title':[], 'author':[], 'year published': [], 'literary form':[], '080 $a':[], '041 $a':[], '041 $h':[], '655 $a':[] }
types = ['román', 'novel', 'povídk']


def do_it(r):
    found = False
    for line in r.get_fields('856'): 
        try:
            digitalized = ('Digitalizovaný dokument' in line['y'])
            if digitalized:
                for t in r.get_fields('655'):
                    if '$'+'a' in str(t):    
                        for i in types:
                            if i in t['a']:
                                        found = True 
                                        if r.title is not None: 
                                            results['title'].append(r.title)
                                        else:
                                            results['title'].append(' ')



                                        if r.author is not None: 
                                            results['author'].append(r.author)
                                        else:
                                            results['author'].append(' ')  


        
                                        
                                        if [] != r.get_fields('008') : #is not None
                                            for y in r.get_fields('008'):
                                                results['year published'].append(y.data[7:11])
                                                results['literary form'].append(y.data[33])
                                                
                                        else:
                                            results['year published'].append(' ')
                                            results['literary form'].append(' ') 

                                        


                                        
                                        if  [] != r.get_fields('080') : #is not None
                                            code_080 = []
                                            for k in r.get_fields('080'):  
                                                if '$'+'a' in str(k):
                                                    code_080.append(k['a'])   
                                                else:
                                                    code_080.append(" ") 
                                            results['080 $a'].append("§".join(code_080))           
                                        else:
                                            results['080 $a'].append(' ')  


                                        if [] != r.get_fields('655') : #is not None
                                            code_655 = []
                                            for k in r.get_fields('655'):  
                                                if '$'+'a' in str(k):
                                                    code_655.append(k['a'])   
                                                else:
                                                    code_655.append(" ") 
                                            results['655 $a'].append("§".join(code_655))           
                                        else:
                                            results['655 $a'].append(' ')  



                                        if [] !=  r.get_fields('041'):#is not None
                                            for k in r.get_fields('041'): 
                                                if '$'+'a' in str(k):
                                                    results['041 $a'].append(k['a'])
                                                else:    
                                                    results['041 $a'].append(' ')

                                                if '$'+'h' in str(k):
                                                    results['041 $h'].append(k['h'])
                                                else:       
                                                    results['041 $h'].append(' ')
                                                break    
                                        else:
                                            results['041 $a'].append(' ')  
                                            results['041 $h'].append(' ')
                                        break
                    if found :
                        break                   
            if found :
                break                                      
        except:
            continue 
        break           

map_xml(do_it, path)

df = pd.DataFrame.from_dict(results, orient='index').T.to_excel('kramerius_novels_stories.xlsx')   