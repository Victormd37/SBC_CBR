import pandas as pd
from index_tree import Tree

class CBR():

    def __init__(self, domain, case_db, users_db):
        self.cases = case_db 
        self.users = users_db 
        self.domain = domain 
        self.index_tree = self._build_index_tree()

    def retrieve(self, new_case):
        """
        New_case: diccionari que conté tots els atributs que composen un cas.
        Aquest new_case encara no esta a la base de casos pero pot ser que el Usuari si que es trobi a la base d'usuaris.

        En cas que al realitzar les preguntes no s'hagi trobat, es realitzaran les preguntes adients per trobar el perfil d'usuari
        i s'afegirà SEMPRE a la base d'usuaris.
        """
        user_id = new_case['User_id'] # Obtenim user_id del cas nou
        user = self.users[user_id] # Obtenim la instancia d'usuari guardat a users_db

        similar_cases_id = self.index_tree.buscar_casos(user) #Recuperem els indexos dels n casos més similars
        # Per els usuaris del cluster 
            # Crear sets amb info del profile i preferences
            # cridem self._jaccard_similarity(set1, set2) per calcular la similaritat entre 2 usuaris
        pass

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
        return Tree(char,self.cases,self.users)

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

def ask_questions():
    pass   