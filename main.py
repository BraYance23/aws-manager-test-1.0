import time
import logging
from dotenv import load_dotenv
from config import logging_config
from core.manage_key_pair import ManageKeyPairs
from core.manage_sg import ManageSecurityGroup
from core.manage_ami import ManageAmi
from core.manage_ec2 import ManageEc2
from controllers import menu_services
from ui.messages import print_message,handle_aws_error
from ui.tables import select_region_name


logging_config.setup_logging()
logger = logging.getLogger(__name__)

class ManagerAWS:

    def __init__(self,region_name:str="us-east-1"):
        load_dotenv()
        self.region_name = region_name
        self.ec2 = ManageEc2(self.region_name)
        self.ami = ManageAmi(self.region_name)
        self.key_pair = ManageKeyPairs(self.region_name)
        self.sg = ManageSecurityGroup(self.region_name)


def main():

    try: 
        while True:

            region_name,location_name = select_region_name()
            if region_name == "cancel":
                return
            
            manager_root = ManagerAWS(region_name=region_name)
            print_message(message="\nValidando credenciales...\nConetando con AWS...",style_message="green italic")
            time.sleep(1)

            flag,code = manager_root.ec2.verify_identity()
            if not flag:
                handle_aws_error(code)
                return
            
            account_data = (code["Account"],code["Arn"],location_name,region_name)
            print_message("Conexion exitosa :D\n\n",style_message="bold bright_white")
            
            exit_program = menu_services.root_menu(account_data=account_data,manager_root=manager_root)
            if exit_program:
                return       
    except KeyboardInterrupt:
        return
                                          
if __name__ == "__main__":
    main()
