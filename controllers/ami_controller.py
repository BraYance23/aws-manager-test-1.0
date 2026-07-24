import logging
from ui.messages import handle_aws_error
from ui import prompt_general
from ui.tables import print_table_ami
from data import data_ec2


logger = logging.getLogger(__name__)

class AmiController:

    def __init__(self,manager_root):
        self.manager_root = manager_root


    def select_type_ec2(self):

        header = data_ec2.headers_types_ec2["header"]
        title = data_ec2.headers_types_ec2["title"]
        print_table_ami(list_header=header,title=title,list_rows=data_ec2.TYPES_INSTANCES)
        return prompt_general.choice_options_table(dict_data=data_ec2.dict_type_instances,context="del tipo de instancia que desea desplegar")
    
    def select_os(self):

        header = data_ec2.header_os_general["header"]
        title = data_ec2.header_os_general["title"]
        print_table_ami(list_header=header,title=title,list_rows=data_ec2.OS_AVALIBLE)
        return prompt_general.choice_options_table(dict_data=data_ec2.dict_os_general,context="del sistema operativo que desea desplegar")
    
    def select_os_version(self,selected_os):

        if not selected_os:
            return
        
        header = data_ec2.header_os_version["header"]
        title = data_ec2.header_os_version["title"]
        list_rows,dict_os_version = self.manager_root.ami.formate_data_selected_os(selected_os)
        print_table_ami(list_header=header,title=title,list_rows=list_rows)
        return prompt_general.choice_options_table(dict_data=dict_os_version,context="de la version de sistema operativo deseado")

    def select_ami_id(self,name_os,verion_os):

        owner = data_ec2.VERSION_OS[name_os][verion_os]["owner"]
        filtro = data_ec2.VERSION_OS[name_os][verion_os]["filter"]
        flag,code = self.manager_root.ami.get_ami_id(owner,filtro)

        if not flag:
            handle_aws_error(code)
            return
        
        list_rows,dict_ami_id = self.manager_root.ami.prepare_data_ami(code)
        header = data_ec2.header_selected_ami["header"]
        title = data_ec2.header_selected_ami["title"]

        print_table_ami(list_header=header,title=title,list_rows=list_rows)
        return prompt_general.choice_options_table(dict_data=dict_ami_id,context="de la AMI ID deseada")
    
    def get_ami_id(self):

        selected_os = self.select_os()
        if selected_os == "cancel":
            return "cancel"

        version_os = self.select_os_version(selected_os)
        if selected_os == "cancel":
            return "cancel"

        return self.select_ami_id(selected_os,version_os)
       
