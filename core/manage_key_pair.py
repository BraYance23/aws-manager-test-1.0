import boto3
from botocore.exceptions import ClientError,NoCredentialsError
from pathlib import Path
import logging


logger = logging.getLogger(__name__)

class ManageKeyPairs:

    def __init__(self,region_name = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name = self.region_name)


    def request_key_pairs(self)-> tuple[bool,dict | str]:

        try:
            response = self.ec2.describe_key_pairs()
            return True,response
            
        except ClientError as e:
            code = e.response["Error"]["Code"]
            return False,code
        
        except NoCredentialsError:
            return False,"No se encontraron credenciales"
      
    def prepare_data(self,response:dict)-> tuple[dict,list]:
        
        filas_tabulate = []
        dict_key_id = {}

        for indice,key in enumerate(response["KeyPairs"],start=1):

            fecha = key.get("CreateTime")
            fecha_formateada = fecha.strftime("%Y/%m/%d %H:%M:%S")

            dict_key_id[str(indice)] = key.get("KeyName",None)

            filas_tabulate.append([
                indice,
                key.get("KeyName","Sin llave"),
                key.get("KeyPairId",None),
                fecha_formateada
            ])
    
        return dict_key_id,filas_tabulate

    def generate_key_pair(self, key_name:str)-> tuple[bool,str]:

        try:
            response = self.ec2.create_key_pair(KeyName=key_name)
            private_key = response["KeyMaterial"]

            return True,private_key
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            return False,code

        except NoCredentialsError as error:
            return False,"No se encontraron credenciales"
            
    def request_name_key(self)-> str:

        while True:
        
            name_key = input("Ingre el nombre de la llave que desea crear : ").strip()

            if name_key:
                return name_key
            
            print("No se puede crear una llave sin nombre")
            
    def save_key_pair(self,private_key:str,key_name:str)-> tuple[bool,Path | str]:

        try:
            key_path = Path.home()/".ssh"/f"{key_name}.pem"
            key_path.parent.mkdir(parents=True,exist_ok=True)
            key_path.write_text(private_key)
            key_path.chmod(0o600)
            return True,key_path

        except Exception as error:
            return False,"ErrorSaveKey"

    def delete_key_pair(self,key_delete:str)-> tuple[bool,str]:

        try:
            self.ec2.delete_key_pair(KeyName=key_delete)
            return True,key_delete

        except ClientError as error:
            code = error.response["Error"]["Code"]
            return False,code
        
        except NoCredentialsError:
            return False,"No se encontraron credenciales"


if __name__ == "__main__":
    pass