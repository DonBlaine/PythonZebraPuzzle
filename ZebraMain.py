from copy import deepcopy


class Domain:
    
    instances = []
    
    def __LargestDomain(self):
        """finds the largest domain in all instances of class domain"""
        x = Domain.instances[0]
        for item in Domain.instances:
            if len(item.house)>= len(x.house):
                x = item
              
        return x
        
    def __init__(self,name0,identifer):
        """create a domain given a name and identifer"""
        self.name = name0
        self.identifer = identifer
        self.house = [1,2,3,4,5]
        Domain.instances.append(self)
        
    def Destroy(self):
        """destroys the domain"""
        self = None
        Domain.instances.remove(self)
        
    def Printed (self):
        """print info on domain"""
        print ("Name is: " + self.name)
        print ("Identifer is: " + self.identifer)
        print ("House Potentials are: " + str(self.house))
        
    def Split(self):
        """split domain in half"""
        
        z = int(len(self.house)/2)
        if len(self.house)>1:
            a = self.house[0:z]
            b = self.house[z: ] 
    
            return (a,b)
        else:
            return False
        
    def CompareToAnotherDomain(self, x):
        """compares this domain to another domain"""
        return self.house == x.house
    
    def IsEmpty(self):
        """checks whether domain is empty"""
        return len(self.house) == 0
    
    def IsReducedToOnlyOneValue(self):
        """checks whether domain is only one value"""
        return len(self.house) == 1


class Constraint:
    number = 0
    
    def  __init__(self,type0):
        """creates constraint instance given name"""
        self.type0 = type0
        Constraint.number +=1
        
    def Delete(self):
        """deletes constraint instance"""
        self = None
        Constraint.number -=1
        
    def Printed(self):
        """prints constrain instance"""
        print ("type is: "+ self.type0)
        
    def IsSatisfied(self):
        """returns boolean if constraint is satisfied"""
        pass

    def GetDomains(self):
        pass
    
    def Reduction(self):
        """returns boolean if domain is empty after reduction"""
        pass


class  Constraint_equality_var_var(Constraint):
    
    def __init__(self,x,y):
        """creates constraint subclass of type Constraint_equality_var_var"""
        Constraint.__init__(self,Constraint_equality_var_var)
        self.d1=x
        self.d2=y
    
    def IsSatisfied(self):
        """returns true if at least one value is in both domains"""
        y = set(self.d1.house).intersection(self.d2.house)
        return y != 0
    
    def Reduction(self):
        """removes all non common values from both domain objects' domains"""
        y = list(set(self.d1.house).intersection(self.d2.house))
        self.d1.house = y
        self.d2.house = y
        if self.d1.IsEmpty() or self.d2.IsEmpty():
            return False
        else:
            return True
    
    def IsOneValue(self):
        """returns true if houses in each Domain object parameter are only one value"""
        return len(self.d1.house)==1 or len(self.d2.house)==1 
    
    def GetDomains(self):
        return (self.d1.name,self.d1.house,self.d2.name,self.d2.house)

           
    
class  Constraint_equality_var_cons(Constraint):
    
    def __init__(self,x,c):
        """creates constraint subclass of type Constraint_equality_var_cons"""
        Constraint.__init__(self,Constraint_equality_var_cons)
        self.d1 = x
        self.c=c
        
    def IsSatisfied(self):
        """returns true if value is in domain"""
        return self.c in self.d1.house
    
    def Reduction(self):
        """removes all values not specified by constraint from domain"""
        self.d1.house = [self.c]
        if self.d1.IsEmpty():
            return False
        else:
            return True
    
    def IsOneValue(self):
        """returns true if houses in each Domain object parameter are only one value"""
        return len(self.d1.house) == 1
    
    def GetDomains(self):
        return (self.d1.house,self.d1.house)


    
    
class  Constraint_equality_var_plus_cons(Constraint):
    
    def __init__(self,x,y,c):
        """creates constraint subclass of type Constraint_equality_var_plus_cons"""
        Constraint.__init__(self,Constraint_equality_var_plus_cons)
        self.d1=x
        self.d2=y
        self.c=c
        
    def IsSatisfied(self):
        """returns true if there exists a value in x's domain such that it equals a value in y's domain + c"""
        a = self.d1.house
        b = self.d2.house
        z=0
        for i in a:
            for j in b:
                if i == j + self.c:
                    z=1
                    break
        return z!=0
    
    def Reduction(self):
        """removes all values in x and y's domains that don't allow for x = y +c"""
        a = self.d1.house
        b = self.d2.house
        c = []
        d = []
        
        for i in a:
            z = 0
            for j in b:
                if i == j + self.c:
                    z = 1
            if z ==1:
                c.append(i)
                
        for j in b:
            z = 0
            for i in a:
                if j == i - self.c:
                    z = 1
            if z == 1:
                d.append(j)
        
        self.d1.house = c
        self.d2.house = d
                
        if self.d1.IsEmpty() or self.d2.IsEmpty():
            return False
        else:
            return True      

    def IsOneValue(self):
        """returns true if houses in each Domain object parameter are only one value"""
        return len(self.d1.house)==1 or len(self.d2.house)==1 
    
    def GetDomains(self):
        return (self.d1.name,self.d1.house,self.d2.name,self.d2.house)
    

