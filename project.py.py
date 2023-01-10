#!/usr/bin/env python
# coding: utf-8

# # Libraries

# In[147]:


# Task 1:
import sys
import isort
import platform
# Task 2:
import importlib

# Task 4:
import os
import os.path

# Task 6:
import networkx as nx
import matplotlib.pyplot as plt


# # Task 1: Collect names of the StdLib modules and packages

# In[148]:


def get_stdlib_packages():
    """
    Function requires no arguments
    
    Function Description:
    
    1. Determines the minor version of Python
    
    2. Chooses the right way to import the correct package (isort for versions 5-9), sys otherwise
    
    3. Returns the names of external packages
    
    ** Exludes packages "this" and "antigravity"
    """
    minor_version = sys.version_info.minor # extract python's version minor through sys

    # creating a dictionary for 3.5-3.9 minor versions 
    version_dict = {5:list(isort.stdlibs.py35.stdlib),
                    6:list(isort.stdlibs.py36.stdlib),
                    7:list(isort.stdlibs.py37.stdlib),
                    8:list(isort.stdlibs.py38.stdlib),
                    9:list(isort.stdlibs.py39.stdlib)}
    
    for key,value in version_dict.items(): 
        value.sort(reverse=False)
        for pkg in value:
            if pkg.startswith("_"): # remove internal libraries
                value.remove(pkg)
            if pkg =="this" or pkg =="antigravity": # remove `this` and `antigravity` 
                value.remove(pkg)

        if minor_version == key: # for minor versions 3.5-3.9
            return value
        elif minor_version >=10:
            return sys.stdlib_module_names # for minor versions 3.10 and above
        else:
            pass
    
    
            


# In[149]:


def task1():
    """
    Function Description:
    
    Creates print statement about the standard libraries that are contained in your Python version 
    Prints the first and last five packages of the packages sorted in alphabetical order
    """
    print(f"Python {sys.version} on {platform.platform()} \n StdLib contains {len(get_stdlib_packages())} external modules and packages:")
    print(f"{get_stdlib_packages()[0:5]} ... {get_stdlib_packages()[-5:]}")


# In[150]:


task1()


# # Task 2: Find what's in each file's namespace
# 

# In[151]:


def get_real(package_names):
    """
    Parameter:
    1. package_names: a sequence of package names
    
    Function Description:
    
    get_real is a function that takes in parameter package_names
    
    1. Iterates through the sequence of names
    
    2. Determines which ones represent the module name that cannot
        be imported (will be exluded)
        
    3. Returns a **list** of names importable StdLib packages
    
    """
    importable_packages = []
    minor_version = sys.version_info.minor

    version_dict = {5:list(isort.stdlibs.py35.stdlib),
                    6:list(isort.stdlibs.py36.stdlib),
                    7:list(isort.stdlibs.py37.stdlib),
                    8:list(isort.stdlibs.py38.stdlib),
                    9:list(isort.stdlibs.py39.stdlib)}
    
    for key,value in version_dict.items():            
        for pkg in value:
            if pkg.startswith("_"):
                value.remove(pkg)
            elif pkg =="this" or pkg =="antigravity":
                value.remove(pkg)
            

        if minor_version == key:
            package_names == value

    # code for importing a module
    for package in package_names:
        try: 
            importlib.import_module(package)
            importable_packages.append(package)
        except:
            pass
    return importable_packages


# In[152]:


def task2():
    """
    Function Description
    
    Creates a print statement of all the packages that are not supported by the system
    I.e., the packages are not importable
    
    """
    not_importable =[]
    for i in get_stdlib_packages():
        if i not in get_real(get_stdlib_packages()):
            not_importable.append(i)
    print(f"These StdLib packages are not importable on Python{platform.platform()} {not_importable}")
    


# In[ ]:


task2()


# # Task 3: Calculate the linking / dependency between the StdLib modules

# In[153]:


def module_dependency(module_names,name):
    """
    Parameters:
    1. module_names: a list of module_names (from Task 2)
    
    2. name: a module name among the list of module_names
    
    
    Function Description:
    
    module_dependency is a function that takes input parameters
    `module_names` and `name
    
    1. Returns the list of names on which the a_module depends on
    
    2. If a_module does not depend on any other module, the function
        will return an empty list
    """
    name = str(name)
