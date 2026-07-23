from controllers.ec2_controller import EC2Controller
from controllers.sg_controller import SGController
from controllers.kp_controller import KPController
from controllers.deploy_flow import select_sg_id
from ui import menus
from ui.prompt_general import choice_options_menu,center_text
from data import data_ec2


def ec2_menu(manager_root):

    ec2_controller = EC2Controller(manager_root=manager_root)

    while True:

        options_ec2 =  data_ec2.main_ec2
        print("\n")
        menus.print_menu_ec2()
        choice_ec2 = choice_options_menu(options_ec2)

        match choice_ec2: 
            case "1":
                ec2_controller.show_instances()
                input(center_text("Presione enter para continuar"))
            case "2":
                ec2_controller.run_ec2()
            case "3" | "4" |"5" | "6":
                ec2_controller.operation_ec2(choice_ec2)
            case "7":
                break

def sg_menu(manager_root):

    sg_controller = SGController(manager_root=manager_root)
    while True:
        
        menus.print_menu_sg(sg_id=manager_root.sg.sg_id)
        options_sg = data_ec2.main_sg
        choice_operation = choice_options_menu(dict_options=options_sg)

        match choice_operation:

            case "1":
                sg_controller.show_rules_sg(direction="ingress")
                input(center_text("Presione enter para continuar"))
            case "2":
                sg_controller.show_rules_sg(direction="egress")
                input(center_text("Presione enter para continuar"))    
            case "3":
                sg_controller.autorize_sg_ingress(direction = "ingress")
            case "4":
                sg_controller.autorize_sg_egress(direction = "egress")
            case "5":
                sg_controller.revoke_sg_ingress(direction = "ingress")
            case "6":
                sg_controller.revoke_sg_egress(direction = "egress")
            case "7":
                sg_controller.change_sg_id()
            case "8":
                break

def kp_menu(manager_root):

    kp_controller = KPController(manager_root=manager_root)
    while True:

        options_key_pair = data_ec2.main_key_pair
        menus.print_menu_kp(manager_root.region_name)
        choice_key_pair = choice_options_menu(dict_options=options_key_pair)

        match choice_key_pair:

            case "1":
                kp_controller.show_key_pairs()
                input(center_text("Presione entener para continuar"))
            case "2":
                kp_controller.generate_key_pairs()
            case "3":
                kp_controller.delete_key_pairs()
            case "4":
                break

def root_menu(account_data,manager_root):

    summary_resources = get_summary_all(manager_root)
    Dashboard_update = False
    while True:

        if Dashboard_update:
            menus.print_root_menu(account_data=account_data,summary=summary_resources,update_dashboard="\n[magenta italic]Dashboard actualizado correctamente\n[/magenta italic]")
            Dashboard_update = False  
        else:
            menus.print_root_menu(account_data=account_data,summary=summary_resources)

        options_root = data_ec2.main_root
        choice_aws = choice_options_menu(dict_options=options_root)
        match choice_aws:

            case "1":
                ec2_menu(manager_root)
            case "2":
                 if not manager_root.sg.sg_id:
    
                    if select_sg_id(manager_root=manager_root) == "cancel":
                        continue
                 sg_menu(manager_root)

            case "3":
                kp_menu(manager_root)
            case "4":
                summary_resources = get_summary_all(manager_root)
                Dashboard_update = True
                
            case "5":
                break
            case "6":
                print(":D Hasta pronto...")
                return True
            

def get_summary_all(manager_root):

    instance_on,instance_off = manager_root.ec2.summary_ec2()
    sg_total = manager_root.sg.summary_sg()
    key_pairs_total = manager_root.key_pair.summary_key_pairs()

    return {
        "instance_on": instance_on,
        "instance_off": instance_off,
        "sg_total": sg_total,
        "key_pairs_total": key_pairs_total
    }