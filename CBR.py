import pandas as pd
from index_tree import Tree

class CBR():

    def __init__(self, db, domain, case_db, users_db):
        self.cases = case_db #Base de Dades? Arbre jerarquic?
        self.users = users_db #Base de dades d'usuaris
        self.domain = domain #Arbre?
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

    def reuse(self):
        pass
    
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


    def _jaccard_similarity(self,set1, set2):
        '''
        En aquest mètode calcularem la metrica de similitud que 
        utilitzarem per determinar com de similars són dos usuaris. 
        De moment només utilitzarem el User Profile i el User preferences.
        Donat que es són vectors de strings utilitzarem Jaccard Similarity.
        '''
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    def _custom_similarity(self,user1, user2):
        '''
        Calculem custom similarity otorgant pesos a aquelles 
        caracteristiques que considerem més importants. 
        '''
        weighted_similarity=0
        total_weight = 0

        # Listas de profile + preferences (atributos multislot son listas)
        features1 = user1.get_user_profile()
        features1.extend(user1.get_user_preferences())
        features2 = user2.get_user_profile()
        features2.extend(user2.get_user_preferences())

        # Definimos pesos de los atributos
        weights = {'Genero':1, 'Edad': 1, 'Vacaciones': 2,
                    'Genero_literario':3}
        
        # Calculamos jaccard similarity con pesos
        for i, feature in enumerate(weights.items()):
            if isinstance(features1[i],list): # Cas especial per atributs multislot
                set1 = set(features1[i])
                set2 = set(features2[i])
            else:
                set1 = set([features1[i]])
                set2 = set([features2[i]])

            weight = feature[1] # Extraemos el peso de la tupla feature
            similarity = self._jaccard_similarity(set1, set2)
            weighted_similarity += weight * similarity
            total_weight += weight

        # Normalizamos el resultado 
        if total_weight != 0:
            weighted_similarity /= total_weight

        return weighted_similarity


class User():

    def __init__(self,atributes_prof, atributes_pref):
        self.atributes_prof = atributes_prof
        self.atributes_pref = atributes_pref
    
    def get_user_profile(self):
        '''
        Devuelve una lista con los atributos del perfil del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.atributes_prof

    def get_user_preferences(self):
        '''
        Devuelve una lista con los atributos de las preferencias del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.atributes_pref

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
#print(db)
domain = ["a","b","c","d","k"]
#print(domain)

# Definir cases_db amb ids
# Exemple (tindrà aquesta forma) emplenar a partir de csv drive:
cases_db = {
    'Case_id': [1,2,3,4,5,6,7,8],
    'User_id': [1,1,2,2,3,2,3,4], # Poden repetir-se
    'Book_id': [0,0,0,0,0,0,0,0], # Poden repetir-se
    'User_preferences': [0,0,0,0,0,0,0,0],
    #'Comprado': [] ?
    'Rating': [0,0,0,0,0,0,0,0], # Valoracions de l'1 al 5 (de moment)
    #'Timestep': []
}

cases_db = pd.DataFrame(cases_db)

cases_db = pd.read_csv("Casos.csv")

# Això s'haurà d'emplenar a partir del csv drive, en el cas de users també al ask():
# Definir users_db (propies instancies usuaris)
users_db = {
    'User_id': [1,2,3,4],
    'Genero' : ['Hombre', 'Mujer', 'Hombre', 'Mujer'],
    'Edad': ['Adulto','Adulto','Adulto','Adulto'],
    'Hobbies': ['Playa', 'Montaña', 'Playa', 'Playa']
}

users_db = pd.DataFrame(users_db)

users_db = pd.read_csv("Usuarios.csv")
# Definir books_db (propies instancies usuaris)

print(cases_db)

print(users_db)

cbr = CBR(db,domain, cases_db, users_db)

'''
if __name__ == '__main__':

    ask_questions()
'''

#print(cbr.index_tree.tree.hijos['Hombre'].valores)

#cbr.index_tree.insertar_caso(9,{'Genero': 'Mujer','Edad': 'Adulto','Hobbies': 'Playa'})

#print(cbr.index_tree.tree.hijos['Hombre'].valores)
#print(cbr.index_tree.tree.hijos['Mujer'].hijos['Playa'].valores)

#print(cbr.index_tree.buscar_casos({'Genero': 'Hombre','Edad': 'Adulto','Hobbies': 'Montaña'}))

print(cbr.index_tree)

#sim_custom = cbr._custom_similarity(user_db.iat[0,1], user_db.iat[3,1])
#sim_jaccard = cbr._jaccard_similarity(user_db.iat[0,1], user_db.iat[3,1])

#print(sim_custom)
#print(sim_jaccard)