#     namespace = vars(importlib.import_module(name)).keys()
    dependencies = []
    try:
        for n in module_names:
            for n in vars(importlib.import_module(name)):
                if n in module_names:
                # if the 'name' input parameter is in the imported list of modules:
                # append the module name to `a_module`
                    dependencies.append(n)

                else:
                    dependencies = dependencies
    except:
        pass
    return dependencies

    


# In[154]:



def task3():
    """
    Function Description:
    
    -2 nested functions:
    
    1. five_most_dependent(): Returns the 5 package names with the most number of dependencies in descending order
                              with its number of dependencies 
    2. core_modules(): Returns the name of all core_modules with no dependencies
    """
    def five_most_dependent():
        all_dependencies=[]


        module_names = get_real(get_stdlib_packages())
        for m in module_names:
            all_dependencies.append((m,len(module_dependency(module_names,m))))
            all_dependencies.sort(key= lambda t: t[1],reverse=True)
            top_five = [dep for dep in all_dependencies[0:5]]


        print(f"These following StdLibs are in top five most dependent:\n {top_five}\n In the format of (package name, number of dependencies) \n")

        
    def core_modules():
        all_dependencies =[]
        module_names = get_real(get_stdlib_packages())
        for m in module_names:

            all_dependencies.append((m,module_dependency(module_names,m)))
            core = [item[0] for item in all_dependencies if len(item[1])==0]

        print(f" These are core modules with no dependencies:{core} \n")
        print(f"The total number of not importable modules is {len(core)}")

    (five_most_dependent(), core_modules())


# In[155]:


task3()


# # Task 4: Explore the code of Python’s written modules

# In[156]:


def explore_package(a_package:str):
    """
        
    Parameters:
    a_package: a package name in type string
    
    Function Description:
    
    1. Checks that `a_package` is one of the importable standard library files
    
    2. Filters OUT files that don't contain '__path__' nor '__file__'
    
    3. Returns a tuple of values: 
    (Total number of lines in all Python files of a_package,
    Total number of custom types a_package defines)
        
    """
    total_length = 0 # counter for total length of all python code files
    num_class = 0 # counter for number of classes within each python code file
    
    #1. check if package is one of importable packages
    if a_package in get_real(get_stdlib_packages()):
    
        #2. check if namespace has __file__ or __path__ attributes
        #   some packages have both __path__ and __file__, thus we check __path__ first
        
        if '__path__' in vars(importlib.import_module(a_package)):
            # use os.walk to traverse the package directory and open the files within 
            # the 0th element of the __path__ attribute of a package provides the path directory
            for root, dirs, files in os.walk(vars(importlib.import_module(a_package))['__path__'][0]):
            
                for f in files:
                    if f.endswith('.py'): # only want the python code files
                        with open(root+'/'+f,"r", encoding = "ISO-8859-1") as fi:
                            content = fi.readlines() # returns a list of lines inside python code file
                            for i in content:
                                i = i.strip() # remove all empty spaces and \n
                                
                                if i.startswith('class') or i.startswith("__"): 
                                # self-defined classes at the beginning of the line only
                                    num_class +=1
                                    total_length+= 1
                        
                    else:
                        pass
            return(total_length,num_class)
                    
                  
                        
      # a module is one file with no inner files, thus we don't need os.walk
        elif '__file__' in vars(importlib.import_module(a_package)):             
            filename=importlib.import_module(a_package).__file__
            
          # a module's __file__ attribute provides the path to a file__init__.py inside the directory

            if filename.endswith('.py'): # only want the python code files

                with open(filename,"r",encoding = "ISO-8859-1") as f:
                    content = f.readlines() # returns a list of lines inside python code file
                    for i in content:
                        i = i.strip() # remove all empty spaces and \n
                        
                        if i.startswith('class') or i.startswith("__"): # count class instances 
                            # self-defined classes at the beginning of the line only
                            num_class += 1 
                return (len(content),num_class)
           

        else:
            pass


# In[157]:


