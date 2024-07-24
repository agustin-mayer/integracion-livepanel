from Livepanel_SDK import LivepanelAuth, APIAccess
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    def get_livepanel_API_access():
        livepanel_API_key = os.getenv('LIVEPANEL_API_KEY')
        auth = LivepanelAuth(livepanel_API_key)
        livepanel_API_access = APIAccess(auth)
        return livepanel_API_access
    
    livpeanel_API_access = get_livepanel_API_access()
    response = livpeanel_API_access.get_projects()
    print(f"Respuesta {response}")
    

if __name__ == "__main__":
    main()