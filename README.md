Created by Arradi Nur Rizal --
For Information Retrieval class -- assignment lab 2

**Only tested in Debian Linux with python 3.6**

**Note:** There are not a lot of guard code, so better check the spelling when entering the command

**KnownBug:** if you removeIndex after restarting the program, sometime the index folder is deleted. you need to create new index folder manually before adding new Index. 

Make sure the following python modules for python 3.6 are available
1. xml (ussually already exist with python 3.6)
2. configparser (sudo pip3 install matplotlib)
3. subprocess (ussually already exist with python 3.6)
4. matplotlib (sudo pip3 install matplotlib)
5. cmd (ussually already exist with python 3.6)
6. shutil (ussually already exist with python 3.6)
7. os (ussually already exist with python 3.6)

Make sure you have the following program install. Check with "which" in command prompt
1. IndriBuildIndex
2. IndriRunQuery
3. trec_eval (https://github.com/usnistgov/trec_eval)