def task4():
    """
    Function description:
    - 4 nested functions:
    
    1. five_largest_packages_loc(): Returns 5 package names with the top line of counts (LOC) within 
                                    its python-coded files and its line count

    2. five_smallest_packages_loc(): Returns 5 package names with the smallest line of counts (LOC) within
                                     its python-coded files and its line count
    3. five_largest_packages_classes(): Returns the 5 package names with the top number of self-defined 
                                        classes within python code and the number of classes
                                        
    4. no_custom_classes()L Returns all package names with no self-defined classes within python code
    
    """
    def five_largest_packages_loc():
            packages_loc = []
            for i in get_real(get_stdlib_packages()):
                try:
                    packages_loc.append((i,explore_package(i)[0]))
                    packages_loc.sort(key=lambda t: t[1],reverse=True)
                except TypeError:
                    pass
            print(f"{packages_loc[0:5]} \n have the largest Line of Counts \n")
    def five_smallest_packages_loc():
        # results with `0` are packages with no __file__ or __path__ --> what to return?
        packages_loc = []
        for i in get_real(get_stdlib_packages()):
            try:
                packages_loc.append((i,explore_package(i)[0]))
                packages_loc.sort(key=lambda t: t[1],reverse=False)
            except TypeError:
                pass
        print(f"{packages_loc[0:5]} \n have the smallest Line of Counts \n")

        return packages_loc[0:5]
    def five_largest_packages_classes():
        packages_classes = []
        for i in get_real(get_stdlib_packages()):
            try:
                packages_classes.append((i,explore_package(i)[1]))
                packages_classes.sort(key=lambda t: t[1],reverse=True)
            except TypeError:
                pass
        print(f"{packages_classes[0:5]} \n have the largest number of defined Classes \n")
    def no_custom_classes():
        packages_noclass = []
        for i in get_real(get_stdlib_packages()):
            try:
                if explore_package(i)[1] ==0:
                    packages_noclass.append(i)
            except TypeError:
                    pass
        print(f"These packages have no self-defined classes {packages_noclass}")
    print(five_largest_packages_loc(), five_smallest_packages_loc(), five_largest_packages_classes(), no_custom_classes())  


# In[158]:


task4()


# # Task 5: Cyclic module dependencies: Are there any in StdLib?

# In[163]:


def find_cycles():
    """
    Function Description: 
    
    Computes all cyclic dependencies using dfs(mod_names, name, dep_list, cycle_list, valid) as 
    a helper function 
    
    Returns a lists of packages that have cyclic dependencies


    """
    circular_dependencies = []  # list of cyclic dependencies
    distinct = []  # list to keep track of dependencies and prevent redundancies
    packages = get_stdlib_packages()
    real = get_real(packages)
    lens = len(real)
    for i in range(lens):
        module = real[i]
        if module in distinct:
            continue
        distinct.append(module)
        dependencies = [module]
        circular = dfs(dependencies, distinct, real, module, circular=[])
        circular_dependencies.extend(circular)
    return circular_dependencies


def dfs(dependencies, distinct, real, module, circular=[]):
    """
    Function Description:
    
    the function uses the concept of depth-first-search to traverse through the 
    graph created by the task3 function, module_dependency()
    
    Parameterse:
    1. mod_names: a list of module_names (importable standard libraries from task2)
    
    2. dep_list: a list of dependencies found by module_dependency function in task3
    
    3. cycle_list: a list that contains packages with cyclic dependencies (i.e. a-> packages -> also dependent on a)
    
    4. valid: a list to keep track of dependencies to prevent redundancies
    """
    next_deps = module_dependency(real, module)
    if not next_deps:
        return []
    else:
        lens = len(next_deps)
        for i in range(lens):
            next_module = next_deps[i]
            if next_module != dependencies[-1] and next_module in dependencies:
                cycle = dependencies[dependencies.index(next_module):]
                cycle.append(next_module)
                circular.append(cycle)
                continue
            if next_module in distinct:
                continue
            else:
                distinct.append(next_module)
                dependencies.append(next_module)
                dfs(dependencies, distinct, real, next_module, circular=circular)
                dependencies.remove(next_module)
    return circular


# In[164]:



def task5():
    """
    Function Description:
    
    Uses the find_cycles() function and creates print statements that visually represent 
    the cyclic dependencies with arrows appointed
    
    Sample output:
    
    The StdLib packages form a cycle of dependency:
    1. package_A -> package_B -> package_C -> ...
    2. package_D -> package_A -> package_Z -> ...
    3. package_O -> package_Y -> package_B -> ...
    
    
    """
    circular_dependencies = find_cycles()
    print('The StdLib packages from a cycle of dependency:')
    lens = len(circular_dependencies)
    for i in range(lens):
        print(str(i + 1) + '.', end=' ')
        dep_lens = len(circular_dependencies[i])
        for j in range(dep_lens):
            if j != dep_lens - 1:
                print(circular_dependencies[i][j] + ' -->', end=' ')
            else:
                print(circular_dependencies[i][j])



# In[165]:


task5()


# # Task 6: Build the StdLib module connectivity graph

# In[17]:


def find_direct_graph():
    """
    Function Description:
    
    Produces a visual representation graph of standard library dependencies using networkx
    
    Red nodes represent core modules with no dependencies
    Blue nodes represent modules that have dependensies
    
    The lines connecting the nodes represent relationships
    
    """
    std_packages = get_real(get_stdlib_packages())
    all_output=[]
    def DFS(parent_package,children_package):
        if not children_package: #It's core libs
            return
        if (parent_package,children_package) not in all_output:
            if parent_package:
                all_output.append((parent_package,children_package))
        else:
            return
        depend_packages = module_dependency(std_packages,children_package)
        
        for i in depend_packages:
            DFS(children_package,i)
    
    #find all stdlibs
    for index,i in enumerate(std_packages):
    
        #print(f"Now finding {i:<20}, still have {len(std_packages)-index-1:>3}packages.")
        DFS("",i)
     
    return sorted(all_output)
    #find_direct_graph()


def task6(node="All"):
    """
    
    """
    std_packages = get_real(get_stdlib_packages())
    core_libs = list(filter(lambda x:len(module_dependency(std_packages,x))==0,std_packages))
    color_map = list(map(lambda x:"#FC766AFF" if x in core_libs else"#5B84B1FF",std_packages))

# Living Coral (#FC766AFF) is core_libs and Pacific Coast (#5B84B1FF) is other modules.
    packages = nx.DiGraph()
    packages.add_nodes_from(std_packages)
    if node=="All":
        packages.add_edges_from(find_direct_graph(),length=1)
    else:
        packages.add_edges_from(list(filter(lambda x:x[0]==node,find_direct_graph())),length=1)
    
    pos = nx.spring_layout(packages,k=1)
    fig = plt.figure(figsize=(24, 12),dpi=120)
    plt.title(f"{node} module dependency Network")
   
    nx.draw(packages,pos=pos,
            node_color=color_map,
            with_labels=True,
            node_size=400,
            font_size=10,
            width=1)
    plt.savefig(f"{node}_graph.png")
    std_packages = get_real(get_stdlib_packages())
    core_libs = list(filter(lambda x:len(module_dependency(std_packages,x))==0,std_packages))
    color_map = list(map(lambda x:"#FC766AFF" if x in core_libs else"#5B84B1FF",std_packages))

# Living Coral (#FC766AFF) is core_libs and Pacific Coast (#5B84B1FF) is other modules.
    packages = nx.DiGraph()
    packages.add_nodes_from(std_packages)

    if node=="All":
        packages.add_edges_from(find_direct_graph(),length=1)
    else:
        packages.add_edges_from(list(filter(lambda x:x[0]==node,find_direct_graph())),length=1)
    pos = nx.spring_layout(packages,k=1)
    fig = plt.figure(figsize=(24, 12),dpi=120)
    plt.title(f"{node} module dependency Network")
   
    nx.draw(packages,pos=pos,
    node_color=color_map,
    with_labels=True,
    node_size=400,
    font_size=10,
    width=1)
    plt.savefig(f"{node}_graph.png")

 


# In[18]:


task6() 


# In[161]:


class Solution:
    def __init__(self,data):
        self.data = data
        
    def analyse_stdlib(self):
        def GetStd(self):
            return task1()

        def GetImportable(self):
            return task2()

        def GetDependencies(self): 

            return task3()

        def GetPyFileAttributes(self): 
            return task4()

        def GetCyclicDependencies(self):
            return task5()
        return f"{GetStd(self),GetImportable(self),GetDependencies(self),GetPyFileAttributes(self),GetCyclicDependencies(self)}"
        

