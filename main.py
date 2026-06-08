from core.manage_ami import ManageAmi
from core.manage_ec2 import ManageEc2
from core.manage_key_pair import ManageKeyPairs
from core.manage_sg import ManageSecurityGroup
from data import data_ec2
from ui import helpers
from colorama import init,Style,Fore
import time


class ManagerAWS:

    def __init__(self,region_name="us-east-1"):
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
            helpers.handle_aws_error(flag,code)
            return
        
        print(Fore.CYAN + Style.BRIGHT + "-Desplegando instancia...")
        time.sleep(8)
        print("instancia desplegada correctamente.🚀" + Style.RESET_ALL)
    
    def init_ec2(self):

        dict_id_ec2,filas_tabulate = self.ADMIN_EC2.preparative()

        if not filas_tabulate:
            print("No hay instancias existentes en esta region.")
            return

        self.show_instances()

        instance_id = helpers.choice(dict_id_ec2)
        flag,code = self.ADMIN_EC2.init_ec2(instance_id)

        if not flag:
            helpers.handle_aws_error(flag,code)
            return

        print(Fore.CYAN + Style.BRIGHT + "📟-Iniciando instancia..." + Style.RESET_ALL)
        self.ADMIN_EC2.waiter_for_state(instance_id,"running")
        print("✅ Instancia iniciada correctamente.")
                
    def show_instances(self):

        dict_ec2_id,filas_tabulate = self.ADMIN_EC2.preparative()

        if not filas_tabulate:
            print("No hay instancias existentes en esta region.")
            return
        header = data_ec2.header_ec2["header"]
        title = data_ec2.header_ec2["title"]

        helpers.display_table(filas_tabulate,header,title)

    def stop_ec2(self):

        dict_id_ec2,filas_tabulate = self.ADMIN_EC2.preparative()

        if not dict_id_ec2:
            print("No hay instancias existentes en esta region.")
            return

        self.show_instances()

        instance_id = helpers.choice(dict_id_ec2)
        flag,code = self.ADMIN_EC2.stop_ec2(instance_id)

        if not flag:
            helpers.handle_aws_error(flag,code)
            return
        
        print(Fore.CYAN + Style.BRIGHT + "-⛔Deteneniendo instancia..." + Style.RESET_ALL)
        self.ADMIN_EC2.waiter_for_state(instance_id,"stopped")
        print("Instancia detenida correctamente")
  
    def reboot_ec2(self):

        dict_id_ec2,filas_tabulate = self.ADMIN_EC2.preparative()

        if not dict_id_ec2:
            print("No hay instancias existentes en esta region.")
            return

        self.show_instances()
        
        instance_id = helpers.choice(dict_id_ec2)

        flag,code = self.ADMIN_EC2.reboot_ec2(instance_id)

        if not flag:
            helpers.handle_aws_error(flag,code)
            return

        print(Fore.CYAN + Style.BRIGHT + "⟳Reinciando instancia..." + Style.RESET_ALL)
        self.ADMIN_EC2.waiter_for_state(instance_id,"running")
        print("Instancia reiniciada correctamente")
                    
    def terminate_ec2(self):
        
        dict_id_ec2,filas_tabulate  = self.ADMIN_EC2.preparative()
        if not dict_id_ec2:
            print("No hay instancias existentes en esta region.")
            return

        self.show_instances()

        instance_id = helpers.choice(dict_id_ec2)

        confirmation = helpers.confirmation()

        if not confirmation:
            print("Operacion cancelada")
            return
        flag,code = self.ADMIN_EC2.terminate_ec2(instance_id)
        
        if not flag:
            helpers.handle_aws_error(flag,code)
            return

        print(Fore.BLUE + Style.BRIGHT + "🗑️-Eliminando instancia..." + Style.RESET_ALL)
        self.ADMIN_EC2.waiter_for_state(instance_id,"terminated")
        print("Instancia eliminado correctamente.")
    
#Security Groups

    def inject_sg_id(self):

        flag,response_or_code = self.ADMIN_SG.get_rules_sg()

        if not flag:
            helpers.handle_aws_error(flag,response_or_code)
            return

        filas_tabulate,dict_sg_id = self.ADMIN_SG.format_data_sg_general(response_or_code)

        header = data_ec2.header_sg["header"]
        title = data_ec2.header_sg["title"]

        helpers.display_table(filas_tabulate,header,title)
        
        return helpers.choice(dict_sg_id)
            
    def show_rules_sg(self):


        flag,response_or_code = self.ADMIN_SG.get_rules_sg(self.ADMIN_SG.sg_id)

        if not flag:
            helpers.handle_aws_error(flag,response_or_code)
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
                  helpers.handle_aws_error(flag,code_or_rule)
                  return
                  
        print(Fore.GREEN + f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.ADMIN_SG.sg_id}" + Style.RESET_ALL)
        input("Presione enter para listar las reglas actualizadas.")
        self.show_rules_sg()
                
    def revoke_sg_ingress(self):

        flag_get_rules,response_or_code = self.ADMIN_SG.get_rules_sg(self.ADMIN_SG.sg_id)
        
        if not flag_get_rules:
            helpers.handle_aws_error(flag_get_rules,response_or_code)
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
                helpers.handle_aws_error(flag_rules_ingress,code_or_rule)
                return

        print(Fore.GREEN +f"Puerto : {code_or_rule['ToPort']} eliminado con exito de : {self.ADMIN_SG.sg_id}" + Style.RESET_ALL)

    def change_sg_id(self):

        self.ADMIN_SG.sg_id = self.inject_sg_id()