class  Constraint_equality_var_abs_cons(Constraint):
    
    def __init__(self,x,y,c):
        """creates constraint subclass of type Constraint_equality_var_abs_cons"""
        Constraint.__init__(self,Constraint_equality_var_plus_cons)
        self.d1=x
        self.d2=y
        self.c=c

    def IsSatisfied(self):
        """returns true if there exists a value in x's domain such that |x-y|=1"""
        a = self.d1.house
        b = self.d2.house
        z=0
        for i in a:
            for j in b:
                if abs(i-j)== self.c:
                    z=1
                    break
        return z!=0
    
    def Reduction(self):
        """removes all values in x and y's domains that don't allow for |x-y|=1"""
        a = self.d1.house
        b = self.d2.house
        c = []
        d = []
        
        for i in a:
            z = 0
            for j in b:
                if abs(i-j) == self.c:
                    z = 1
                    
            if z == 1:
                c.append(i)
                
        for j in b:
            z = 0
            for i in a:
                if abs(i-j)==self.c:
                    z = 1
                    
            if z == 1:
                d.append(j)
        
        self.d1.house = c
        self.d2.house = d
                
        if self.d1.IsEmpty() or self.d2.IsEmpty():
            return False
        else:
            return True     
    
    def IsOneValue(self):
        """returns true if houses in each Domain object parameter are only one value"""
        return len(self.d1.house)==1 or len(self.d2.house)==1 
    
    def GetDomains(self):
        return (self.d1.name,self.d1.house,self.d2.name,self.d2.house)
    

    
class  Constraint_difference_var_var(Constraint):
    
    def __init__(self,x,y):
        """creates constraint subclass of type Constraint_difference_var_var"""
        Constraint.__init__(self,Constraint_difference_var_var)
        self.d1 = x
        self.d2 = y
        
    def IsSatisfied(self):
        """returns true if both domains do not have a single identical value"""
        return self.d1.house != self.d2.house or len(self.d1.house)>1 or len(self.d2.house)>1 
    
    def Reduction(self):
        """removes value in x or y domain depending on which object has only one value"""
        if len(self.d1.house)==1:
            self.d2.house = list(set(self.d2.house)-set(self.d1.house))
        elif len(self.d2.house)==1:
            self.d1.house = list(set(self.d1.house)-set(self.d2.house))
        else:
            pass
        if self.d1.IsEmpty() or self.d2.IsEmpty():
            return False
        else:
            return True

    def IsOneValue(self):
        """returns true if houses in each Domain object parameter are only one value"""
        return len(self.d1.house)==1 or len(self.d2.house)==1 
    
    def GetDomains(self):
        return (self.d1.name,self.d1.house,self.d2.name,self.d2.house)
    

