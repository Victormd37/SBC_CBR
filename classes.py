import pandas as pd

class User():
    def __init__(self, user_id, user_profile):
        self.user_id = user_id
        self.user_profile = user_profile
    
    def get_username(self):

        return self.user_id
    
    def get_user_profile(self):
        '''
        Devuelve una lista con los atributos del perfil del usuario.
        '''
        return self.user_profile
    
    def to_dataframe_row(self):
        """
        Transforma la instancia de User a una fila de DataFrame para la base de datos de usuarios.
        """
        user_data = {
            'usuario': [self.get_username()],
            'genero': [self.get_user_profile()[0]],
            'edad': [self.get_user_profile()[1]],
            'clase_social': [self.get_user_profile()[2]],
            'trabajo': [self.get_user_profile()[3]],
            'horas_lectura': [self.get_user_profile()[4]],
            'musica': [self.get_user_profile()[5]],
            'tarde_libre': [self.get_user_profile()[6]],
            'vacaciones': [self.get_user_profile()[7]]
        }

        new_user = pd.DataFrame(user_data)
        return new_user

class Book():
    def __init__(self, book_id, book_title, book_features):
        self.book_id = book_id
        self.book_title = book_title
        self.book_features = book_features
    
    def get_book_features(self):
        return self.book_features
    
    def get_book_id(self):
        return self.book_id
    
    def get_title(self):
        return self.book_title
    

class Case():
    # 3 first inputs are lists
    def __init__(self,case_id, user_instance, atributes_pref=None, book_instance = None, rating = None, drift_value = None, timestamp = None):
        self.case_id = case_id
        self.user = user_instance
        self.atributes_pref = atributes_pref
        self.book = book_instance
        self.rating = rating
        self.drift_value = drift_value
        self.timestamp = timestamp 
    
    def get_user(self):
        '''
        Devuelve una lista con los atributos del perfil del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.user

    def get_caseid(self):
        '''
        Devuelve una lista con los atributos del perfil del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.case_id
    
    def get_book(self):
        '''
        Devuelve una lista con los atributos del perfil del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.book

    def get_user_preferences(self):
        '''
        Devuelve una lista con los atributos de las preferencias del usuario.
        Los atributos multislot seran sublistas.
        '''
        return self.atributes_pref
    
    def get_timestamp(self):
        '''
        Devuelve el timestamp cuando se hizo la valoración
        '''
        return self.timestamp

    def get_rating(self):
        return self.rating
    
    def set_book(self, book_inst):
        '''
        Permite añadir un libro al caso como solución
        '''
        self.book = book_inst

    def set_atributes(self, atr):
        '''
        Permite añadir las preferencias del usuario
        '''
        self.atributes_pref = atr

    def to_dataframe_row(self):
            """
            Transforma la instancia de User a una fila de DataFrame para la base de datos de usuarios.
            """
            # si user es llista fer [0], si es instància així 
            pref = self.get_user_preferences()
            case_data = {
                'usuario': [self.get_user().get_username()],
                'contiene': [pref[0]],
                'formato': [pref[1]],
                'idioma': [pref[2]],
                'largura_libro': [pref[3]],
                'clasificacion_edad': [pref[4]],
                'compone_saga': [pref[5]],
                'famoso': [pref[6]],
                'peso': [pref[7]],
                'tipo_narrador':[pref[8]],
                'libro': [self.get_book().get_book_id()],
                'valoracion': [self.get_rating()],
                'timestep': [self.get_timestamp()]
            }

            new_case = pd.DataFrame(case_data)
            return new_case 

    