import json
import logging
from ui.messages import print_message,handle_aws_error
from ui import prompt_general
from ui import tables
from utils.network import get_ip_public


logger = logging.getLogger(__name__)

class SGController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def inject_sg_id(self):

        flag,response_or_code = self.manager_root.sg.get_rules_sg()

        if not flag:
            handle_aws_error(response_or_code)
            return

        rich_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response_or_code)
        tables.print_table_sg(title="Security Groups Existentes",list_rows=rich_rows)
        return prompt_general.choice_options_table(dict_data=dict_sg_id,context="del grupo de seguridad que desea administrar")
            
    def show_rules_sg(self,direction:str):

        flag_response,response = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        if not flag_response:
            assert isinstance(response,str)
            handle_aws_error(response)
            return

        assert isinstance(response,dict)
        data_sg = self.manager_root.sg.formata_data_sg_rules(response)

        list_rows_ingress = data_sg["list_rows_ingress"]
        list_rows_egress = data_sg["list_rows_egress"]

        if direction ==  "ingress":
            if list_rows_ingress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de entrada",list_rows=list_rows_ingress)
                return
            print_message(f"No hay reglas de entrada existentes en esta region : [bold bright_white]{self.manager_root.region_name}[/bold bright_white]")
  
         
        elif direction == "egress":
            if list_rows_egress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de salida",list_rows=list_rows_egress)
                return
            print_message(message=f"No hay reglas de salida existentes en esta region : [bold bright_white]{self.manager_root.region_name}[/bold bright_white]",
                          style_message="green italic")
            
    def autorize_sg_ingress(self,direction):

        ip_public = get_ip_public()

        while True:
            ip_permissions = prompt_general.request_ip_permissions(ip_public)
            confirmation = prompt_general.confirmation_config(data=ip_permissions,title="Regla de entrada a crear")
            
            match confirmation:
                case "confirm":
                    break
                case "cancel":
                    return
                case "retry":
                    continue

        flag,code_or_rule = self.manager_root.sg.authorize_rule_ingress(ip_permissions)
        if not flag:
                  handle_aws_error(code_or_rule)
                  logger.error(f"Fallo  autorize_ingress | SG ID : {self.manager_root.sg.sg_id} | CODE : {code_or_rule}")
                  return

        format_ip_permissions = json.dumps(ip_permissions,indent=2,default=str)   
        print_message(f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"Autorize_ingress en SG ID: {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        self.show_rules_sg(direction)

    def autorize_sg_egress(self,direction):

        ip_public = get_ip_public()

        while True:
            ip_permissions = prompt_general.request_ip_permissions(ip_public)
            confirmation = prompt_general.confirmation_config(data=ip_permissions,title="Regla de salida a crear")
            
            match confirmation:
                case "confirm":
                    break
                case "cancel":
                    return
                case "retry":
                    continue

        flag,code_or_rule = self.manager_root.sg.authorize_rule_egress(ip_permissions)
        if not flag:
                  handle_aws_error(code_or_rule)
                  logger.error(f"Fallo  autorize_egress | SG ID : {self.manager_root.sg.sg_id} | CODE : {code_or_rule}")
                  return

        format_ip_permissions = json.dumps(ip_permissions,indent=2,default=str)   
        print_message(f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"Autorize_egress en SG ID: {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        self.show_rules_sg(direction)

    def revoke_sg_ingress(self,direction):

        flag_get_rules,response_or_code = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        if not flag_get_rules:
            handle_aws_error(response_or_code)
            return
            
        data_sg  = self.manager_root.sg.formata_data_sg_rules(response_or_code)
        dict_rules = data_sg.get("dict_rules_ingress")
        self.show_rules_sg(direction)

        if not dict_rules:
            print_message("[yellow italic]No hay reglas existentes.[/yellow italic]")
            return

        selected_rule = prompt_general.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        if selected_rule == "cancel":
            return
            
        confirmation = prompt_general.confirmation()
        if not confirmation:
            print_message("[yellow]Operacion cancelada[/yellow]")
            return
        
        flag_rules_ingress,code_or_rule = self.manager_root.sg.remove_rule_ingress(selected_rule)
        if not flag_rules_ingress:
                handle_aws_error(code_or_rule)
                logger.error(f"Fallo en revoke_ingress | SG ID : {self.manager_root.sg.sg_id} | CODE : {code_or_rule}")
                return

        format_ip_permissions = json.dumps(selected_rule,indent=2,default=str)
        logger.info(f"Revoke ingress en SG ID : {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        print_message(f"[green]Puerto : {code_or_rule['ToPort']} eliminado con exito de : {self.manager_root.sg.sg_id}[/green]")

    def revoke_sg_egress(self,direction):

        flag_get_rules,response_or_code = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        
        if not flag_get_rules:
            handle_aws_error(response_or_code)
            return
            
        data_sg  = self.manager_root.sg.formata_data_sg_rules(response_or_code)
        dict_rules = data_sg.get("dict_rules_egress")
        self.show_rules_sg(direction)

        if not dict_rules:
            print("No hay reglas existentes.")
            return

        selected_rule = prompt_general.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        if selected_rule == "cancel":
            return
        confirmation = prompt_general.confirmation()

        if not confirmation:
            print("Operacion cancelada")
            return
        flag_rules_ingress,code_or_rule = self.manager_root.sg.remove_rule_egress(selected_rule)

        if not flag_rules_ingress:
                handle_aws_error(code_or_rule)
                logger.error(f"Fallo en revoke_egress | SG ID : {self.manager_root.sg.sg_id} | CODE : {code_or_rule}")
                return

        format_ip_permissions = json.dumps(selected_rule,indent=2,default=str)
        logger.info(f"Revoke egress en SG ID : {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        print_message(message=f"Puerto : {code_or_rule['ToPort']} eliminado con exito de : {self.manager_root.sg.sg_id}",style_message="green italic")

    def change_sg_id(self):

        selected_sg_id = self.inject_sg_id()

        if selected_sg_id == "cancel":
            return "cancel"
        
        self.manager_root.sg.sg_id = selected_sg_id
        return True
