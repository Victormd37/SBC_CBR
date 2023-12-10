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
        Los atributos multislot seran sublistas.
        '''
        return self.user_profile
    
    def to_dataframe_row(self):
        """
        Transforma la instancia de User a una fila de DataFrame para la base de datos de usuarios.
        """
        user_data = {
            'Usuario': [self.get_username()],
            'Genero': [self.get_user_profile()[0]],
            'Edad': [self.get_user_profile()[1]],
            'Clase social': [self.get_user_profile()[2]],
            'Trabajo': [self.get_user_profile()[3]],
            'Horas lectura': [self.get_user_profile()[4]],
            'Musica': [self.get_user_profile()[5]],
            'Tarde libre': [self.get_user_profile()[6]],
            'Vacaciones': [self.get_user_profile()[7]]
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
    

class Case():
    # 3 first inputs are lists
    def __init__(self,case_id, user_instance, atributes_pref, book_instance = None, purchased = None, rating = None, drift_value = None, timestamp = None):
        self.case_id = case_id
        self.user = user_instance
        self.atributes_pref = atributes_pref
        self.book = book_instance
        self.rating = rating
        self.purchased = purchased
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
        Devuelve el timestamp en formato Unix: seconds that have elapsed since January 1, 1970 
        '''
        return self.timestamp

    def get_rating(self):
        return self.rating
    
    def set_book(self, book_inst):
        '''
        Permite añadir un libro al caso como solución
        '''
        self.book = book_inst

    def to_dataframe_row(self):
            """
            Transforma la instancia de User a una fila de DataFrame para la base de datos de usuarios.
            """
            # si user es llista fer [0], si es instància així 
            case_data = {
                'Usuario': [self.get_user().get_username()],
                'Contiene': [self.get_user_preferences()[0]],
                'Formato': [self.get_user_preferences()[1]],
                'Idioma': [self.get_user_preferences()[2]],
                'Largura_libro': [self.get_user_preferences()[3]],
                'Clasificacion_edad': [self.get_user_preferences()[4]],
                'Compone_saga': [self.get_user_preferences()[5]],
                'Famoso': [self.get_user_preferences()[6]],
                'Peso': [self.get_user_preferences()[7]],
                'Tipo_narrador':[self.get_user_preferences()[8]],
                'Libro': [self.get_book()],
                'Valoracion': [self.get_rating()],
                'Timestamp': [self.get_timestamp()]
            }

            new_case = pd.DataFrame(case_data)
            return new_case 

    