#Key Pairs

    def show_key_pairs(self):

        flag,response_or_code = self.ADMIN_KEY.request_key_pairs()

        if not flag:
            helpers.handle_aws_error(flag,response_or_code)
            return

        dict_id_key,filas_tabulate = self.ADMIN_KEY.prepare_data(response_or_code)
        if not filas_tabulate:
            print(f"No hay llaves SSH en esta region : {self.region_name}")
            return

        header = data_ec2.header_key_pair["header"]
        title = data_ec2.header_key_pair["title"]
        helpers.display_table(filas_tabulate,header,title)

    def generate_key_pairs(self):

        name_key = self.ADMIN_KEY.request_name_key()

        if not name_key:
            return
        
        flag_gen_key,response_generate_key = self.ADMIN_KEY.generate_key_pair(name_key)

        if not flag_gen_key:
            helpers.handle_aws_error(flag_gen_key,response_generate_key)
            return

        flag_save_key,response_save_key = self.ADMIN_KEY.save_key_pair(response_generate_key,name_key)

        if not flag_save_key:
            helpers.handle_aws_error(flag_save_key,response_save_key)
            return
        
        print(Fore.GREEN + f"Llave guardada con exito en : {response_save_key}" + Style.RESET_ALL)

    def delete_key_pairs(self,cut:bool=False):

        succes,response = self.ADMIN_KEY.request_key_pairs()

        if not succes:
            helpers.handle_aws_error(succes,response)
            return
        
        dict_key,filas_tabulate = self.ADMIN_KEY.prepare_data(response)

        if not filas_tabulate:
            print(f"No hay llaves SSH existentes en esta region : {self.region_name}")
            return
        
        self.show_key_pairs()
        
        selected_key_pair = helpers.choice(dict_key)


        if not cut:

            confirmation = helpers.confirmation()

            if not confirmation:
                print("Operacion cancelada")
                return
        
            deleted_successfully,delete_code = self.ADMIN_KEY.delete_key_pair(selected_key_pair)

            if not deleted_successfully:
                helpers.handle_aws_error(deleted_successfully,delete_code)
                return
            
        return selected_key_pair

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
            helpers.handle_aws_error(flag,code)
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

    def request_date_run_instance(self):

        type_machime = self.select_type_ec2()
        ami_id = self.get_ami_id()
        key_pair_id = self.delete_key_pairs(True)
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

#MENUS DE ORQUESTADORES
    def ec2_menu(self):

        while True:

            options_ec2 =  data_ec2.main_ec2

            print("Manage EC2\n")
            for clave,valor in options_ec2.items():
                print(f"\t{clave}-{valor}")

            choice_ec2 = helpers.choice_main(options_ec2)

            match choice_ec2:

                case "1":
                    self.show_instances()
                    input("Presione enter para continuar")
                case "2":
                    self.run_ec2()
                case "3":
                    self.init_ec2()
                case "4":
                    self.reboot_ec2()
                case "5":
                    self.stop_ec2()
                case "6":
                    self.terminate_ec2()
                case "7":
                    break

    def sg_menu(self):

        while True:

            option_sg = data_ec2.main_sg
            print( Fore.BLUE + f"Estas operando sobre grupo de seguridad : {self.ADMIN_SG.sg_id} \n" + Style.RESET_ALL)
            print("Manage Security Groups")

            for clave,valor in option_sg.items():

                print(f"\t{clave}-{valor}")

            choice_sg = helpers.choice_main(option_sg)

            match choice_sg:

                case "1":
                    self.show_rules_sg()
                    input("Presione enter para continuar.")
                case "2":
                    self.autorize_sg_ingress()
                case "3":
                    self.revoke_sg_ingress()
                case "4":
                    self.change_sg_id()
                case "5":
                    break

    def kp_menu(self):
        
        while True:

            options_key_pair = data_ec2.main_key_pair
                        
            print("Manage Key Pairs\n")
            for clave,valor in options_key_pair.items():
                print(f"\t{clave}-{valor}")

            choice_key_pair = helpers.choice_main(options_key_pair)

            match choice_key_pair:

                case "1":
                    self.show_key_pairs()
                    input("Presione enter para continuar.")
                case "2":
                    self.generate_key_pairs()
                case "3":
                    self.delete_key_pairs()
                case "4":
                    break


def main():
        
    while True:
        region_name = helpers.select_region_name()
        manager = ManagerAWS(region_name)
        print(Fore.GREEN +"Validando credenciales..")
        print("Conectando con AWS..." + Style.RESET_ALL)
        time.sleep(4)

            
        flag,code = manager.ADMIN_EC2.verify_identity()

        if not flag:
            helpers.handle_aws_error(flag,code)
            return

        account_id = code.get("Account")
        arn = code.get("Arn")
        print(Fore.GREEN + "conexion exitosa :D" + Style.RESET_ALL)

        while True:

            print(f"Bienvenido a Manage AWS \n")
            print(f"ID  de la cuenta : {Style.BRIGHT + account_id + Style.RESET_ALL}")
            print(f"ARN : {Style.BRIGHT + arn + Style.RESET_ALL}")
            print(f"Estas operando sobre la region : {Style.BRIGHT + manager.region_name + Style.RESET_ALL}\n")

            options_aws = data_ec2.main_aws

            print("_" * 30)
            for clave,valor in options_aws.items():

                print(f"|{clave}-{valor}")
            print("-" * 30)

            choice_aws = helpers.choice_main(options_aws)

            match choice_aws:

                case "1":
                    manager.ec2_menu()
                case "2":
                    manager.change_sg_id()
                    manager.sg_menu()
                case "3":
                    manager.kp_menu()
                case "4":
                    break
                case "5":
                    print(Fore.GREEN + ":D Hasta pronto..." + Style.RESET_ALL)
                    return
                       
                    

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        pass