class Problem:
    """This is the set of constraints and variables that will be used to solve the Zebra puzzle"""
    
    def __init__(self):
        
        

        self.english = Domain("english","nationalities")
        self.spaniard = Domain("spaniard","nationalities")
        self.ukrainian = Domain("ukrainian","nationalities")
        self.norwegian = Domain("norwegian","nationalities")
        self.japanese = Domain("japanese","nationalities")
        self.red = Domain("red","color")
        self.green = Domain("green","color")
        self.ivory = Domain("ivory","color")
        self.yellow = Domain("yellow","color")
        self.blue = Domain("blue","color")
        self.dog = Domain("dog","pet")
        self.snails = Domain("snails","pet")
        self.fox = Domain("fox","pet")
        self.horse = Domain("horse","pet")
        self.zebra = Domain("zebra","pet")
        self.snakes_and_ladders = Domain("snakes and ladders","board_games")
        self.cluedo = Domain("cluedo","board_games")
        self.pictionary = Domain("pictionary","board_games")
        self.travel_the_world = Domain("travel the world","board_games")
        self.backgammon = Domain("backgammon","board_games")
        self.water = Domain("water","beverages")
        self.coffee = Domain("coffee","beverages")
        self.tea = Domain("tea","beverages")
        self.milk = Domain("milk","beverages")
        self.orange_juice = Domain("orange juice","beverages")
        
        self.variables =[self.english,self.spaniard,self.ukrainian,self.norwegian,self.japanese,self.red,self.green,self.ivory,self.yellow,self.blue,self.dog,self.snails,self.fox,self.horse,self.zebra,self.snakes_and_ladders,self.cluedo,self.pictionary,self.travel_the_world,self.backgammon,self.water,self.coffee,self.tea,self.milk,self.orange_juice]
        
        self.con1 = Constraint_equality_var_var(self.english,self.red)
        self.con2 = Constraint_equality_var_var(self.spaniard,self.dog)
        self.con3 = Constraint_equality_var_var(self.coffee,self.green)
        self.con4 = Constraint_equality_var_var(self.ukrainian,self.tea)
        self.con5 = Constraint_equality_var_plus_cons(self.green,self.ivory,1)
        self.con6 = Constraint_equality_var_var(self.snakes_and_ladders,self.snails)
        self.con7 = Constraint_equality_var_var(self.cluedo,self.yellow)
        self.con8 = Constraint_equality_var_cons(self.milk,3)
        self.con9 = Constraint_equality_var_cons(self.norwegian,1)
        self.con10 = Constraint_equality_var_abs_cons(self.pictionary,self.fox,1)
        self.con11 = Constraint_equality_var_abs_cons(self.cluedo,self.horse,1)
        self.con12 = Constraint_equality_var_var(self.travel_the_world,self.orange_juice)
        self.con13 = Constraint_equality_var_var(self.japanese,self.backgammon)
        self.con14 = Constraint_equality_var_abs_cons(self.norwegian,self.blue,1)
        
        self.con15 = Constraint_difference_var_var(self.english,self.japanese)
        self.con16 = Constraint_difference_var_var(self.english,self.spaniard)
        self.con17 = Constraint_difference_var_var(self.english,self.ukrainian)
        self.con18 = Constraint_difference_var_var(self.english,self.norwegian)
        self.con19 = Constraint_difference_var_var(self.spaniard,self.japanese)
        self.con21 = Constraint_difference_var_var(self.spaniard,self.ukrainian)
        self.con22 = Constraint_difference_var_var(self.spaniard,self.norwegian)
        self.con23 = Constraint_difference_var_var(self.ukrainian,self.japanese)
        self.con24 = Constraint_difference_var_var(self.ukrainian,self.norwegian)
        self.con25 = Constraint_difference_var_var(self.norwegian,self.japanese)
        
        self.con20 = Constraint_difference_var_var(self.milk,self.orange_juice)
        
        self.con26 = Constraint_difference_var_var(self.red,self.green)
        self.con27 = Constraint_difference_var_var(self.red,self.ivory)
        self.con28 = Constraint_difference_var_var(self.red,self.yellow)
        self.con29 = Constraint_difference_var_var(self.red,self.blue)
        self.con30 = Constraint_difference_var_var(self.ivory,self.green)
        self.con31 = Constraint_difference_var_var(self.yellow,self.green)
        self.con32 = Constraint_difference_var_var(self.blue,self.green)
        self.con33 = Constraint_difference_var_var(self.ivory,self.yellow)
        self.con34 = Constraint_difference_var_var(self.ivory,self.blue)
        self.con35 = Constraint_difference_var_var(self.yellow,self.blue)
        
        self.con36 = Constraint_difference_var_var(self.dog,self.snails)
        self.con37 = Constraint_difference_var_var(self.dog,self.fox)
        self.con38 = Constraint_difference_var_var(self.dog,self.horse)
        self.con39 = Constraint_difference_var_var(self.dog,self.zebra)
        self.con40 = Constraint_difference_var_var(self.snails,self.fox)
        self.con41 = Constraint_difference_var_var(self.snails,self.horse)
        self.con42 = Constraint_difference_var_var(self.snails,self.zebra)
        self.con43 = Constraint_difference_var_var(self.fox,self.horse)
        self.con44 = Constraint_difference_var_var(self.fox,self.zebra)
        self.con45 = Constraint_difference_var_var(self.horse,self.zebra)
        
        self.con46 = Constraint_difference_var_var(self.snakes_and_ladders,self.cluedo)
        self.con47 = Constraint_difference_var_var(self.snakes_and_ladders,self.pictionary)
        self.con48 = Constraint_difference_var_var(self.snakes_and_ladders,self.travel_the_world)
        self.con49 = Constraint_difference_var_var(self.snakes_and_ladders,self.backgammon)
        self.con50 = Constraint_difference_var_var(self.cluedo,self.pictionary)
        self.con51 = Constraint_difference_var_var(self.cluedo,self.travel_the_world)
        self.con52 = Constraint_difference_var_var(self.cluedo,self.backgammon)
        self.con53 = Constraint_difference_var_var(self.pictionary,self.travel_the_world)
        self.con54 = Constraint_difference_var_var(self.pictionary,self.backgammon)
        self.con55 = Constraint_difference_var_var(self.travel_the_world,self.backgammon)
        
        self.con56 = Constraint_difference_var_var(self.water,self.coffee)
        self.con57 = Constraint_difference_var_var(self.water,self.tea)
        self.con58 = Constraint_difference_var_var(self.water,self.milk)
        self.con59 = Constraint_difference_var_var(self.water,self.orange_juice)
        self.con60 = Constraint_difference_var_var(self.coffee,self.tea)
        self.con61 = Constraint_difference_var_var(self.coffee,self.milk)
        self.con62 = Constraint_difference_var_var(self.coffee,self.orange_juice)
        self.con63 = Constraint_difference_var_var(self.tea,self.milk)
        self.con64 = Constraint_difference_var_var(self.tea,self.orange_juice)
        #10 constraint for beverages is listed as con20
        
        self.con_straints = [self.con1,self.con2,self.con3,self.con4,self.con5,self.con6,self.con7,self.con8,self.con9,self.con10,self.con11,self.con12,self.con13,self.con14,self.con15,self.con16,self.con17,self.con18,self.con19,self.con20,self.con21,self.con22,self.con23,self.con24,self.con25,self.con26,self.con27,self.con28,self.con29,self.con30,self.con31,self.con32,self.con33,self.con34,self.con35,self.con36,self.con37,self.con38,self.con39,self.con40,self.con41,self.con42,self.con43,self.con44,self.con45,self.con46,self.con47,self.con48,self.con49,self.con50,self.con51,self.con52,self.con53,self.con54,self.con55,self.con56,self.con57,self.con58,self.con59,self.con60,self.con61,self.con62,self.con63,self.con64]
        
    def ConstraintReduction(self):
        """iterates over constraints and does reduction until empty domain is found or nothing happens"""
        
        while True:
            templist = []
            for item in self.variables:
                templist.append(item.house)
                if item.IsEmpty():
                    return 0
            
            for item in self.con_straints:
                item.Reduction()
          
            templist2 = []
            for item in self.variables:
                templist2.append(item.house)
                if item.IsEmpty():
                    return 0
                
            if templist == templist2:
                return None

    def PrintVariables(self):
        for item in self.variables:
            item.Printed()
           
