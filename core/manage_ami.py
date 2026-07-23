import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError,NoCredentialsError
from data import data_ec2


logger = logging.getLogger(__name__)


class ManageAmi:
  
    def __init__(self,region_name = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name=self.region_name)
    
    def get_ami_id(self,owner:str,filter:str)-> tuple[bool,dict | str]:
  
        try:
            response = self.ec2.describe_images(
            Owners=[owner],
            Filters=[
                    {"Name": "name", "Values": [filter]},
                    {"Name": "state", "Values": ["available"]},
                    {"Name": "architecture", "Values": ["x86_64"]}
                ]
            )

            return True,response
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            return False,code

        except NoCredentialsError:
            return False,"No se encontraron credenciales"

    def prepare_data_ami(self,data_ami:dict)-> tuple[list,dict]:

        list_rows = []
        dict_id_ami = {}

        for indice,image in enumerate(data_ami["Images"],start=1):
                
            if image["State"] == "available":
                
                fecha = image.get("CreationDate")
                fecha_formateada = str(datetime.strptime(fecha,"%Y-%m-%dT%H:%M:%S.%fZ"))
                    
                list_rows.append(
                    [str(indice),
                    image.get("ImageId"),
                    image.get("Name"),
                    image.get("Architecture"),
                    str(image.get("FreeTierEligible")),
                    fecha_formateada
                    ]
                    )
                dict_id_ami[str(indice)] = image.get("ImageId")
                    
        return list_rows,dict_id_ami
         
    def formate_data_selected_os(self,election:str)-> tuple[list,dict]:

        dict_distro = {}
        list_rows = []
         
        for indice,valor in enumerate(data_ec2.VERSION_OS[election],start=1):
            list_rows.append([str(indice),
                                  valor,
                                  "x86_64",
                                  "AMAZON"
                                  ])
            dict_distro[str(indice)] = valor
            
        return list_rows,dict_distro
    

if __name__ == "__main__":
    pass