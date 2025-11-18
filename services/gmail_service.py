import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailService:
    
    def __init__(
            self,
            scopes: list[str],
            authentication_data_dir: str,
            service_version: str = "v1",
            ) -> None:
        
        self.credentials: Credentials | None = None
        self.scopes: list[str] = scopes
        self.token_filename: str = "token.json"
        self.credentials_filename: str = "credentials.json"
        self.authentication_data_dir: str = authentication_data_dir
        self.service_name: str = "gmail"
        self.service_version: str = service_version
        self.service = None

        self.build_service()

    @property
    def token_filepath(self):
        return os.path.join(self.authentication_data_dir, self.token_filename)
    
    @property
    def credentials_filepath(self):
        return os.path.join(self.authentication_data_dir, self.credentials_filename)

    def get_credentials(self) -> None:

        if os.path.exists(self.token_filepath):
            
            self.credentials = Credentials.from_authorized_user_file(
                filename=self.token_filepath,
                scopes=self.scopes
                )
        
        if not self.credentials or not self.credentials.valid:
            
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                
                self.credentials.refresh(Request())
            
            else:
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=self.credentials_filepath,
                    scopes=self.scopes
                    )

                self.credentials = flow.run_local_server(port=0)

            with open(file=self.token_filepath, mode="w") as token:
                token.write(self.credentials.to_json())

    def build_service(self) -> None:
        
        try:
            self.get_credentials()

            if self.service:
                return

            self.service = build(
                serviceName=self.service_name,
                version=self.service_version,
                credentials=self.credentials)
        
        except HttpError as error:
            print(f"An error occurred: {error}")
 




        
