from lib.IndexQuery import IndexQuery
from cmd import Cmd
import shutil
import os

'''
Created by Arradi Nur Rizal
For Information Retrieval class assignment lab 2
'''

class IndexQueryPrompt(Cmd):
    prompt = 'cmd>> '
 
    def preloop(self):
        super(IndexQueryPrompt,self).preloop()
        if shutil.which("IndriBuildIndex") and shutil.which("IndriRunQuery") and shutil.which("trec_eval"):
            self.IQ = IndexQuery("", "", "","","") 
            print("Type ? to list commands")
        else:
            print("WARNING!! You need to install trec_eval and/or Indri first, type 'exit' to continue ")
            

    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
 
    def do_index(self, inp):
        ai = IndexPrompt(self.IQ)
        ai.prompt = self.prompt[:-3]+':Index>>'
        ai.cmdloop()
    
    def do_addIndex(self, inp):
        i = inp.split()
        self.IQ.add_index(i[0],i[1])

    def do_query(self, inp):
        q = QueryPrompt(self.IQ)
        q.prompt = self.prompt[:-3]+':Query>>'
        q.cmdloop()

    def do_listIndex(self, inp):
        self.IQ.list_index()

    def do_removeIndex(self, inp):
        self.IQ.remove_index(inp)

    def help_removeIndex(self):
        print('remove index. I.e: removeIndex index-name')

    def help_addIndex(self):
        print("Add new index. I.e: addIndex index-name corpus-path")
    
    def help_index(self):
        print("information and command to available index.")

    def help_query(self):
        print("Make Query to index.")
 
    def help_listIndex(self):
        print('list index')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))
 
    do_EOF = do_exit
    help_EOF = help_exit

class IndexPrompt(Cmd):
    def __init__(self, IQ):
        super(IndexPrompt, self).__init__()
        self.IQ = IQ
    
    def do_exit(self, inp):
        return True

    def help_exit(self):
        print('go back to main menu')
 
    def do_list(self, inp):
        self.IQ.list_index()

    def help_list(self):
        print('list index')

    def default(self, inp):
        print('please use the command. Type ? to list commands')
    
    # add new index
    def do_add(self, inp):
        i = inp.split()
        self.IQ.add_index(i[0],i[1])

    def help_add(self):
        print('add index. I.e: add index-name corpus-path')

    # remove index
    def do_remove(self, inp):
        self.IQ.remove_index(inp)

    def help_remove(self):
        print('remove index. I.e: remove index-name')

    do_EOF = do_exit
    help_EOF = help_exit

class QueryPrompt(Cmd):
    def __init__(self, IQ):
        super(QueryPrompt, self).__init__()
        self.IQ = IQ

    def do_listIndex(self, inp):
        self.IQ.list_index()

    def help_listIndex(self):
        print('list index')

    def do_exit(self, inp):
        return True
    
    def help_exit(self):
        print('go back to main menu')

    # addquery number
    def do_queryNum(self, inp):
        self.IQ.switch_query_number(inp)
    
    def help_queryNum(self):
        print('select query number. i.ex: queryNum query-number')

    # add index choice
    def do_use(self, inp):
        self.prompt[:-3]+':'+inp+'>>'
        self.IQ.switch_index(inp)

    def help_use(self):
        print('select index for query. i.ex: use index-name')

    # add assements file
    def do_selectAssesmentFile(self, inp):
        self.IQ.switch_assesment_file(inp)

    def help_selectAssesmentFile(self):
        print('select Assesment File for evaluation. i.ex: selectAssesmentFile assesment-file-path')

    def default(self, inp):
         
        self.IQ.apply_query(inp)
        
        #check that query number not empty, index not empty, assesment file not empty
        if self.IQ.index_name and self.IQ.q_num and self.IQ.q_text and self.IQ.assesment_file:
            self.IQ.create_query()
            self.IQ.run_query()

            #evaluate
            self.IQ.evaluate_query_result()
        else:
            print("either index is not selected or query number is not entered or assesment file is not entered")

    do_EOF = do_exit
    help_EOF = help_exit
 