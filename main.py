import json
import time
import logging
from config import logging_config
from colorama import init,Style,Fore
from core.manage_key_pair import ManageKeyPairs
from core.manage_sg import ManageSecurityGroup
from core.manage_ami import ManageAmi
from core.manage_ec2 import ManageEc2
from controllers import menu_services
from data import data_ec2
from ui import helpers


logging_config.setup_logging()
logger = logging.getLogger(__name__)

class ManagerAWS:

    def __init__(self,region_name:str="us-east-1"):
        self.region_name = region_name
        self.ADMIN_EC2 = ManageEc2(self.region_name)
        self.ADMIN_AMI = ManageAmi(self.region_name)
        self.ADMIN_KEY = ManageKeyPairs(self.region_name)
        self.ADMIN_SG = ManageSecurityGroup(self.region_name)

#Instancias:

    def run_ec2(self):
        
        config_instace = self.request_date_run_instance()
        flag,code = self.ADMIN_EC2.run_ec2(config_instace)

        if not flag:
            helpers.handle_aws_error(code)
            logger.error(f"Error al lanzar instancia : {code}")
            return

        logger.info(f"EC2 desplegado correctamente, ID : {code}")
        print(Fore.CYAN + Style.BRIGHT + "-Desplegando instancia...")
        self.ADMIN_EC2.waiter_for_state(code,"running")
        print("instancia desplegada correctamente.🚀" + Style.RESET_ALL)
        
    def operation_ec2(self,selection):

        flag_describe_ec2,response = self.ADMIN_EC2.describe_ec2()
        if not flag_describe_ec2:
            helpers.handle_aws_error(response)
            return

        dict_id_ec2,filas_tabulate = self.ADMIN_EC2.format_data_ec2(response)
        if not filas_tabulate:
            print("No hay instancias existentes en esta region.")
            return
        
        self.show_instances()
        instance_id = helpers.choice(dict_id_ec2)

        mensaje_init,waiter,mensaje_fin = data_ec2.pameter_operation_ec2[selection]
        if waiter == "terminated" and  not helpers.confirmation():
            print(Fore.YELLOW + "Operacion cancelada por el usuario" + Style.RESET_ALL)
            return

        metodos_ec2 = {
            "3": self.ADMIN_EC2.init_ec2,
            "4": self.ADMIN_EC2.reboot_ec2,
            "5": self.ADMIN_EC2.stop_ec2,
            "6": self.ADMIN_EC2.terminate_ec2
            }

        flag,code = metodos_ec2[selection](instance_id)
        if not flag:
            helpers.handle_aws_error(code)
            return
        
        print(Style.BRIGHT +  mensaje_init + Style.RESET_ALL)
        self.ADMIN_EC2.waiter_for_state(instance_id,waiter)
        print(Fore.GREEN + mensaje_fin + Style.RESET_ALL)
                 
    def show_instances(self):

        flag_response,response = self.ADMIN_EC2.describe_ec2()

        if not flag_response:
            helpers.handle_aws_error(response)
            return
        
        dict_ec2_id,filas_tabulate = self.ADMIN_EC2.format_data_ec2(response)

        if not filas_tabulate:
            print("No hay instancias existentes en esta region.")
            return
        header = data_ec2.header_ec2["header"]
        title = data_ec2.header_ec2["title"]

        helpers.display_table(filas_tabulate,header,title)
        logger.info("EC2 listadas correctamente.")

