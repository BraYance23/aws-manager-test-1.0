from colorama import init,Fore,Style
from ui import helpers
from data import data_ec2
import logging

def ec2_menu(manager):

    while True:

        options_ec2 =  data_ec2.main_ec2

        print(Style.BRIGHT + "\n\n  Manage EC2\n" + Style.RESET_ALL)
        for clave,valor in options_ec2.items():
            print(f"|{clave}-{valor}")

        choice_ec2 = helpers.choice_main(options_ec2)
        match choice_ec2:
            
            case "1":
                manager.show_instances()
                input("Presione enter para continuar")
            case "2":
                manager.run_ec2()
            case "3" | "4" |"5" | "6":
                manager.operation_ec2(choice_ec2)
            case "7":
                break

def sg_menu(manager):

    while True:

        option_sg = data_ec2.main_sg
        print(Style.BRIGHT + "\n\n  Manage Security Groups" + Style.RESET_ALL)
        print( f"Estas operando sobre grupo de seguridad : {Style.BRIGHT + manager.ADMIN_SG.sg_id + Style.RESET_ALL} \n")

        for clave,valor in option_sg.items():
            print(f"|{clave}-{valor}")

        choice_sg = helpers.choice_main(option_sg)
        match choice_sg:

            case "1":
                manager.show_rules_sg()
                input("Presione enter para continuar.")
            case "2":
                manager.autorize_sg_ingress()
            case "3":
                manager.revoke_sg_ingress()
            case "4":
                manager.change_sg_id()
            case "5":
                break

def kp_menu(manager):
    
    while True:

        options_key_pair = data_ec2.main_key_pair            
        print(Style.BRIGHT + "\n\n  Manage Key Pairs\n" + Style.RESET_ALL)

        for clave,valor in options_key_pair.items():
            print(f"|{clave}-{valor}")

        choice_key_pair = helpers.choice_main(options_key_pair)

        match choice_key_pair:

            case "1":
                manager.show_key_pairs()
                input("Presione enter para continuar.")
            case "2":
                manager.generate_key_pairs()
            case "3":
                manager.delete_key_pairs()
            case "4":
                break

def root_menu(matriz_dashboard,manager):

    header = data_ec2.header_dashboard["header"]
    title = data_ec2.header_dashboard["title"]
    while True:

        print(Style.BRIGHT + f"\tBienvenido a Manage AWS \n" + Style.RESET_ALL)
        helpers.display_table(matriz_dashboard,header,title)
        options_aws = data_ec2.main_aws

        for clave,valor in options_aws.items():
            print(f"|{clave}-{valor}")

        choice_aws = helpers.choice_main(options_aws)
        match choice_aws:

            case "1":
                ec2_menu(manager)
            case "2":
                 if not manager.ADMIN_SG.sg_id:
                    manager.change_sg_id()
                 sg_menu(manager)
            case "3":
                kp_menu(manager)
            case "4":
                break
            case "5":
                print(Fore.GREEN + ":D Hasta pronto..." + Style.RESET_ALL)
                return True