from colorama import init,Fore,Style
from ui import helpers
from data import data_ec2
import logging

def ec2_menu(manager):

    while True:

        options_ec2 =  data_ec2.main_ec2

        print(Style.BRIGHT + "\n\n\t\t\t\t    Manage EC2" + Style.RESET_ALL)
        print("\t\t\t╒═════════════════════════════════╕")
        for clave,valor in options_ec2.items():
            print(f"\t\t\t│ [{Style.BRIGHT + clave + Style.RESET_ALL}] -> {valor:<25}│")
        print("\t\t\t╘═════════════════════════════════╛")

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
        print(Style.BRIGHT + "\n\n\t\t\t\tManage Security Groups" + Style.RESET_ALL)
        print("\t\t\t╒════════════════════════════════════╕")
        print(f"\t\t\t│   {Style.BRIGHT} SG ID: {manager.security_groups.sg_id} {Style.RESET_ALL}    │")
        print("\t\t\t╞════════════════════════════════════╡")
        for clave,valor in option_sg.items():
            print(f"\t\t\t│ [{Style.BRIGHT + clave + Style.RESET_ALL}] -> {valor:<28}│")
        print("\t\t\t╘════════════════════════════════════╛")
        

        choice_operation = helpers.choice_main(option_sg)
        match choice_operation:

            case "1":
                manager.show_rules_sg(direction="ingress")
                input("Presione enter para continuar.")
            case "2":
                manager.show_rules_sg(direction="egress")
                input("Presione enter para continuar.")    
            case "3":
                manager.autorize_sg_ingress(direction = "ingress")
            case "4":
                manager.revoke_sg_ingress(direction = "ingress")
            case "5":
                manager.autorize_sg_egress(direction = "egress")
            case "6":
                manager.revoke_sg_egress(direction = "egress")
            case "7":
                manager.change_sg_id()
            case "8":
                break

def kp_menu(manager):
    
    while True:

        options_key_pair = data_ec2.main_key_pair            
        print(Style.BRIGHT + "\t\t\t\t  Manage Key Pairs" + Style.RESET_ALL)

        print("\t\t\t ╒═════════════════════════════════╕")
        for clave,valor in options_key_pair.items():
            print(f"\t\t\t │ [{Style.BRIGHT + clave + Style.RESET_ALL}] -> {valor:<25}│")
        print("\t\t\t ╘═════════════════════════════════╛")

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
    summary_resources = get_summary_all(manager)
    Dashboard_update = False

    while True:

        print(Style.BRIGHT + f"\t\t\t\tBienvenido a Manage AWS \n" + Style.RESET_ALL)
        helpers.display_table(matriz_dashboard,header,title)
        print_dashboard_resources(summary_resources)
        options_root = data_ec2.main_root

        if Dashboard_update:
            print(Fore.CYAN + "\t\t\t[i] Dashboard actualizado correctamente" + Style.RESET_ALL)
            Dashboard_update = False   
        print("\t\t\t╒════════════════════════════════════╕")
        for clave,valor in options_root.items():
            print(f"\t\t\t│ [{Style.BRIGHT + clave + Style.RESET_ALL}] -> {valor:<28}│")
        print("\t\t\t╘════════════════════════════════════╛")

        choice_aws = helpers.choice_main(options_root)
        match choice_aws:

            case "1":
                ec2_menu(manager)
            case "2":
                 if not manager.security_groups.sg_id:
                    if manager.change_sg_id() == "cancel":
                        continue
                 sg_menu(manager)
            case "3":
                kp_menu(manager)
            case "4":
                summary_resources = get_summary_all(manager)
                Dashboard_update = True
                
            case "5":
                break
            case "6":
                print(Fore.GREEN + ":D Hasta pronto..." + Style.RESET_ALL)

def print_dashboard_resources(summary_resources):

    instance_on = f"{summary_resources["instance_on"]:>3}"
    instance_off = f"{summary_resources["instance_off"]:>3}"
    sg_total = f"{summary_resources["sg_total"]:>3}"
    key_pairs_total = f"{summary_resources["key_pairs_total"]:>3}"

    ec2_dashboard = f"{Style.BRIGHT}EC2{Style.RESET_ALL} : {instance_on} Activas / {instance_off} Inactivas"
    sg_dashboard = f"{Style.BRIGHT}SG{Style.RESET_ALL}: {sg_total}"
    key_pairs_dashboard = f"{Style.BRIGHT}Key Pairs{Style.RESET_ALL}: {key_pairs_total}"

    print("\t\t╒══════════════════════════════════════════════════════════════╕")
    print(f"\t\t│ {ec2_dashboard} | {sg_dashboard} | {key_pairs_dashboard} │")
    print("\t\t╘══════════════════════════════════════════════════════════════╛")

def get_summary_all(manager):

    instance_on,instance_off = manager.ec2.summary_ec2()
    sg_total = manager.security_groups.summary_sg()
    key_pairs_total = manager.key_pair.summary_key_pairs()

    return {
        "instance_on": instance_on,
        "instance_off": instance_off,
        "sg_total": sg_total,
        "key_pairs_total": key_pairs_total
    }