import requests
from lxml import etree


def getPaperTitle(name):
    url="http://xueshu.baidu.com/s?wd="+name
    s = requests.Session()
    r = s.get(url)
    tree=etree.HTML(r.content)
    nodes = tree.xpath('''//*[@id="1"]/div[1]/h3/a''')
    if(nodes!=[]):
        return nodes[0].text
    else:
        return ""
    
    
    
    
file="2017-10-26.log"
with open(file) as f:
    for line in f.readlines():
        try:
            #print(line)
            tmp=line[1:-3].split(",Some(")
            if(len(tmp)<2): continue
            name=tmp[1].replace("\"","\\\"")
            if(name.find("paperuri")!=-1):
                name=getPaperTitle(name)
            value=tmp[0]
            if(value!=0 and name!=""):
                print("{name:\""+name+"\",value:"+tmp[0]+"},")
        except :
            #print("have a error")
            pass`
        
            

        
        