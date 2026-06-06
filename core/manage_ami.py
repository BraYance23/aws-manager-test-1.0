import boto3
from datetime import datetime
from botocore.exceptions import ClientError,NoCredentialsError
from data import data_ec2
import logging


class ManageAmi:
  
    def __init__(self,region_name = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name=self.region_name)
    
    def get_ami_id(self,owner:str,filter:str):
  
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
            logging.error(f"Error al intentar describir AMIS : {code}")
            return False,code

        except NoCredentialsError:
            logging.error("No se encontradron credenciales de AWS.")
            return False,"No se encontraron credenciales"

    def prepare_data_ami(self,data_ami):

        filas_tabulate = []
        dict_id_ami = {}

        for indice,image in enumerate(data_ami["Images"],start=1):
                
            if image["State"] == "available":
                
                fecha = image.get("CreationDate")
                fecha_formateada = datetime.strptime(fecha,"%Y-%m-%dT%H:%M:%S.%fZ")
                    
                filas_tabulate.append(
                    [indice,
                    image.get("ImageId"),
                    image.get("Name"),
                    image.get("Architecture"),
                    image.get("FreeTierEligible"),
                    fecha_formateada
                    ]
                    )
                dict_id_ami[str(indice)] = image.get("ImageId")
                    
        return filas_tabulate,dict_id_ami
      
    def get_name_ami_and_owner(self,name,version):

        owner = data_ec2.DISTROS[name][version]["owner"]
        filter = data_ec2.DISTROS[name][version]["filter"]
        return owner,filter
       
    def formate_data_selected_os(self,election):

        dict_distro = {}
        filas_tabulate = []
         
        for indice,valor in enumerate(data_ec2.VERSION_OS[election],start=1):
            filas_tabulate.append([indice,
                                  valor,
                                  "x86",
                                  "Canonical"
                                  ])
            dict_distro[str(indice)] = valor
            
        return filas_tabulate,dict_distro
    

if __name__ == "__main__":
    pass