#Security Groups

    def inject_sg_id(self):

        flag,response_or_code = self.ADMIN_SG.get_rules_sg()

        if not flag:
            helpers.handle_aws_error(response_or_code)
            return

        filas_tabulate,dict_sg_id = self.ADMIN_SG.format_data_sg_general(response_or_code)

        header = data_ec2.header_sg["header"]
        title = data_ec2.header_sg["title"]

        helpers.display_table(filas_tabulate,header,title)
        
        return helpers.choice(dict_sg_id)
            
    def show_rules_sg(self):


        flag,response_or_code = self.ADMIN_SG.get_rules_sg(self.ADMIN_SG.sg_id)

        if not flag:
            helpers.handle_aws_error(response_or_code)
            return

        filas_tabulate,dict_rules = self.ADMIN_SG.formata_data_sg_rules(response_or_code)

        if not filas_tabulate:
            print("No existen reglas de entrada")
            return

        header = data_ec2.header_rules_sg["header"]
        title = data_ec2.header_rules_sg["title"]
        helpers.display_table(filas_tabulate,header,title)
          
    def autorize_sg_ingress(self):

        ip_public = helpers.get_ip_public()

        ip_permissions = helpers.request_ip_permissions(ip_public)

        if not  ip_permissions:
            print("Operacion cancelada")
            return

        flag,code_or_rule = self.ADMIN_SG.authorize_rule_ingress(ip_permissions)

        if not flag:
                  helpers.handle_aws_error(code_or_rule)
                  logger.error(f"Fallo  autorize_ingress | SG ID : {self.ADMIN_SG.sg_id} | CODE : {code_or_rule}")
                  return

        format_ip_permissions = json.dumps(ip_permissions,indent=2,default=str)   
        print(Fore.GREEN + f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.ADMIN_SG.sg_id}" + Style.RESET_ALL)
        logger.info(f"Autorize_ingress en SG ID: {self.ADMIN_SG.sg_id}\nRegla : {format_ip_permissions}")
        input("Presione enter para listar las reglas actualizadas.")
        self.show_rules_sg()
                
    def revoke_sg_ingress(self):

        flag_get_rules,response_or_code = self.ADMIN_SG.get_rules_sg(self.ADMIN_SG.sg_id)
        
        if not flag_get_rules:
            helpers.handle_aws_error(response_or_code)
            return
            
        filas_tabulate,dict_rules = self.ADMIN_SG.formata_data_sg_rules(response_or_code)
        self.show_rules_sg()

        if not dict_rules:
            print("No hay reglas existentes.")
            return

        selected_rule = helpers.choice(dict_rules)
        confirmation = helpers.confirmation()

        if not confirmation:
            print("Operacion cancelada")
            return
        flag_rules_ingress,code_or_rule = self.ADMIN_SG.remove_rule_ingress(selected_rule)

        if not flag_rules_ingress:
                helpers.handle_aws_error(code_or_rule)
                logger.error(f"Fallo en revoke_ingress | SG ID : {self.ADMIN_SG.sg_id} | CODE : {code_or_rule}")
                return

        format_ip_permissions = json.dumps(selected_rule,indent=2,default=2)
        logger.info(f"Revoke ingress en SG ID : {self.ADMIN_SG.sg_id}\nRegla : {format_ip_permissions}")
        print(Fore.GREEN +f"Puerto : {code_or_rule['ToPort']} eliminado con exito de : {self.ADMIN_SG.sg_id}" + Style.RESET_ALL)

    def change_sg_id(self):

        self.ADMIN_SG.sg_id = self.inject_sg_id()

#Key Pairs

    def show_key_pairs(self):

        flag,response_or_code = self.ADMIN_KEY.request_key_pairs()

        if not flag:
            helpers.handle_aws_error(response_or_code)
            return

        dict_id_key,filas_tabulate = self.ADMIN_KEY.format_data(response_or_code)
        if not filas_tabulate:
            print(f"No hay llaves SSH en esta region : {self.region_name}")
            return

        header = data_ec2.header_key_pair["header"]
        title = data_ec2.header_key_pair["title"]
        helpers.display_table(filas_tabulate,header,title)

    def select_key_pair(self):

        flag,response = self.ADMIN_KEY.request_key_pairs()

        if not flag:
            helpers.handle_aws_error(response)
            return
        
        dict_key,filas_tabulate = self.ADMIN_KEY.format_data(response)

        if not filas_tabulate:
            print(f"No hay llaves SSH existentes en esta region : {self.region_name}")
            return None

        headers = data_ec2.header_key_pair["header"]
        title = data_ec2.header_key_pair["title"]

        helpers.display_table(filas_tabulate,headers,title)
        return helpers.choice(dict_key)
    
    def generate_key_pairs(self):

        name_key = self.ADMIN_KEY.request_name_key()

        if not name_key:
            return
        
        flag_gen_key,response_generate_key = self.ADMIN_KEY.generate_key_pair(name_key)

        if not flag_gen_key:
            helpers.handle_aws_error(response_generate_key)
            return

        flag_save_key,response_save_key = self.ADMIN_KEY.save_key_pair(response_generate_key,name_key)

        if not flag_save_key:
            helpers.handle_aws_error(response_save_key)
            return
        
        print(Fore.GREEN + f"💾-Llave guardada con exito en : {response_save_key}" + Style.RESET_ALL)

    def delete_key_pairs(self):
  
        selected_key_pair = self.select_key_pair()

        if not selected_key_pair:
            print("Hubo un error al seleccionar la llave SSH.")
            return

        confirmation = helpers.confirmation()
        if not confirmation:
            print("Operacion cancelada")
            return
        
        deleted_successfully,delete_code = self.ADMIN_KEY.delete_key_pair(selected_key_pair)

        if not deleted_successfully:
            helpers.handle_aws_error(delete_code)
            return

        logger.info(f"Se elimino la llave SSH : {selected_key_pair}.pem")
