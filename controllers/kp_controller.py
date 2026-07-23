import logging
from ui.messages import print_message,handle_aws_error
from ui import prompt_general
from ui import tables
from ui import helpers


logger = logging.getLogger(__name__)

class KPController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def show_key_pairs(self):

        flag,response_or_code = self.manager_root.key_pair.request_key_pairs()
        if not flag:
            handle_aws_error(response_or_code)
            return

        dict_id_key,list_rows = self.manager_root.key_pair.format_data(response_or_code)
        if not list_rows:
            print_message(f"[yellow italic]No hay llaves SSH en esta region[/yellow italic] : [bold bright_white]{self.manager_root.region_name}[/bold bright_white]")
            return
        
        tables.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)

    def select_key_pair(self)-> bool|None|str:

        flag,response = self.manager_root.key_pair.request_key_pairs()

        if not flag:
            handle_aws_error(response)
            return False
        
        dict_key,list_rows = self.manager_root.key_pair.format_data(response)

        if not list_rows:
            print_message(f"[yellow italic]No hay llaves SSH existentes en esta region[/yellow italic] : [bold bright_white]{self.region_name}[/bold bright_white]")
            return None

        tables.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)
        return prompt_general.choice_options_table(dict_data=dict_key,context="de la llave de SSH que desea eliminar ")
        
    def generate_key_pairs(self):

        name_key = self.manager_root.key_pair.request_name_key()
        if not name_key:
            return
        
        flag_gen_key,response_generate_key = self.manager_root.key_pair.generate_key_pair(name_key)
        if not flag_gen_key:
            handle_aws_error(response_generate_key)
            return

        flag_save_key,response_save_key = self.manager_root.key_pair.save_key_pair(response_generate_key,name_key)
        if not flag_save_key:
            handle_aws_error(response_save_key)
            return
        
        print_message(f"💾-Llave guardada con exito en : {response_save_key}",style_message="green italic")

    def delete_key_pairs(self):
  
        key_selected  = self.select_key_pair()

        match key_selected:
            case "cancel" | False | None:
                return

        confirmation = prompt_general.confirmation()
        if not confirmation:
                print("Operacion cancelada")
                return
                
        deleted_successfully,delete_code = self.manager_root.key_pair.delete_key_pair(key_selected)
        if not deleted_successfully:
            handle_aws_error(delete_code)
            return
        logger.info(f"Se elimino la llave SSH : {key_selected}.pem")