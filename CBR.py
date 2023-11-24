class CBR():

    def __init__(self,case_db,domain):
        self.cases = case_db #Base de Dades?
        self.domain = domain #Arbre?

    def retrieve(self, new_case):
        pass

    def reuse(self):
        pass
    
    def revise(self):
        pass

    def retain(self):
        pass

    def _similarity(self,new_case):
        

class User():

    def __init__(self,atributes):
        self.a1 = atributes[0]
        self.a2 = atributes[1]
        self.a3 = atributes[2]
        self.a4 = atributes[3]
        self.a5 = atributes[4]

class Book():

    def __init__(self,atributes):
        self.a1 = atributes[0]
        self.a2 = atributes[1]
        self.a3 = atributes[2]
        self.a4 = atributes[3]
        self.a5 = atributes[4]

def ask_questions():
    pass   

db = [1,2,3,4,5,6]
print(db)
domain = ["a","b","c","d","k"]
print(domain)


cbr = CBR(db,domain)

if __name__ == '__main__':

    ask_questions()
    