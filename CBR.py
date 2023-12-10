import pandas as pd
from index_tree import Tree
from classes import User,Case,Book
from datetime import datetime
import numpy as np

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
            instance = Book(row_elements[0], row_elements[2] ,row_elements[3:])
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
        user = new_case.get_user()
        username = new_case.get_user().get_username()

        similar_cases= self.index_tree.buscar_casos(user) #Recuperem els indexos dels n casos en una mateixa fulla
        similar_cases = [elem for elem in similar_cases if elem.get_user().get_username() != username and elem.get_rating() > 3]  #eliminem els casos que pertanyen al propi usuari
        sim = []
        for i in similar_cases:
            sim.append(self._custom_similarity_users(new_case,i)) #Buscamos la similaridad entre nuestro caso y un caso similar
        pares = zip(similar_cases,sim)
        pares_ordenados = sorted(pares, key=lambda x: x[1]) #Ordenamos los casos ascendentemente
        if len(similar_cases) > 10:
            similar_cases =pares_ordenados[:10] #Cojemos los 10 casos más similares
        else:
            similar_cases = pares_ordenados
        
        return similar_cases

    # most_similar_cases ha de ser una llista amb aquelles instancies de casos més similars
    def reuse(self, most_similar_cases, actual_case): 
        """
        Rep els casos on l'ususari és més similar, inferim les preferencies especifiques de l'usuari en funció
        de l'historial que tinguem seu i adaptem la solució. Per adaptar la solució, seleccionem aquells llibres 
        que trobem en els casos més similars i calculem la seva similitud amb el cas ideal inferit. Finalment retornem 
        els 3 llibres on la similaritat de llibre es major 
        """
        ideal_book = self._infer_user_preferences(actual_case.get_user())
        actual_case.atributes_pref = ideal_book
        final_similarities = []
        # We compute the similarity between ideal_book with books 
        # characteristics recomended in the most similar cases retrieved 
        # by user's profile
        for case,sim_users in most_similar_cases:
            book_atributes = list(case.get_book().get_book_features())
            similarity_book = self._custom_similarity_books(ideal_book, book_atributes)
            final_similarities.append((similarity_book, case)) #Devolvemos una tupla con la similaridad, la instancia de caso
        sorted_books = sorted(final_similarities, key=lambda x: x[0], reverse=True)
        return sorted_books[0:3]

    
    def revise(self, cases_list, new_case):
        # first we calculate the timestamp since the day we had de cases database
        date_today = datetime.now()
        day_90 = datetime(2023, 12, 8) # ja canviarem aquesta data
        difference_days = (date_today - day_90).days
        timestamp = 90 + difference_days
        new_cases = []
        i = 0
        for sim, case in cases_list:
            n_case = Case(new_case.get_caseid()+i,new_case.get_user(), new_case.get_user_preferences())
            conf = sim*100
            print(f"Te recomendamos el libro {case.get_book().get_title()} con una confianza del {conf}%")
            # demanem que es puntui la recomanació del llibre
            try:
                rating = float(input("Puntúa la recomendación obtenida del libro '{}' (1-5)".format(case.get_book().get_title())))
            except ValueError:
                print("Por favor, ingresa una puntuación válida.")
            # afegim a la instància cas
            n_case.book = case.get_book()
            n_case.rating = rating
            n_case.timestamp = timestamp
            new_cases.append(n_case)   
            i += 1 
        return new_cases

    def retain(self,cases):
        """ IMPORTANTE: Al añadir un caso sumar 1 a self.number_cases, si se quita un caso restar 1."""
        # arriben 3 instàncies de cas (ens quedem tots) (cases es una llista que els inclou)
        # rep l'arbre ja que s'haurà d'anar actualitzant
        # Comencem afegint tant a l'arbre (amb metode insertar caso) com a la base de dades tots els casos que arribin, mantenint coherent la variable num casos
        # despres ja identificarem si cal eliminar casos, no quedar-se amb alguns perque son inutils o redundants...
        # caldrà afegir el cas a la base de dades i a l'arbre, i afegir l'usuari a la base de dades 

        for case in cases: 
            """ Comencem afegint l'usuari d'aquell cas a la base de dades """
            # Obtener el usuario del caso
            user = case.get_user()

            # Verificar si el usuario ya está en la base de datos
            # Funciona si user es una instancia d'usuari, si es llista, canviar detall de user.get_username()
            user_exists = any(u.get_username() == user.get_username() for u in self.users_inst)

            # Si el usuario no está en la base de datos, añadirlo
            if not user_exists:
                # Convertir la información del usuario a una fila de DataFrame
                user_row = user.to_dataframe_row()

                # Añadir la fila a la base de datos de usuarios
                self.users = pd.concat([self.users, user_row], ignore_index=True)
                self.users_inst.append(user)  # Añadir la instancia del usuario a la lista de instancias

            """ Ara hem d'afegir el nou cas a la base de dades i a l'arbre """

            # Adaptem la info del cas i l'afegim a la base de dades
            case_row = case.to_dataframe_row()
            self.cases = pd.concat([self.cases, case_row], ignore_index=True)

            # Afegim el cas a l'arbre
            # Quan modifiquem classe insertar_caso per a que no calguin user prefs, no passar segon param 
            self.index_tree.insertar_caso(case,case.get_user_preferences())
            
            # Augmentem el nombre de casos en 1, ja que n'acabem d'afegir un
            self.number_cases += 1 
        # identificar casos redundants i casos inutils (??) 
        # metode auxiliar: mirar quins casos tenen timestamp més antic i eliminar-los 
        # afegir tant en el pandas com en l'arbre
        # emmagatzemar el nou i carregar-nos els antics


    def _build_index_tree(self):
        """
        Aquest métode obte les diferents variables i modalitats del perfil d'usuari.

        Retorna un arbre indexat amb tots els casos de la base de casos actual classificats.
        """
        char = {}
        for col in self.users.columns:
            if col != 'Usuario':
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
        weighted_disimilarity=0
        total_weight = 0

        # Definimos pesos de los atributos
        weights = {'contiene':4, 'formato': 1, 'idioma': 2, 'largura_libro': 1,
                   'clasificacion_edad':3, 'compone_saga':1, 'famoso':1, 'peso':1,
                   'tipo_narrador':2}
        
        for i, feature in enumerate(weights.items()):
            ele1 = ideal_features[i]
            ele2 = book_features[i]
            # Calculamos similarity con pesos
            attr = feature[0]
            weight = feature[1]
            # Afegim relacions de distancia entre certes modalitats
            related_attr = {'largura_libro','clasificacion_edad','peso'}
            if attr in related_attr: 
                map = {'largura_libro':{'corto':0, 'normal':1, 'largo':2},
                'clasificacion_edad':{'infantil':0, 'juvenil':1,'adulto':2},
                'peso': {'ligero':0, 'intermedio':1,'pesado':2}}
                diff = abs(map[attr][ele1] - map[attr][ele2])
                weighted_disimilarity += weight*diff
            else:
                if type(ele2) != list:
                    if ele1 != ele2:
                        weighted_disimilarity += weight
                else:
                    if ele1 not in ele2:
                        weighted_disimilarity += weight
            total_weight += weight
        
        # Normalizamos el resultado 
        weighted_disimilarity /= total_weight

        return 1 - weighted_disimilarity
    
    def _infer_user_preferences(self,user):
        '''
        Rep l'usuari per al qual volem fer la recomanació. Recopila tota la info de
        les recomanacions previes. Utilitzant aquesta informació infereix quins són
        els atributs dels llibres que més li agraden. En el pas d'inferencia fa us 
        de: Timestamp, Rating i Atributs dels llibres recomenats. 
        '''
        user_id = user.get_username()
        # Obtenim tots els casos de la mateixa fulla de l'arbre a la que correspon l'usuari
        
        leaf_cases = self.index_tree.buscar_casos(user)
        user_cases = [case for case in leaf_cases if case.get_user().get_username() == user_id]

        # Si l'usuari es nou i no tenim historial li preguntem :
        if len(user_cases) == 0:
            user_prefs = self._ask_user_prefs()
            return user_prefs
        
        user_db = {
            'Book_features':[list(case.get_book().get_book_features()) for case in user_cases],
            'Rating':[case.get_rating() for case in user_cases],
            'Timestamp':[case.get_timestamp() for case in user_cases]
        }
        df = pd.DataFrame(user_db)
        df['Normalized_Rating'] = df['Rating'].div(5)

        decay_factor = 0.1  # Adjust this based on the desired decay rate

        # Representem formula: e^(-decay_factor * time_differences) on time_differences 
        # es la diferencia entre el timestamp més recent i timestamp en questió. 
        df['Weight'] = np.exp(-(df['Timestamp'].max() - df['Timestamp']) * decay_factor) # Estarà entre 0 i 1.
        df['Combined_Value'] = df['Normalized_Rating'] * df['Weight'] # Combinem els 2 valors

        dict = {'contiene':{}, 'formato': {}, 'idioma': {}, 'largura_libro': {},
                   'clasificacion_edad':{}, 'compone_saga':{}, 'famoso':{}, 'peso':{},
                   'tipo_narrador':{}}

        # Calcul de quines són les caracteristiques preferides a partir de sum(Combined value)/len(values) 
        for i, feature in enumerate(dict.items()):
            attr = feature[0]
            for j in range(len(df)):
                sign = 1
                if df['Rating'][j] <= 2:
                    sign = -1
                ele = df['Book_features'][j][i]                
                if type(ele) == list:
                    for e in ele:
                        if e in dict[attr].keys():
                            dict[attr][e].append(sign*df['Combined_Value'][j])
                        else:
                            dict[attr][e] = [sign*df['Combined_Value'][j]]
                else:
                    if ele in dict[attr].keys():
                        dict[attr][ele].append(sign*df['Combined_Value'][j])
                    else:
                        dict[attr][ele] = [sign*df['Combined_Value'][j]]
        user_preferences = []
        for key in dict:
            for feature in dict[key]:
                values = dict[key][feature]
                dict[key][feature] = sum(values)/len(values)
            best = max(dict[key].items(), key=lambda item: item[1])[0]
            user_preferences.append(best)
        return user_preferences
    
    def _ask_user_prefs(self):
        """
        Funció per preguntar a usuaris nous les seves preferències
        """
        user_prefs = []

        return user_prefs

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