import csv
import os
import json
import uuid 

from elasticsearch import Elasticsearch
from datetime import datetime, date, timezone


import sys, os.path
sys.path.append(os.path.abspath('../esconfig'))
from esconfig import *
import targets

targets = targets.get_list("ROOTDOMAIN")
es = Elasticsearch([{'host': es_host, 'port': 9200}])

class esLog:
    indexName = str()
    i_d = str()
    type_of_doc = str()
    js = str()

    def __init__(self, indexName, type_of_doc, i_d, js):
        self.indexName = indexName
        self.i_d = i_d
        self.type_of_doc = type_of_doc
        self.js = js
        
def sendToES(esllog):
    es.index(index=esllog.indexName, doc_type=esllog.type_of_doc,
             id=esllog.i_d, body=json.loads(esllog.js))
    # print("sent" + i_d)


def main():
    for row in targets:
        os.system('/bin/amass enum -d ' + row["target"] + ' -ip -json /tmp/amassoutput -src')
        
        file1 = open('/tmp/amassoutput', 'r') 
        Lines = file1.readlines() 
        count = 0
    
        for line in Lines: 
           
            el = json.loads(line)
            
            el["timestamp"]= datetime.now(timezone.utc).isoformat() 
            el["network"] = row["network"]
            el["namespace"] = row["namespace"]
            id = uuid.uuid1() 
            es_log = esLog("amassscanresults", 'log', id , json.dumps(el, default=str))
            sendToES(es_log)
           # print(el)

if __name__ == "__main__":
    main()

