import pandas as pd
from index_tree import Tree
from classes import User,Case,Book

class CBR():

    def __init__(self, case_db, users_db, books_db):
        self.cases = case_db 
        self.users = users_db 
        self.users_inst = []
        for row in range(len(users_db)):
            row_elements = users_db.loc[row]
            instance = User(row_elements[0], row_elements[1:])
            self.users_inst.append(instance)

        self.books_db = books_db
        self.books_inst = []
        for row in range(len(books_db)):
            row_elements = books_db.loc[row]
            instance = Book(row_elements[0], row_elements[1] ,row_elements[2:])
            self.books_inst.append(instance)

        self.number_cases = self.cases.shape[0] #Obtenim el nombre de casos actuals, anirem modificant si afegim o retirem casos
        self.index_tree = self._build_index_tree()

    def retrieve(self, new_case):
        """
        New_case: Instancia de Case (no te tots els atributs encara).
        Aquest new_case encara no esta a la base de casos pero pot ser que el Usuari si que es trobi a la base d'usuaris.

        En cas que al realitzar les preguntes no s'hagi trobat, es realitzaran les preguntes adients per trobar el perfil d'usuari
        i s'afegirà SEMPRE a la base d'usuaris.
        """
        user = new_case.get_user().get_user_profile()

        similar_cases= self.index_tree.buscar_casos(user) #Recuperem els indexos dels n casos més similars
        
        return similar_cases

    # most_similar_cases ha de ser una llista amb aquelles instancies de casos més similars
    def reuse(self, most_similar_cases, actual_case): 
        ideal_book = list(actual_case.get_user_preferences())
        book_similarities = []
        # We compute the similarity between ideal_book with books 
        # characteristics recomended in the most similar cases retrieved 
        # by user's profile
        for case in most_similar_cases:
            book_atributes = list(case.get_book().get_book_features())
            similarity = self._custom_similarity_books(ideal_book, book_atributes)
            book_similarities.append((similarity, case))
        sorted_books = sorted(book_similarities, key=lambda x: x[0], reverse=True)
        return sorted_books[0:3]

    
    def revise(self):
        pass

    def retain(self):
        """ IMPORTANTE: Al añadir un caso sumar 1 a self.number_cases, si se quita un caso restar 1."""
        pass


    def _build_index_tree(self):
        """
        Aquest métode obte les diferents variables i modalitats del perfil d'usuari.

        Retorna un arbre indexat amb tots els casos de la base de casos actual classificats.
        """
        char = {}
        for col in self.users.columns:
            if col != 'User_id':
                char[col] = self.users[col].unique()
        return Tree(char,self.cases,self.users, self.users_inst, self.books_inst)

    def _custom_similarity_users(self,case1, case2):
        '''
        Calculem custom similarity otorgant pesos a aquelles 
        caracteristiques que considerem més importants. 
        '''
        weighted_similarity=0
        total_weight = 0

        # Listas de profile features
        features1 = case1.get_user().get_user_profile()
        features2 = case2.get_user().get_user_profile()

        # Definimos pesos de los atributos
        # Ajustar pesos en función de los resultados
        weights = {'Genero':1, 'Edad': 1, 'Classe social': 2, 
                   'Trabajo': 2, 'Horas de lectura a la semana' : 3,	
                   'Musica': 1,'Tarde libre':1, 'Vacaciones':1}  
        
        # Calculamos jaccard similarity con pesos
        for i, feature in enumerate(weights.items()):
            ele1 = features1[i]
            ele2 = features2[i]
            weight = feature[1] # Extraemos el peso de la tupla feature
            if ele1 == ele2:
                weighted_similarity += weight
            total_weight += weight
        
        # Normalizamos el resultado 
        if total_weight != 0:
            weighted_similarity /= total_weight

        return weighted_similarity
    
    def _custom_similarity_books(self, ideal_features, book_features):
        '''
        Calculem custom similarity otorgant pesos a aquelles 
        caracteristiques que considerem més importants. 
        '''
        weighted_similarity=0
        total_weight = 0
        # Definimos pesos de los atributos
        # Ajustar pesos en función de los resultados
        weights = {'Genero':3, 'Largura': 2, 'Formato': 1, 'Idioma': 1}  
        for i, feature in enumerate(weights.items()):
            ele1 = ideal_features[i]
            ele2 = book_features[i]
        
            # Calculamos similarity con pesos
            attr = feature[0]
            weight = feature[1] # Extraemos el peso de la tupla feature
            if attr == 'Largura':
                if ele1 == ele2:
                    weighted_similarity += weight
            else:
                if ele1 in ele2:
                    weighted_similarity += weight
            total_weight += weight
        
        # Normalizamos el resultado 
        if total_weight != 0:
            weighted_similarity /= total_weight

        return weighted_similarity

    def ask_questions(self):

        """
        Aquesta funció hauria de fer les preguntes necessaries per extreure:
            1. En cas que l'usuario no es trobi (preguntar username), extreure el perfil de l'usuari.
                1.1 Si l'usuari es troba a la llista d'instancies, retornar la posició a la llista.
                1.2 Si no, crear el perfil d'usuari, crear la instancia, i afegirlo al final de la llista d'instancies.
            2. Extreure les preferencies de l'usuari per aquest cas.
        
        Retorna una instancia de CASE on només tenim el perfil d'usuari i les seves preferencies: Case(self.number_cases + 1, User_instance, Diccionari d'atributs)
        """
        pass   