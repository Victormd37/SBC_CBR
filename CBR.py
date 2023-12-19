import pandas as pd
from index_tree import Tree
from classes import User,Case,Book
from datetime import datetime
import numpy as np
from unidecode import unidecode


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

    def retrieve(self, new_case, num_cases_retrieve):
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
        pares_ordenados = sorted(pares, key=lambda x: x[1], reverse=True) #Ordenamos los casos ascendentemente
        if len(similar_cases) > num_cases_retrieve:
            similar_cases =pares_ordenados[:num_cases_retrieve] #Cojemos los 10 casos más similares
        else:
            similar_cases = pares_ordenados
        
        return similar_cases

    # most_similar_cases ha de ser una llista amb aquelles instancies de casos més similars

    # Answers es un valor binari que ens diu si les prefs han estat respostes o han des ser inferides.
    def reuse(self, most_similar_cases, actual_case): 
        """
        Rep els casos on l'ususari és més similar, inferim les preferencies especifiques de l'usuari en funció
        de l'historial que tinguem seu i adaptem la solució. Per adaptar la solució, seleccionem aquells llibres 
        que trobem en els casos més similars i calculem la seva similitud amb el cas ideal inferit. Finalment retornem 
        els 3 llibres on la similaritat de llibre es major 
        """
        if actual_case.get_user().get_username() < len(self.users_inst):
            ideal_book = self._infer_user_preferences(actual_case.get_user())
            actual_pref = actual_case.get_user_preferences()
            if actual_pref == None:
                print("cucu")
                actual_case.atributes_pref = ideal_book
            else:
                for i in range(len(actual_pref)):
                    if actual_pref[i] == None:
                        actual_pref[i] = ideal_book[i]
                        print(ideal_book[i])
                actual_case.atributes_pref = actual_pref
        final_similarities = []
        books = []
        # We compute the similarity between ideal_book with books 
        # characteristics recomended in the most similar cases retrieved 
        # by user's profile
        for case,sim_users in most_similar_cases:
            book_atributes = list(case.get_book().get_book_features())
            # Matched attributes són aquelles coses del llibre que són iguals que al cas ideal
            similarity_book, matched_attributes = self._custom_similarity_books(actual_case.get_user_preferences(), book_atributes)
            # Calculem similaritat combinada llibre, usuari i rating. 
            comb_sim = similarity_book*0.6 + sim_users*0.2 + (case.get_rating()/5)*0.2
            # Devolvemos una tupla con la similaridad, la instancia de caso i matched attributes
            book = case.get_book().get_book_id()
            if book not in books:
                books.append(book)
                final_similarities.append((comb_sim, case, matched_attributes)) 
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
        print(new_case.get_caseid())
        for sim, case, match_attr in cases_list:
            n_case = Case(new_case.get_caseid()+i,new_case.get_user(), new_case.get_user_preferences())
            conf = sim*100
            print()
            print(f"Te recomendamos el libro '{case.get_book().get_title()}' con una confianza del {conf}%")
            print()
            justificacion = self._justify_recomendation(match_attr)
            print(justificacion)
            print()
            # demanem que es puntui la recomanació del llibre
            rating = 0
            while rating not in range(1,6):
                try:
                    rating = int(input("Puntúa la recomendación obtenida del libro '{}' (1-5) ".format(case.get_book().get_title())))
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
        # Arriben 3 instàncies de cas (ens quedem tots) (cases es una llista que els inclou)
        # Mirem quin es el timestamp dels casos que arriben perque posteriorment potser ens fa falta per eliminar casos inútils 
        # Els 3 casos que arriben tindran el mateix timestamp, per tant, prenent-ne el de un ja és suficient 
        new_timestamp = cases[0].get_timestamp()
        
        # Obtenim l'usuari del cas, tots els casos que arribin seran del mateix usuari:
        user = cases[0].get_user()

        for case in cases: 

            ''' Vigilar redundància'''
            # buscar casos idèntics o amb usuaris similars i mateix llibre i quedar-nos amb el que tingui timestamp més recent (el nou cas)
            # buscar casos redundants iterant sobre els casos emmagatzemats en la mateixa fulla 
            # el que farem serà partir d'una base de dades en la que suposem que no hi ha casos redundants i aleshores, cada cop que anem a afegir un nou cas, anar a la fulla on li tocaria anar a aquell cas i buscar si el fet d'afegir aquest nou cas crearia redundància en aquella fulla
            # accedint a l'arbre podem arribar a obtenir els casos d'una fulla com a instància 
            # cridar els mètodes que calculen la similaritat i aplicarem thresholds en aquests valors per determinar quins casos van fora
            # cada cop que eliminem un cas, aquest s'ha d'esborrar tant de l'arbre com del dataset

            # Veiem els casos que hi ha a la fulla on anirà emmagatzemat per vigilar si crearem redundància en afegir-lo 
            cases_leaf = self.index_tree.buscar_casos(case.get_user())

            # Preparem una llista en la que guardarem tots aquells casos antics que causin conflicte de redundància amb el nou
            cases_to_delete = []

            # Comparem el cas nou amb cadascun dels presents ja a la fulla 
            for case_old in cases_leaf: 
                similarity_users = self._custom_similarity_users(case,case_old)

                # Si els usuaris són molt similars (o idèntics) i el llibre recomanat és el mateix, ens quedem amb aquell que tingui el timestamp més recent
                if similarity_users >= 0.8 and case.get_book().get_title() == case_old.get_book().get_title() :

                    # Eliminem directament l'antic ja que els casos nous sempre tindran un timestamp igual o major als ja presents al dataset
                    cases_to_delete.append(case_old)
            
            # Afegim el cas nou sempre i després esborrarem els que hagin causat redundància, si n'hi ha 
            
            """ Comencem afegint l'usuari d'aquell cas a la base de dades """

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
            self.index_tree.insertar_caso(case,user.get_user_profile())
            
            # Augmentem el nombre de casos en 1, ja que n'acabem d'afegir un
            self.number_cases += 1
            
            # Si s'ha trobat casos similars al nou cas afegit en la base de dades, els eliminarem ja que són antics
            if len(cases_to_delete)>0:

                """ Ara cal eliminar els casos amb els que ha causat redundància """
                for case_delete in cases_to_delete:
                    # L'eliminem primer del dataset 
                    row_to_delete = case_delete.to_dataframe_row()
                    index_to_delete = self.cases[self.cases.isin(row_to_delete).all(axis=1)].index
                    self.cases = self.cases.drop(index_to_delete)

                    # I seguidament de l'arbre
                    self.index_tree.eliminar_caso(case_delete,case_delete.get_user().get_user_profile())

                    self.number_cases -= 1

        """ Revisem si hi ha casos inútils per l'usuari del que han arribat els casos """
        # Casos inútils serien aquells molt antics, per exemple que superin un cert període de temps de diferència amb la data dels nous casos
        
        leaf_cases = self.index_tree.buscar_casos(user)
        user_cases = [case for case in leaf_cases if case.get_user().get_username() == user]

        # Mirarem si hi ha casos d'un usuari que superin els 4 mesos (120 dies) de diferència amb els nous casos i, si n'hi ha, els eliminarem
        for case_time in user_cases: 
            if new_timestamp - case_time.get_timestamp() > 120:
                # L'eliminem primer del dataset 
                row_to_delete = case_time.to_dataframe_row()
                index_to_delete = self.cases[self.cases.isin(row_to_delete).all(axis=1)].index
                self.cases = self.cases.drop(index_to_delete)
                
                # I seguidament de l'arbre
                self.index_tree.eliminar_caso(case_time,case_time.get_user().get_user_profile())

                self.number_cases -= 1


    def _build_index_tree(self):
        """
        Aquest métode obte les diferents variables i modalitats del perfil d'usuari.

        Retorna un arbre indexat amb tots els casos de la base de casos actual classificats.
        """
        char = {}
        for col in self.users.columns:
            if col != 'usuario':
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
        matched_attributes = {}

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
                if diff == 0:
                    matched_attributes[attr] = ele1
                weighted_disimilarity += weight*diff
                total_weight += weight*2
            else:
                if type(ele2) != list:
                    if ele1 != ele2:
                        weighted_disimilarity += weight
                    else:
                       matched_attributes[attr] = ele1 
                else:
                    if ele1 not in ele2:
                        weighted_disimilarity += weight
                    else:
                        matched_attributes[attr] = ele1 
                total_weight += weight

        # Normalizamos el resultado 
        weighted_disimilarity /= total_weight

        return 1 - weighted_disimilarity, matched_attributes
    
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
        
        user_db = {
            'Book_features':[list(case.get_book().get_book_features()) for case in user_cases],
            'Rating':[case.get_rating() for case in user_cases],
            'Timestamp':[case.get_timestamp() for case in user_cases]
        }
        df = pd.DataFrame(user_db)
        df['Normalized_Rating'] = df['Rating'].div(5)

        dict = {'contiene':{}, 'formato': {}, 'idioma': {}, 'largura_libro': {},
                   'clasificacion_edad':{}, 'compone_saga':{}, 'famoso':{}, 'peso':{},
                   'tipo_narrador':{}}
        
        timestamps_modalities = {}
        for row in range(len(df)):
            for ele in df.iloc[row]['Book_features']:
                if type(ele) == list:
                    for e in ele:
                        if e in timestamps_modalities.keys():
                            timestamps_modalities[e].append(df.iloc[row]['Timestamp'])
                        else:
                            timestamps_modalities[e] = [df.iloc[row]['Timestamp']]
                else:
                    if ele in timestamps_modalities.keys():
                            timestamps_modalities[ele].append(df.iloc[row]['Timestamp'])
                    else:
                        timestamps_modalities[ele] = [df.iloc[row]['Timestamp']]

        for key in timestamps_modalities:
            total = sum(timestamps_modalities[key])
            weights = [value/total for value in timestamps_modalities[key]]
            timestamps_modalities[key] = weights
        
        counter_modalities = {mod:0 for mod in timestamps_modalities.keys()}

        # Calcul de quines són les caracteristiques preferides a partir de sum(Combined value)/len(values) 
        for i, feature in enumerate(dict.items()):
            attr = feature[0]
            for j in range(len(df)):
                ele = df['Book_features'][j][i]                
                if type(ele) == list:
                    for e in ele:
                        counter_modalities[e] += 1
                        index = counter_modalities[e] -1
                        if e in dict[attr].keys():
                            dict[attr][e].append(timestamps_modalities[e][index]*df['Normalized_Rating'][j])
                        else:
                            dict[attr][e] = [timestamps_modalities[e][index]*df['Normalized_Rating'][j]]
                else:
                    counter_modalities[ele] += 1
                    index = counter_modalities[ele] -1
                    if ele in dict[attr].keys():
                        dict[attr][ele].append(timestamps_modalities[ele][index]*df['Normalized_Rating'][j])
                    else:
                        dict[attr][ele] = [timestamps_modalities[ele][index]*df['Normalized_Rating'][j]]

        user_preferences = []
        for key in dict:
            for feature in dict[key]:
                values = dict[key][feature]
                dict[key][feature] = sum(values)
            best = max(dict[key].items(), key=lambda item: item[1])[0]
            user_preferences.append(best)
        
        return user_preferences
    
    def _justify_recomendation(self, book_matched_attributes):
        """
        Función para justificar una recomendación basada en las preferencias del usuario.
        """
        justification = "Hemos recomendado este libro porque usuarios con características parecidas a ti lo han puntuado positivamente y porque: "
        
        # Verificar cada atributo y agregar la justificación correspondiente
        if 'contiene' in book_matched_attributes:
            justification += f" contiene el género {book_matched_attributes['contiene']},"
        
        if 'formato' in book_matched_attributes:
            justification += f" se encuentra disponible en formato {book_matched_attributes['formato']},"
        
        if 'idioma' in book_matched_attributes:
            justification += f" está escrito en {book_matched_attributes['idioma']},"

        if 'largura_libro' in book_matched_attributes:
            justification += f" tiene una longitud {book_matched_attributes['largura_libro']},"

        if 'clasificacion_edad' in book_matched_attributes:
            justification += f" pertenece a la clasificación de edad {book_matched_attributes['clasificacion_edad']},"

        if 'compone_saga' in book_matched_attributes:
            if book_matched_attributes['compone_saga'] == 'si':
                justification += " forma parte de una saga,"

        if 'famoso' in book_matched_attributes:
            if book_matched_attributes['famoso'] == 'si':
                justification += " es una obra mundialmente conocida,"

        if 'peso' in book_matched_attributes:
            justification += f" tiene un peso {book_matched_attributes['peso']},"

        if 'tipo_narrador' in book_matched_attributes:
            justification += f" está narrado desde {book_matched_attributes['tipo_narrador']}."

        justification += " "

        return justification
        
    
    def ask_user_prefs(self):
        """
        Funció per preguntar a usuaris nous les seves preferències
        """
        user_prefs_dic = {'contiene':None, 'formato': None, 'idioma': None, 'largura_libro': None,
                   'clasificacion_edad':None, 'compone_saga':None, 'famoso':None, 'peso':None,
                   'tipo_narrador':None}
        
        # Pregunta 1
        print("Vas a la librería y te encuentras estas secciones, ¿en cuál de ellas invertirías más tiempo mirando libros?")
        print("Opciones: Fantasia, Ficción Histórica, Terror, Humor, Magia, Misterio, Romance, Ciencia Ficción o Suspense")
        user_prefs_dic['contiene'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 2
        print("¿A qué clasificación de edad te gustaría que perteneciera tu libro?")
        print("Opciones: Infantil, Juvenil, Adulto")
        user_prefs_dic['clasificacion_edad'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 3
        print("¿Desde qué punto de vista quieres que se explique la historia?")
        print("Opciones: Primera persona o Tercera persona")
        user_prefs_dic['tipo_narrador'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 4
        print("¿Quieres leer un libro que pertenezca a una saga ?")
        print("Opciones: Si o No")
        user_prefs_dic['compone_saga'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 5
        print("¿Cuál consideras que debe ser la longitud ideal para tu libro?")
        print("Opciones: Corto, Normal o Largo")
        user_prefs_dic['largura_libro'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 6
        print("¿En qué formato disfrutas más un libro?")
        print("Opciones: Audiolibro, Papel o Ebook")
        user_prefs_dic['formato'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 7
        print("Teniendo en cuenta tu sitio habitual de lectura, ¿cuál es el peso del libro con el que te sentirías más cómodo/a?")
        print("Opciones: Ligero, Intermedio o Pesado")
        user_prefs_dic['peso'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 8
        print("¿En qué idioma buscas leer?")
        print("Opciones: Castellano, Inglés o Catalán")
        user_prefs_dic['idioma'] = self._procesar_input(input("Respuesta: "))

        # Pregunta 9
        print("¿Prefieres una obra mundialmente conocida?")
        print("Opciones: Si o No")
        user_prefs_dic['famoso'] = self._procesar_input(input("Respuesta: "))

        return list(user_prefs_dic.values())

    def _procesar_input(self, cadena):
            '''
            función que elimina mayusculas, tildes y espacios del input del usuario
            '''
            cadena_sin_tildes = unidecode(cadena)
            cadena_en_minusculas = cadena_sin_tildes.lower()
            cadena_con_guiones = cadena_en_minusculas.replace(' ', '_')
            return cadena_con_guiones
    
    def ask_questions(self,num_usuario):
        """
        Aquesta funció hauria de fer les preguntes necessaries per extreure:
            1. En cas que l'usuario no es trobi (preguntar username), extreure el perfil de l'usuari.
                1.1 Si l'usuari es troba a la llista d'instancies, retornar la posició a la llista.
                1.2 Si no, crear el perfil d'usuari, crear la instancia, i afegirlo al final de la llista d'instancies.
            2. Extreure les preferencies de l'usuari per aquest cas.
        
        Retorna una instancia de CASE on només tenim el perfil d'usuari i les seves preferencies: Case(self.number_cases + 1, User_instance, Diccionari d'atributs)
        """

        
        # pregunta 1
        print("¿Cuál es tu género? ")
        print("Opciones: Hombre, Mujer o Prefiero no decirlo")
        genero = self._procesar_input(input("Respuesta: "))
        
        # pregunta 2
        n = int(input("Introduzca su edad "))
        if n > 25:
            edad = 'adulto'
        else:
            edad = 'joven'
                    
        # pregunta 3
        print("¿A qué clase social perteneces? ")
        print("Opciones: Alta, Media o Baja")
        clase_social = self._procesar_input(input("Respuesta: "))
        
        # pregunta 4
        print("¿Cuál es tu situación laboral alctual? ")
        print("Opciones: Trabajador, Estudiante, Jubilado o Nada")
        trabajo = self._procesar_input(input("Respuesta: "))
        
        # pregunta 5
        h = int(input("¿Cuántas horas le dedicas a la lectura a la semana? "))
        if h > 13:
            horas_lectura = 'muchas'
        elif n > 5:
            horas_lectura = 'normal'
        else: 
            horas_lectura = 'pocas'
            
        # pregunta 6
        print("¿Qué tipo de música escuchas? ")
        print("Opciones: Reggeatón, Techno, Pop, Cláscia, Rap, Heavy Metal")
        musica = self._procesar_input(input("Respuesta: "))
        
        # pregunta 7
        print("¿Dónde irías una tarde libre? ")
        print("Opciones: Bar, Playa, Montaña o Sofá")
        tarde = self._procesar_input(input("Respuesta: "))
        if tarde == "montana":
            tarde = "montaña"
        
        # pregunta 8
        print("¿Qué tipo de vacaciones te gusta más? ")
        print("Opciones: Aventura, Moderno o Clásico")
        vacaciones = self._procesar_input(input("Respuesta: "))
        
        dicc = [{"genero": genero, "edad": edad, "clase_social": clase_social, "trabajo": trabajo, "horas_lectura_a_la_semana": horas_lectura, "musica": musica, "tarde_libre": tarde, "vacaciones": vacaciones}]
        prof = pd.DataFrame(dicc)
        instance = User(num_usuario, prof.loc[0])
        print(instance.get_user_profile())
        new_case = Case(self.number_cases,instance)



        return new_case
    
    def inici_usuari(self):

        print('Bienvenido al recomendador de libros Bicho3, ahora somos 4!')
        r = input("Te has registrado anteriormente? (Si/No)").lower()
        if r == "si":
            num_usuario = float("inf")
            while num_usuario not in range(0,len(self.users_inst)):
                try:
                    num_usuario = int(input("Introduzca su número de usuario: "))
                except ValueError:
                    print("Usuario no encontrado en la base de datos. Porfavor introduzca su número de usuario: ")
            a = input("Quieres contarnos cuáles son tus preferencias? O prefieres que las infiramos en función de tu historial? Opciones: 1,2")
            if a == "1":
                print('Ahora queremos saber qué caracterísitcas quieres que contenga el libro que estás buscando:')
                prefs =  self.ask_user_prefs()
            else:
                prefs = None
            return Case(self.number_cases,self.users_inst[num_usuario],prefs)
                    
        else:
            num_usuario = len(self.users_inst)
            print(f'Sú número de usuario és el siguiente: {num_usuario}')
            print('Para recomendarte el mejor libro, primero debemos saber un poco más de tí.')
            new_case = self.ask_questions(num_usuario)
            print('Ahora queremos saber qué caracterísitcas quieres que contenga el libro que estás buscando:')
            prefs =  self.ask_user_prefs()
            new_case.set_atributes(prefs)
            return new_case
    def save_databases(self):
        self.cases.to_csv('df_casos_new', index=False)
        self.users.to_csv('df_users_new', index=False)
    
