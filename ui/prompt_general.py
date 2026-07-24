from rich.console import Console
from rich.prompt import Prompt
from rich .table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from typing import Literal

console = Console()

def center_text(text:str)-> str:

    width = console.size.width
    padding = max(0,(width - len(text)) // 2)
    return " " * padding + text

def choice_options_table(dict_data:dict,context:str)-> str:


    while True:

        choice = Prompt.ask(center_text(text=f"Ingrese el # {context} ('0' para cancelar)"))

        if not choice:
            console.print("\n[yellow italic]Valor ingresado vacio,por favor ingresar una opción.[/yellow italic]\n",justify="center")
            print()
            continue
        elif choice in dict_data:
            return dict_data[choice]
        elif choice == "0":
            return "cancel"

        console.print("[yellow italic]\nValor ingresado no esta en el rango valido.[/yellow italic]\n",justify="center")

def choice_options_menu(dict_options:dict)-> str:

    while True:

        choice = Prompt.ask(center_text(text="Ingrese la opcion que desee"))
        if not choice:
            console.print("\n[yellow italic]Valor ingresado vacio,por favor ingresar una opción.[/yellow italic]\n",justify="center")
            continue
        elif not choice in dict_options:
            console.print("\n[yellow italic]Valor ingresado no esta en el rango valido.[/yellow italic]\n",justify="center")
            continue
        return choice
    
def confirmation_config(data:dict)-> Literal["confirm","cancel","retry"]:

    
    while True:
        print("\n")
        confirmation_user = Prompt.ask(center_text(text="¿Los datos ingresados son correctos? [S/N] | [0] Volver al menú anterior ")).strip().upper()

        if confirmation_user not in ["S","N","0"]:
                console.print("Valor ingresado no valido, por favor confirmar operacion.",style="yellow italic",justify="center")
                continue

        if confirmation_user == "S":
            return "confirm"
        elif confirmation_user == "0":
            return "cancel"
        else:
            return "retry"

def confirmation()-> bool:

    while True:
        choice = Prompt.ask(center_text("Esta acción es irreversible, desea continuar S/N ")).strip().upper()

        if "S" != choice != "N":
            console.print("Valor ingresado no valido, por favor confirmar operacion.")
            continue

        return choice == "S"

def build_panel_rules_sg(data:dict):

    ip_protocol = data["IpProtocol"]
    from_port = data["FromPort"]
    to_port = data["FromPort"]
    for value in data["IpRanges"]:
        cdrip_ip = value["CidrIp"]
        description = value["Description"]


    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=True
    )

    table.add_column(
        "Campo",
        style="bold cyan",
        justify="right",
        no_wrap=True
    )

    table.add_column(
        "Valor",
        style="white"
    )

    table.add_row(
        "Protocolo",
        f"[dim magenta]{ip_protocol}[/dim magenta]"
    )

    table.add_row(
        "Puerto inicio",
        f"[dim magenta]{from_port}[/dim magenta]"
    )

    table.add_row(
        "Puerto fin",
        f"[dim magenta]{to_port}[/dim magenta]"
    )

    table.add_row(
        "Cdrip IP",
        f"[dim magenta]{cdrip_ip}[/dim magenta]"
    )

    table.add_row(
        "Descripcion",
        f"[dim magenta]{description}[/dim magenta]"
    )

    panel = Panel(
        table,
        title="[bold white]🌐 Datos de regla a crear[/bold white]",
        title_align="center",
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print(
        Align.center(panel)
    )

def build_panel_deploy_ec2(data: dict):

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=True
    )

    table.add_column(
        "Campo",
        style="bold cyan",
        justify="right",
        no_wrap=True
    )

    table.add_column(
        "Valor",
        style="white"
    )

    table.add_row(
        "Tipo de máquina",
        f"[dim magenta]{data['TypeMachine']}[/dim magenta]"
    )

    table.add_row(
        "AMI ID",
        f"[dim magenta]{data['AmiId']}[/dim magenta]"
    )

    table.add_row(
        "Nombre de instancia",
        f"[dim magenta]{data['NameInstance']}[/dim magenta]"
    )

    table.add_row(
        "Llave SSH",
        f"[dim magenta]{data['KeyPairName']}[/dim magenta]"
    )

    table.add_row(
        "Grupo de seguridad",
        f"[dim magenta]{data['SecurityGroupsId']}[/dim magenta]"
    )

    table.add_row(
        "Mínimo de instancias",
        f"[dim magenta]{data['MinCount']}[/dim magenta]"
    )

    table.add_row(
        "Máximo de instancias",
        f"[dim magenta]{data['MaxCount']}[/dim magenta]"
    )

    panel = Panel(
        table,
        title="[bold white]🚀 Datos de instancia a desplegar[/bold white]",
        title_align="center",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print(
        Align.center(panel)
    )

def request_ip_permissions(public_ip:str)-> dict:

    console.print("Por favor asegurarse de que los datos ingresados sean correctos.\n",style="bold bright_white",justify="center")
    protocol = Prompt.ask(center_text(text="Protocolo (tcp/udp/icmp/-1 para todo) ")).strip()

    while True:
  
        from_port = ask_int(prompt="Puerto inicio : ",value_min=1,value_max=65535,msg_max="El rango valido para puertos es : 1 -") if protocol != "-1" else -1
        to_port = ask_int(prompt="Puerto fin : ",value_min=1,value_max=65535,msg_max="El rango valido para puertos es : 1 -") if protocol != "-1" else -1

        if protocol == "-1":
            break
        elif to_port >= from_port:
            break

        console.print("El puerto de inicio no puede ser mayor al puerto fin.",style="yellow italic",justify="center")
        continue
    cidr_ip = Prompt.ask(center_text(text="CIDR IP (ej: 0.0.0.0/0 o ingresa \"1\" para colocar automaticamente su ip publica) ")).strip()
    description = Prompt.ask(center_text(text="Descripción de la regla (opcional) "))
    cidr_ip_finaly = public_ip if cidr_ip == "1" else cidr_ip
    return {
            "IpProtocol": protocol,
            "FromPort": from_port,
            "ToPort": to_port,
            "IpRanges": [
                {
                    "CidrIp": cidr_ip_finaly,
                    "Description": description
                }
            ]
        }

def ask_int(prompt:str,value_min:int = 1,value_max:int = 100,msg_max:str="")-> int:

    while True:

        try:
            value = int(input(center_text(prompt)).strip())

            if value < value_min:
                console.print(f"El valor debe ser mayor o igual a : {value_min}",style="yellow italic",justify="center")
                continue

            elif value > value_max:
                console.print(f"\n{msg_max} {value_max}\n",style="yellow italic",justify="center")
                continue
            return value
        except ValueError:
            console.print("Solo ingresar valores numericos.",style="yellow italic",justify="center")
    
def request_data_config_ec2()->tuple[int,int,str]:

    
    name_ec2= Prompt.ask(center_text("Ingrese el nombre de la instancia a desplegar ")).strip()

    print("\n")
    console.print("""[bold bright_white]Explicacion de parametros minimo de instancias y maxino de instancias[/bold bright_white]
                  
AWS intentara lanzar hasta maximo de instancias que le indiques, pero si no puede (por falta de capacidad),
aceptara lanzar hasta llegar al minimo de instancias. Si no puede garantizar ni el mínimo, falla toda la operación.
                  
MaxCount = 5  → "quiero hasta 5"
MinCount = 2  → "pero necesito al menos 2"\n""",style="green",justify="center")
     
    while True:

        min_count = ask_int(prompt="Ingrese el minimo de instancias que desea desplegar : ",msg_max="El maximo de instancias que se puede desplegar es :")
        max_count = ask_int(prompt="Ingrese el maximo de instancias que desea desplegar : ",msg_max="El maximo de instancias que se puede desplegar es :")

        if max_count >= min_count:
            break
        console.print("\nError: El máximo debe ser mayor o igual al mínimo. Intente de nuevo.\n",style="yellow italic",justify="center")
        
    return min_count,max_count,name_ec2
     
if __name__ == "__main__":
    request_data_config_ec2()
