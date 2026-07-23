import threading
import logging
from ui.messages import print_message,spinner,handle_aws_error
from controllers.deploy_flow import build_instance_config
from ui import prompt_general,tables,helpers
from data import data_ec2


logger = logging.getLogger(__name__)

class EC2Controller:

    def __init__(self,manager_root):
        self.manager_root = manager_root
        pass


    def run_ec2(self):
        
        while True:

            config_instace = build_instance_config(manager_root=self.manager_root)
            confirmation = prompt_general.confirmation_config(config_instace,title="Configuracion de instancia a desplegar")

            match confirmation:
                 case "cancel":
                      return
                 case "confirm":
                      break
                 case "retry":
                      continue

        flag,code = self.manager_root.ec2.run_ec2(config_instace)
        if not flag:
            handle_aws_error(code)
            logger.error(f"Error al lanzar instancia : {code}")
            return
        
        stop_spinner = threading.Event()
        hilo_spinner = threading.Thread(target=spinner,args=(stop_spinner,"Desplegando instancia...","green"))
        hilo_spinner.start()

        try:
            correct_operation = self.manager_root.ec2.waiter_for_state(code,"running")                
        finally:
            stop_spinner.set()
            hilo_spinner.join()

        if not correct_operation:
                        print_message(f"No se pudo verificar el estado de la instancia, por favor validar en |1-Listar instancias",style_message="red italic")
                        return
        logger.info(f"EC2 desplegado correctamente, ID : {code}")
        print_message(message="-Instancia desplegada con exito",style_message="green italic")


    def show_instances(self):

        flag_response,response = self.manager_root.ec2.describe_ec2()

        if not flag_response:
            handle_aws_error(response)
            return
        
        dict_ec2_id,list_rows = self.manager_root.ec2.format_data_ec2(response)

        if not list_rows:
            print_message("No hay instancias existentes en esta region.",style_message="yellow italic")
            return

        print("\n\n")
        tables.print_table_ec2(list_rows=list_rows,title="Listado de instancias")
        logger.info("EC2 listadas correctamente.")

    def operation_ec2(self,selection):

        flag_describe_ec2,response = self.manager_root.ec2.describe_ec2()
        if not flag_describe_ec2:
            handle_aws_error(response)
            return

        dict_id_ec2,filas_tabulate = self.manager_root.ec2.format_data_ec2(response)
        if not filas_tabulate:
            print_message("No hay instancias existentes en esta region.",style_message="yellow italic")
            return
        
        self.show_instances()
        instance_id = prompt_general.choice_options_table(dict_id_ec2,context="de la instancia deseada")

        if instance_id == "cancel":
            return

        mensaje_init,waiter,mensaje_fin = data_ec2.pameter_operation_ec2[selection]
        
        if waiter == "terminated" and  not prompt_general.confirmation():
            print_message("Operacion cancelada por el usuario",style_message="yellow italic")
            return

        metodos_ec2 = {
            "3": self.manager_root.ec2.init_ec2,
            "4": self.manager_root.ec2.reboot_ec2,
            "5": self.manager_root.ec2.stop_ec2,
            "6": self.manager_root.ec2.terminate_ec2
            }

        flag,code = metodos_ec2[selection](instance_id)
        if not flag:
            handle_aws_error(code)
            return

        stop_spinner = threading.Event()
        hilo_spinner = threading.Thread(target=spinner,args=(stop_spinner,mensaje_init,"green"))
        hilo_spinner.start()
        try:
            correct_operation = self.manager_root.ec2.waiter_for_state(instance_id,waiter)
        finally:
            stop_spinner.set()
            hilo_spinner.join()

        if not correct_operation:
                        print_message(f"No se pudo verificar el estado de la instancia, por favor validar en |1-Listar instancias",style_message="red italic")
                        return
        print_message(message=mensaje_fin,style_message="green italic")