import boto3
from botocore.exceptions import ClientError,NoCredentialsError
import logging




logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s - %(levelname)s - %(message)s')

class ManageEc2:


    def __init__(self,region_name = "us-east-1"):
        self.region_name = region_name
        try:
            self.ec2 = boto3.client("ec2",region_name = self.region_name)
        except NoCredentialsError:
            logging.error("No se encontraron credenciales de AWS.")
            print("No se encontraron las credenciales de AWS. Configura tu ~/.aws/credentials")
            return

    def describe_ec2(self)-> bool|str:

        try:
    
            response = self.ec2.describe_instances()
            return True,response

        except ClientError as e:

            code = e.response["Error"]["Code"]
            logging.error(f"Hubo un error al intentar describir una instancia : {code}")
            return False,code

        except NoCredentialsError:
            logging.error(f"No se encontraron las crendenciales de AWS.")
            return False,"No se encontraron credenciales"

    def verify_identity(self)-> bool|str:
        """
        Creamos cliente de STS para validar credenciales, antes de ejecutar
        metodos que llaman a la API de AWS.
        """

        try:
            sts = boto3.client("sts")

            response = sts.get_caller_identity()

            return True,response

        except NoCredentialsError:
            return False,"No se encontraron credenciales de AWS"

        except ClientError as e:
            return False, e

    def run_ec2(self,config:dict):

        machine_type = config.get("TypeMachine")
        ami_id = config.get("AmiId")
        name_instance = config.get("NameInstance")
        key_pair_name = config.get("KeyPairName")
        sg_id = config.get("SecurityGroupsId")
        min_count = config.get("MinCount")
        max_count = config.get("MaxCount")

        try:

            response = self.ec2.run_instances(
                ImageId = ami_id,
                InstanceType = machine_type,
                MinCount = min_count,
                MaxCount = max_count,
                KeyName = key_pair_name,
                SecurityGroupIds = [sg_id],
                TagSpecifications = [
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": name_instance}]
                    }
                ]
            )

            return True,response.get("Instances")[0].get("InstanceId")

        except ClientError as e:
            code = e.response["Error"]["Code"]
            logging.error(f"Error al intentar lanzar una instancia : {code}")
            return False,code
        
        except NoCredentialsError:
            logging.error("No se encontraron credendiales de AWS.")
            return False,"No se encontraron credenciales"
        

    def init_ec2(self,instance_id):

        try:

            self.ec2.start_instances(InstanceIds=[instance_id])
            return True,instance_id
           
        except ClientError  as e:
            code = e.response["Error"]["Code"]

            logging.error(f"Hubo un error al intentar iniciar la instancia. {code}")
        
            return False,code
        
        except NoCredentialsError:
            return False,"No se encontraron credenciales"

    def reboot_ec2(self,instance_id):

        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id])
            return True,instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]

            logging.error(f"Hubo un error al intentar reiniciar la instancia : {code}")

            return False,code

        except NoCredentialsError:
            logging.error("Error en validacion de credenciales AWS.")

            return False,"No se encontraron credenciales"
        
             
    def stop_ec2(self,instance_id):

        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return True,instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]

            logging.error(f"Hubo error al intentar detener una instancia : {code}")
            return False,code

        except NoCredentialsError:
            logging.error("Error en validacion de credenciales AWS.")
            return False,"No se encontraron credenciales"

    def terminate_ec2(self,instance_id):

        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            return True,instance_id

        except ClientError as e:
            code = e.response["Error"]["Code"]

            logging.error(f"Hubo un error al intentar detener una instancia : {code}")
            return False,code

        except NoCredentialsError:
            logging.error("No se encontraron credenciales de AWS.")
            return False,"No se encontraron credenciales"

    def format_data_ec2(self,response):

        filas_tabulate = []
        dict_id_ec2 = {}
        
        for indice,reservation in enumerate(response["Reservations"],start=1):

            for instance in reservation["Instances"]:

                dict_id_ec2[str(indice)] = (instance.get("InstanceId"))
                fecha = instance.get("LaunchTime")
                fecha_formateada = fecha.strftime("%Y/%m/%d %H:%M:%S")
                                                
                nombre = "Sin nombre"
                for tag in instance.get("Tags",[]):

                    if tag.get("Key") == "Name":
                        nombre = tag.get("Value","Sin Nombre")
                        break

            filas_tabulate.append([indice,
                                   nombre,
                                   instance.get("InstanceType"),
                                   instance["State"].get("Name"),
                         instance.get("Architecture"),instance.get("InstanceId"),
                         instance.get("PublicIpAddress","Sin ip publica"),
                         fecha_formateada
                         ])
        return dict_id_ec2,filas_tabulate


    def preparative(self):

        flag,code = self.describe_ec2()

        if not flag:
            return flag,code

        return self.format_data_ec2(code)
        
        

    def waiter_for_state(self,instance_id,target_state):
     
        waiter = self.ec2.get_waiter(f"instance_{target_state}")
        waiter.wait(InstanceIds=[instance_id])
        return True
             
    
if __name__ == "__main__":
    pass
    