class Trees:
    """Blueprint for binary tree data structure"""
    count = 0
         
    def __init__(self, elem):
        self.elem = elem
        self.left = None
        self.right = None
        Trees.count +=1
               
    def addRight(self, elem):
               
        self.right = elem
           
    def addLeft(self,elem):
               
        self.left = elem
           
    def removeLeft(self,elem):
       
        self.left = None
               
    def removeRight(self,elem):
               
        self.right = None    
           
    def getLeft(self):
        return self.left
           
    def getRight(self):
        return self.right
               
    def isEmpty(self):
        return self.elem == None
       
    def getPayload(self):
        return self.elem
    
    def removePayload(self):
        self.elem = None
        Trees.count -=1

  
def RecursiveTree(tree):
    """This function takes in a tree, gets the domain variables from the problem instance object then
    if that domain is not empty or one value, creates two new problem instances, adds those to the 
    tree structure then runs this function on those two new tree nodes"""
       
    x = tree.getPayload()
    y = x.ConstraintReduction()  

    
    if y ==0:
        return False
    else:
        if all(item.IsReducedToOnlyOneValue() for item in x.variables):
            return True
        else:
            a = x.variables[0]
            for item in x.variables:
                if len(item.house)>= 2:
                    a = item
                    break
            z = x.variables.index(a)
            y = a.Split()
            domainlist2 = deepcopy(x)
            domainlist3 = deepcopy(x)
            domainlist2.variables[z].house = y[0]
            domainlist3.variables[z].house = y[1]
          
               
            tree1 = Trees(domainlist2)
            tree2 = Trees(domainlist3)
              
            tree.addLeft(tree1)
            tree.addRight(tree2)
              
            results_left = RecursiveTree(tree1)
            results_right = RecursiveTree(tree2)
              
            return (results_left,results_right)

            
def FindOneValue(tree):
    """This function takes in a payload and returns tree if the tree payload has domains that only have one value"""
       
    y = tree.getPayload()
    z = y.variables
    return all(item.IsReducedToOnlyOneValue()for item in z)
             
def Traverse(tree):
    """This function takes in a tree and traverses the tree then returns the payload of the 
    tree node that has domains with only one value"""
       
    if FindOneValue(tree):
        return tree.getPayload()
    else:
        if tree.left != None:
            return Traverse(tree.left)
         
        if tree.right != None:
            return Traverse(tree.right)   
     
  

y = Trees(Problem())
RecursiveTree(y)
z = Traverse(y)

print ("The house numbers for each variable are: " +"\n")

for item in z.variables:
    print("Variable "+item.name+" is in house "+ str(item.house[0]))

