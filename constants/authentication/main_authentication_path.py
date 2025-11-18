from constants.authentication.authentication_path import AuthenticationPath

class MainAuthenticationPath(AuthenticationPath):

    def __init__(self):
        self.__token_filename: str = "token.json"
        self.__credentials_filename: str = "credentials.json"
        self.__data_dir: str = "data"
        self.__authentication_data_dir: str = "authentication"

    @property
    def token_filename(self) -> str:
        return self.__token_filename
    
    @property
    def credentials_filename(self) -> str:
        return self.__credentials_filename
    
    @property
    def data_dir(self) -> str:
        return self.__data_dir
    
    @property
    def authentication_data_dir(self) -> str:
        return self.__authentication_data_dir
    