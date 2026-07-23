import boto3
from botocore.exceptions import ClientError,NoCredentialsError
import logging
from schemas import DictFormatSGRules


logger = logging.getLogger(__name__)

class ManageSecurityGroup:
    
    def __init__(self,region_name:str = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name=region_name)
        self.sg_id = None
 
    def get_rules_sg(self,sg_id:str | None = "")-> tuple[bool,dict | str]:

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

    def formata_data_sg_rules(self,response:dict)-> DictFormatSGRules:

        list_rows_ingress = []
        list_rows_egress = []
        dict_rules_ingress = {}
        dict_rules_egress = {}

        for security in response["SecurityGroups"]:
                
            for indice,rule in enumerate(security["IpPermissions"],start=1):
         
                for ip_ranges in rule["IpRanges"]:

                    dict_rules_ingress[str(indice)] = {

                        "IpProtocol":rule.get("IpProtocol","N/A."),
                        "FromPort": rule.get("FromPort",-1),
                        "ToPort": rule.get("ToPort",-1),
                        "IpRanges": [{"CidrIp" : ip_ranges.get("CidrIp","Sin CidrIp."),
                                    "Description": ip_ranges.get("Description","Sin descipcion.")}]
                                    }
                            
                    list_rows_ingress.append([str(indice),
                                    rule.get("IpProtocol","Sin protocolo").upper(),
                                    str(rule.get("FromPort","ALL")),
                                    str(rule.get("ToPort","ALL")),
                                    ip_ranges.get("CidrIp","Sin CidrIp"),
                                    ip_ranges.get("Description","Sin descripción")
                                    ])
                    
            for indice,rule_egress in enumerate(security["IpPermissionsEgress"],start=1):

                 for ip_ranges_egress in rule_egress["IpRanges"]:

                        dict_rules_egress[str(indice)] = {

                            "IpProtocol":rule_egress.get("IpProtocol","N/A."),
                            "FromPort": rule_egress.get("FromPort","ALL"),
                            "ToPort": rule_egress.get("ToPort","ALL"),
                            "IpRanges": [{"CidrIp" : ip_ranges_egress.get("CidrIp","Sin CidrIp."),
                                        "Description": ip_ranges_egress.get("Description","Sin descipcion.")}]
                                        }
                        
                        list_rows_egress.append([str(indice),
                                        rule_egress.get("IpProtocol","Sin protocolo").upper(),
                                        str(rule_egress.get("FromPort","ALL")),
                                        str(rule_egress.get("ToPort","ALL")),
                                        ip_ranges_egress.get("CidrIp","Sin CidrIp"),
                                        ip_ranges_egress.get("Description","Sin descripción")
                                        ])


        return {
            "list_rows_ingress": list_rows_ingress,
            "list_rows_egress": list_rows_egress,
            "dict_rules_ingress": dict_rules_ingress,
            "dict_rules_egress": dict_rules_egress
            }

    def format_data_sg_general(self,response:dict)-> tuple[list,dict]:

        dict_sg_id = {}
        list_rows = []

        for indice,valor in enumerate(response["SecurityGroups"],start=1):

            list_rows.append([
                str(indice),
                valor.get("GroupId"),
                valor.get("Description")
            ])
            dict_sg_id[str(indice)] = valor.get("GroupId")
        
        return list_rows,dict_sg_id

    def authorize_rule_ingress(self,ip_permissions:dict)-> tuple[bool,dict | str]:

        
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
          
    def remove_rule_ingress(self,ip_permissions:dict)-> tuple[bool,dict | str]:

        
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

    def authorize_rule_egress(self,ip_permissions:dict)-> tuple[bool,dict | str]:
    
        try:
            self.ec2.authorize_security_group_egress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return True,ip_permissions

        except ClientError as error:
            code = error.response["Error"]["Code"]
            return False,code

        except NoCredentialsError:
            return False,"No se encontraron credenciales"
            
    def remove_rule_egress(self,ip_permissions:dict)-> tuple[bool,dict | str]:

        try:
            for valor in ip_permissions["IpRanges"]:
                del valor["Description"]        
                
            self.ec2.revoke_security_group_egress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
                        )
            return True,ip_permissions
                        
        except ClientError as error:
            code = error.response['Error']['Code']
            return False,code
        
        except NoCredentialsError:
            return False,"No se encontraron credenciales"
    
    def summary_sg(self):

        sg_total = 0
        flag_response,response = self.get_rules_sg()
        if not flag_response:
            return sg_total

        list_sg = response["SecurityGroups"]
        return len(list_sg)
            

if __name__ == "__main__":
    pass