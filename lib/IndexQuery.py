import subprocess as sp
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import configparser as cp
import matplotlib.pyplot as plt
import os
import shutil

'''
Created by Arradi Nur Rizal
For Information Retrieval class assignment lab 2
'''

class IndexQuery:
    def __init__(self,
                index_name, 
                corpus_path,
                q_num, 
                q_text,
                assesment_file):
        #get common configs        
        cf = cp.RawConfigParser()   
        configFilePath = r'config/common.txt'
        cf.read(configFilePath)
        cf.get('common-configs', 'class')
        self.config_path = "config"
        self.data_path = cf.get('common-configs', 'data_path')
        self.index_path = cf.get('common-configs', 'index_path')
        self.index_name = index_name
        self.index_full_path = self.index_path + "/" + index_name
        self.index_parameters_config = index_name+"_index_parameters.xml"
        self.index_parameters_path = self.config_path + "/" + self.index_parameters_config
        self.memory_allocation = cf.get('common-configs', 'index_memory')
        self.corpus_path = corpus_path
        self.fileClass = cf.get('common-configs', 'class')
        self.stemmer_name = cf.get('common-configs', 'stemmer')
        self.field_name = cf.get('common-configs', 'field')
        self.query_parameters_path = self.config_path + "/query.xml"
        self.q_num = q_num
        self.q_text = q_text
        self.assesment_file = assesment_file
     
    '''
    Creating Index Parameter XML file
    '''
    def create_index_parameter(self):
        parameters = ET.Element('parameters')

        index = ET.SubElement(parameters, 'index')
        index.text = self.index_path+"/"+self.index_name

        memory = ET.SubElement(parameters, 'memory')
        memory.text = self.memory_allocation

        corpus = ET.SubElement(parameters, 'corpus')
        path = ET.SubElement(corpus, 'path')
        path.text = self.corpus_path
        file_class = ET.SubElement(corpus, 'class')
        file_class.text = self.fileClass

        stemmer = ET.SubElement(parameters, 'stemmer')
        name = ET.SubElement(stemmer, 'name')
        name.text = self.stemmer_name

        field = ET.SubElement(parameters, 'field')
        name = ET.SubElement(field, 'name')
        name.text = self.field_name

        xmlstr = minidom.parseString(ET.tostring(parameters, 'utf-8')).toprettyxml(indent="   ")[23:]

        with open(self.index_parameters_path, "w") as f:
            f.write(xmlstr)

    '''
    Creating query XML file
    '''
    def create_query(self):
        parameters = ET.Element('parameters')

        query = ET.SubElement(parameters, 'query')
        query_number = ET.SubElement(query, 'number')
        query_number.text = self.q_num
        query_text = ET.SubElement(query, 'text')
        query_text.text = self.q_text

        xmlstr = minidom.parseString(ET.tostring(parameters, 'utf-8')).toprettyxml(indent="   ")[23:]

        with open(self.query_parameters_path, "w") as f:
            f.write(xmlstr)
    
    '''
    Add Index
    '''
    def add_index(self, index_name, corpus_path):
        self.index_name = index_name
        self.index_full_path = self.index_path + "/" + index_name
        self.index_parameters_config = index_name+"_index_parameters.xml"
        self.index_parameters_path = self.config_path + "/" + self.index_parameters_config
        self.corpus_path = corpus_path
        self.create_index_parameter()
        self.build_index()
    
    '''
    Remove Index
    '''
    def remove_index(self, index_name):
        shutil.rmtree(os.path.join(self.index_path, self.index_name))
        os.remove(os.path.join(self.config_path, index_name+"_index_parameters.xml"))

    '''
    Building Index
    '''
    def build_index(self):
        sp.call(["IndriBuildIndex", self.index_parameters_path])
    
    '''
    List Index
    '''
    def list_index(self):
        for item in os.listdir(self.index_path):
            if os.path.isdir(os.path.join(self.index_path, item)):
                print(item)
    
    '''
    Switch Index
    '''
    def switch_index(self, index_name):
        #check index exist
        if os.path.isdir(os.path.join(self.index_path, index_name)):
            self.index_name = index_name
            self.index_full_path = self.index_path + "/" + index_name
            self.index_parameters_config = index_name+"_index_parameters.xml"
            self.index_parameters_path = self.config_path + "/" + self.index_parameters_config
        else:
            print("index does not exist")
    
    '''
    Switch Query Number
    '''
    def switch_query_number(self, query_number):
        self.q_num = query_number

    '''
    Switch Assesment File
    '''
    def switch_assesment_file(self, assesment_file_path):
        if os.path.exists(assesment_file_path):
            self.assesment_file = assesment_file_path
        else:
            print("the path/file you enter does not exist/reachable")
    
    '''
    Apply Query
    '''
    def apply_query(self, query_text):
        self.q_text = query_text
    
    '''
    Run Query
    '''
    def run_query(self):
        sp.call(["IndriRunQuery -trecFormat=true -index=" + self.index_full_path + " " + self.query_parameters_path + " > " + self.data_path + "/my_run1_rankings.trec"], shell=True)
    
    '''
    Evaluate Query Result
    '''
    def evaluate_query_result(self):
        output = sp.check_output(["trec_eval -q -m iprec_at_recall " + self.assesment_file + " " + self.data_path + "/my_run1_rankings.trec | awk '{print $3 }'"], shell=True).decode('UTF-8').splitlines()
        self.create_precision_recall_graph(output[:11])
    
    '''
    Show index_parameters.xml
    '''
    def show_index_parameters(self):
        sp.call(["cat", self.index_parameters_path])
    
    '''
    Show query_parameters.xml
    '''
    def show_query_parameters(self):
        sp.call(["cat", self.query_parameters_path])
    
    '''
    Create Precision Recall graph
    '''
    def create_precision_recall_graph(self, iprec_at_recall):
        # x axis values (Recall)
        x = [0,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00] 
        # corresponding y axis values (Precision)
        y = iprec_at_recall 
        
        # plotting the points  
        plt.plot(x, y)
        plt.gca().invert_yaxis()
        plt.xlabel('Recall') 
        plt.ylabel('Precision') 
        plt.title('Precision Recall graph') 
        plt.show() 

