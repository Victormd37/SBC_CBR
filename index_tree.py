import numpy as np
from classes import Case, User, Book

class Tree:

    """
    Aquesta clase conté un arbre indexat on a les fulles podem trobar els casos que
    comparteixen atributs similars
    """

    class TreeNode:

        def __init__(self, valores = [], feature = None, hijos = None):
            self.feature = feature
            self.valores = valores
            self.hijos = hijos
        
        def add_valor(self, valor):
            """Afegeix un nou índex a un node (aquest node será una fulla i l'index el d'un nou cas afegit en la fase de retain)"""
            self.valores += [valor]
        def get_casos(self):
            """Retorna els indexos de tots els casos que es troben en una mateixa fulla"""
            return self.valores
        def get_feature(self):
            """Retorna la característica que utilitza un node per separar els casos"""
            return self.feature
        def get_hijo_valor(self, carac):
            """Retorna el fill que conté els casos amb el valor d'atribut indicat (carac)"""
            return self.hijos.get(carac)
    
    def __init__(self, caracteristicas, casos, users, user_inst, book_inst):
        self.cases = casos
        self.users = users
        self.user_instances = user_inst
        self.book_instances = book_inst
        self.tree = self.crear_arbol(caracteristicas, self.users, self._get_numbercases())
        

    def crear_arbol(self, caracteristicas, users, n, valor = None):
        """
        Aquesta funció és l'encarregada de crear l'arbre indexat a partir dels casos i les característiques
        del perfil d'usuari.

        Per fer-ho utilitza el métode "_choose_best_partition" per escollir sobre quin atribut partir a cada node.
        L'arbre es dividirà fins que passi un dels següents casos:
            - Hi ha 10 o menys casos en un node
            - No hi ha més característiques per seguir dividint
            - Només hi ha un usuari que compleix les característiques però apareix en 10 casos o més.
            - Tots els usuaris que queden tenen les mateixes característiques (seguir dividint només augmenta la mida de l'arbre i les particions serien de n en una branca i 0 casos a l'altra)
        
        
        """
        if len(caracteristicas) != 0 and users[users.duplicated(subset= users.columns[1:],keep=False)].shape[0] != users.shape[0] and users.shape[0] > 1:
            if n > 50:
                best_c = self._choose_best_partition(caracteristicas, users, n)
                hijos = {}
                for i in caracteristicas[best_c]:
                    new_users = users.loc[users[best_c] == i]
                    l = new_users['Usuario_ID'].tolist()
                    suma = (self.cases['Usuario_ID'].isin(l)).sum()
                    c = caracteristicas.copy()
                    c.pop(best_c)
                    hijos[f"{i}"] = self.crear_arbol(c, new_users, suma) #Cridem recursivament a la funció
                arbol = self.TreeNode(valor, best_c, hijos)
            else:
                l = users['Usuario_ID'].tolist()
                casos = self.cases[self.cases['Usuario_ID'].isin(l)]
                lista_instancias_casos = []
                for row in casos.index:
                    row_elements = casos.loc[row]
                    instance = Case(row_elements[0], self.user_instances[row_elements[1]-1] 
                                    ,row_elements[2:6], self.book_instances[row_elements[6]])
                    lista_instancias_casos.append(instance)
                arbol = self.TreeNode(lista_instancias_casos) #Si arribem a un node fulla, aprofitem i afegim directament els indexos dels casos
        else:
            l = users['Usuario_ID'].tolist()
            casos = self.cases[self.cases['Usuario_ID'].isin(l)]
            lista_instancias_casos = []
            for row in casos.index:
                row_elements = casos.loc[row]
                instance = Case(row_elements[0], self.user_instances[row_elements[1]-1] 
                                ,row_elements[2:6], self.book_instances[row_elements[6]])
                lista_instancias_casos.append(instance)
            arbol = self.TreeNode(lista_instancias_casos) #Si arribem a un node fulla, aprofitem i afegim directament els indexos dels casos
        return arbol
    
    def _choose_best_partition(self, char, users, n):
        """
        Aquesta funció escull la característica per la qual el node haurà de dividir les dades.
        Per fer-ho, simula com quedaria la partició per cada una de les característiques.

        Per escollir la millor, busca aquella característica que reparteix millor els casos.
            Ex: Si una característica separa els casos en 25 i 25 i una altra ho fa en 15 35, escollirem la primera per fer la partició.
        
        Per aconseguir això calculem el valor òptim de les particions que serà: casos en aquell node/ modalitats de la característica.
        Un cop tenim aquest valor, farem la diferencia entre els casos que queden en cada partició amb el valor òptim:
            Ex: Amb 50 casos i 2 característiques amb 2 modalitats el valor òptim és 25.
                Característica 1: Separa en 15 35 els casos.  --->  |25-15| + |25-35|  =  20
                Característica 2: Separa en 22 28 els casos.  --->  |25-22| + |25-28|  =  6

                Com més petit el valor, millor separa la característica.
        """
        best_char = {}
        for key,values in char.items():
            if len(values) >1: #Això prevé que si un atribut només té una modalitat per falta de dades al cas inicial no es realitzin particions de més.
                n_i = n/len(values) #Calculem l'òptim
                best_char[key] = 0 #Assignem un valor de 0 que anirem incrementant si les particions generades s'allunyen de l'òptim
                for v in values:
                    l = users.loc[users[key] == v,['Usuario_ID']]['Usuario_ID'].tolist()
                    suma = (self.cases['Usuario_ID'].isin(l)).sum()
                    best_char[key] += abs(n_i - suma) #Calculem el valor absulut entre l'òptim i la partició real.
                    
        if len(best_char) > 1: #Això prevé que només hi hagi un atribut disponible per fer el filtratge, ja que no podriem fer el minim.
            return min(best_char, key = best_char.get)
        return list(best_char.keys())[0]
    
    def _get_numbercases(self):
        return self.cases.shape[0]
    
    def insertar_caso(self, caso, user_atr):
        """Donat la INSTANCIA d'un cas que es vol insertar i els atributs de l'usuari d'aquell cas s'inserta en el node corresponent."""
        nodo = self.tree
        while not nodo.hijos == None:
            atr = nodo.get_feature() 
            nodo = nodo.get_hijo_valor(user_atr[atr])
        nodo.add_valor(caso)
        
    
    def buscar_casos(self, new_case_atr):
        """Donat els atributs del nou usuari es busquen els casos que es troben al node del arbre que cumpleix les característiques de l'usuari."""
        nodo = self.tree
        while not nodo.hijos == None:
            atr = nodo.get_feature() 
            nodo = nodo.get_hijo_valor(new_case_atr[atr])
        return nodo.get_casos()
    
    def _crear_dict(self, nodo):
        """Crea un diccionari de l'arbre per poder-lo imprimir"""
        if nodo.hijos == None:
            return  [instancia.get_caseid() for instancia in nodo.valores]
        diccionario = {'Feature': nodo.feature}
        for valor,hijo in nodo.hijos.items():
            diccionario[valor] = self._crear_dict(hijo)
        return diccionario
    
    def __str__(self):
        """Permet imprimir el arbre com si fos un diccionari, permetent visualitzar de forma més o menys clara el seu contingut"""
        return str(self._crear_dict(self.tree))
