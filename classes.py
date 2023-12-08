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

    