#AMIS

    def select_type_ec2(self):

        header = data_ec2.headers_types_ec2["header"]
        title = data_ec2.headers_types_ec2["title"]

        helpers.display_table(data_ec2.TYPES_INSTANCES,header,title)

        return helpers.choice(data_ec2.dict_type_instances)

    def select_os(self):

        header = data_ec2.header_os_general["header"]
        tile = data_ec2.header_os_general["title"]

        helpers.display_table(data_ec2.OS_AVALIBLE,header,tile)

        return helpers.choice(data_ec2.dict_os_general)
    
    def select_os_version(self,selected_os):

        if not selected_os:
            return
        
        header = data_ec2.header_os_version["header"]
        title = data_ec2.header_os_version["title"]

        fils_tabulate,dict_os_version = self.ADMIN_AMI.formate_data_selected_os(selected_os)

        helpers.display_table(fils_tabulate,header,title)

        return helpers.choice(dict_os_version)

    def select_ami_id(self,name_os,verion_os):

        owner = data_ec2.VERSION_OS[name_os][verion_os]["owner"]
        filtro = data_ec2.VERSION_OS[name_os][verion_os]["filter"]
        flag,code = self.ADMIN_AMI.get_ami_id(owner,filtro)

        if not flag:
            helpers.handle_aws_error(code)
            return
        
        filas_tabulate,dict_ami_id = self.ADMIN_AMI.prepare_data_ami(code)
        header = data_ec2.header_selected_ami["header"]
        title = data_ec2.header_selected_ami["title"]

        helpers.display_table(filas_tabulate,header,title)
        return helpers.choice(dict_ami_id)
        
    def get_ami_id(self):

        selected_os = self.select_os()

        version_os = self.select_os_version(selected_os)

        return self.select_ami_id(selected_os,version_os)

    def request_date_run_instance(self)-> dict:

        type_machime = self.select_type_ec2()
        ami_id = self.get_ami_id()
        key_pair_id = self.select_key_pair()
        sg_id = self.inject_sg_id()
        min_count,max_count,name_instance = helpers.request_date_config_ec2()

        return {
            "TypeMachine": type_machime,
            "AmiId": ami_id,
            "NameInstance": name_instance,
            "KeyPairName": key_pair_id,
            "SecurityGroupsId": sg_id,
            "MinCount": min_count,
            "MaxCount": max_count
        }

def main():

    try: 
        while True:
            region_name,location_name = helpers.select_region_name()
            manager = ManagerAWS(region_name)
            print(Fore.GREEN +"Validando credenciales..")
            print("Conectando con AWS..." + Style.RESET_ALL)
            time.sleep(1)
    
            flag,code = manager.ADMIN_EC2.verify_identity()

            if not flag:
                helpers.handle_aws_error(code)
                return

            matriz_dashboard = [[code.get("Account"),code.get("Arn"),location_name,manager.region_name]]
            print(Fore.GREEN + "conexion exitosa :D\n\n" + Style.RESET_ALL)
            exit = menu_services.root_menu(matriz_dashboard,manager)
            
            if exit:
                return
    except KeyboardInterrupt:
        return
                       
                    
if __name__ == "__main__":
    main()

