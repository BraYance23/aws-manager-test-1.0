import boto3
from botocore.exceptions import ClientError,NoCredentialsError
import logging


logger = logging.getLogger(__name__)

class ManageSecurityGroup:
    
    def __init__(self,region_name:str = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name=region_name)
        self.sg_id = None
 
    def get_rules_sg(self,sg_id:str = "")-> tuple[bool,dict | str]:

        try:
            response = self.ec2.describe_security_groups(
                GroupIds=[sg_id]
            )
            return True,response
        

        except ClientError as e:
            code = e.response["Error"]["Code"]
            return False,code

        except NoCredentialsError:
            return False,"No se encontraron credenciales"


    def formata_data_sg_rules(self,response:dict)-> tuple[list,dict]:

        filas_tabulate = []
        dict_rules_sg = {}

        for securiry in response["SecurityGroups"]:

      
            for indice,rule in enumerate(securiry["IpPermissions"],start=1):
         
                    for ip_ranges in rule["IpRanges"]:

                        dict_rules_sg[str(indice)] = {

                            "IpProtocol":rule.get("IpProtocol","N/A."),
                            "FromPort": rule.get("FromPort",-1),
                            "ToPort": rule.get("ToPort",-1),
                            "IpRanges": [{"CidrIp" : ip_ranges.get("CidrIp","Sin CidrIp."),
                                        "Description": ip_ranges.get("Description","Sin descipcion.")}]
                                        }
                                
                        filas_tabulate.append([indice,
                                        rule.get("IpProtocol","Sin protocolo").upper(),
                                        rule.get("FromPort",-1),
                                        rule.get("ToPort",-1),
                                        ip_ranges.get("CidrIp","Sin CidrIp"),
                                        ip_ranges.get("Description","Sin descripción")
                                        ])
        return filas_tabulate,dict_rules_sg

    def format_data_sg_general(self,response:dict)-> tuple[list,dict]:

        dict_sg_id = {}
        filas_tabulate = []

        for indice,valor in enumerate(response["SecurityGroups"],start=1):

            filas_tabulate.append([
                indice,
                valor.get("GroupId"),
                valor.get("Description")
            ])
            dict_sg_id[str(indice)] = valor.get("GroupId")
        
        return filas_tabulate,dict_sg_id


    def authorize_rule_ingress(self,ip_permissions:list)-> tuple[bool,str]:

        
        try:
            self.ec2.authorize_security_group_ingress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return True,ip_permissions

        except ClientError as error:
            code = error.response["Error"]["Code"]
            return False,code

        except NoCredentialsError:
            return False,"No se encontraron credenciales"
    
    def remove_rule_ingress(self,ip_permissions:list)-> tuple[bool,dict | str]:

        
        try:
            for valor in ip_permissions["IpRanges"]:
                del valor["Description"]        
                
            self.ec2.revoke_security_group_ingress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
                        )
            return True,ip_permissions
                     
        except ClientError as error:
            code = error.response['Error']['Code']
            return False,code
        
        except NoCredentialsError:
            return False,"No se encontraron credenciales"
    
if __name__ == "__main__":
    pass