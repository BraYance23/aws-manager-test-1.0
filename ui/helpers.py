import json
import requests
from tabulate import tabulate
from colorama import init,Style,Fore
from data import data_ec2 

def choice(dict_data:dict)-> str:

    while True:
        choice = input(Style.BRIGHT + "\nIngrese el numero INDICE de la opcion que desee : " + Style.RESET_ALL).strip()

        if not choice:
            print(Fore.YELLOW + f"Valor ingresado vacio,por favor ingresar una opción." + Style.RESET_ALL)
            continue
        elif choice in dict_data:
            return dict_data[choice]
        
        print(Fore.YELLOW + "Valor ingresado no esta en el rango valido." + Style.RESET_ALL)
    
def request_ip_permissions(public_ip:str)-> dict:

    print("Por favor asegurarse de que los datos ingresados sean correctos.\n")
    protocol = input("Protocolo (tcp/udp/icmp/-1 para todo) : ").strip()

    while True:
  
        from_port = ask_int(prompt="Puerto inicio : ",value_min=1,value_max=65535,msg_max="El rango valido para puertos es : 1 -") if protocol != "-1" else -1
        to_port = ask_int(prompt="Puerto fin : ",value_min=1,value_max=65535,msg_max="El rango valido para puertos es : 1 -") if protocol != "-1" else -1

        if protocol == "-1":
            break
        elif to_port >= from_port:
            break

        print(Fore.YELLOW + "El puerto de inicio no puede ser mayor al puerto fin." + Style.RESET_ALL)
        continue     

    cidr_ip = input("CIDR IP (ej: 0.0.0.0/0 o ingresa \"1\" para colocar automaticamente su ip publica) : ").strip()
    description = input("Descripción de la regla (opcional) : ").strip()
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

def confirmation_config(data:dict,title:str="")-> bool:

    print(Style.BRIGHT + f"\n\t{title}" + Style.RESET_ALL)
    print(json.dumps(data,indent=2,default=str))
    while True:
        confirmation_user = input(Style.BRIGHT + "\nLos datos ingresados son correctos? S/N: " + Style.RESET_ALL ).strip().upper()

        if "S" != confirmation_user != "N":
                print(Fore.YELLOW + "Valor ingresado no valido, por favor confirmar operacion." + Style.RESET_ALL)
                continue
        return confirmation_user == "S"

def ask_int(prompt:str,value_min:int = 1,value_max:int = 100,msg_max:str="")-> int:

    while True:

        try:
            value = int(input(prompt))

            if value < value_min:
                print(Fore.YELLOW + f"El valor debe ser mayor o igual a : {value_min}" + Style.RESET_ALL)
                continue

            elif value > value_max:
                print(Fore.YELLOW + f"{msg_max} {value_max}" + Style.RESET_ALL)
                continue
            return value
        except ValueError:
            print(Fore.YELLOW + "Solo ingresar valores numericos." + Style.RESET_ALL)
    
def request_data_config_ec2()->tuple[int,int,str]:
    
    name_ec2= input(Style.BRIGHT + "Ingrese el nombre de la instancia : " + Style.RESET_ALL).strip()

    print(Fore.YELLOW +"""\n\nExplicacion de parametros minimo de instancias y maxino de instancias:
                  
AWS intentara lanzar hasta maximo de instancias que le indiques, pero si no puede (por falta de capacidad),
aceptara lanzar hasta llegar al minimo de instancias. Si no puede garantizar ni el mínimo, falla toda la operación.
                  
MaxCount = 5  → "quiero hasta 5"
MinCount = 2  → "pero necesito al menos 2\n""" + Style.RESET_ALL)
     
    while True:

        min_count = ask_int(prompt="Ingrese el minimo de instancias que desea desplegar : ",msg_max="El maximo de instancias que se puede desplegar es :")
        max_count = ask_int(prompt="Ingrese el maximo de instancias que desea desplegar : ",msg_max="El maximo de instancias que se puede desplegar es :")

        if max_count >= min_count:
            break
        print(Fore.YELLOW + "\nError: El máximo debe ser mayor o igual al mínimo. Intente de nuevo.\n" + Style.RESET_ALL)
        
    return min_count,max_count,name_ec2
           
def formate_region_name()-> list|dict:

    filas_tabulate = []
    dict_region_id = {}

    for indice,(key,value) in enumerate(data_ec2.AWS_REGIONS.items(),start=1):  
        dict_region_id[str(indice)] = key
        filas_tabulate.append(
             [indice,
              value,
              key
              ])    
    return filas_tabulate,dict_region_id

def select_region_name():
     
    filas_tabulate,dict_region_name = formate_region_name()
    header = data_ec2.header_region_name["header"]
    title = data_ec2.header_region_name["title"]

    display_table(filas_tabulate,header,title)
    region_name = choice(dict_region_name)
    location_name = data_ec2.AWS_REGIONS.get(region_name)
    return region_name,location_name

def handle_aws_error(code:str):
    """
    Maneja errores de AWS de forma centralizada
    
    Args:
        code: La excepción ClientError capturada
    """

    match code:
        # Errores de instancias
        case "InvalidInstanceID.NotFound":
            print(Fore.RED + f"Error: La instancia especificada no existe" + Style.RESET_ALL)
        case "InvalidInstanceID.Malformed":
            print(Fore.RED + f"El ID de la instancia tiene formato inválido" + Style.RESET_ALL)
        case "IncorrectInstanceState":
            print(Fore.RED + f"La instancia no puede realizar esta acción desde su estado actual" + Style.RESET_ALL)
        case "OperationNotPermitted":
            print(Fore.RED + f"La instancia tiene protección de terminación activada" + Style.RESET_ALL)
        case "InsufficientInstanceCapacity":
            print(Fore.RED + f"AWS no tiene capacidad disponible para este tipo de instancia" + Style.RESET_ALL)
        case "InstanceLimitExceeded":
            print(Fore.RED + f"Has alcanzado el límite de instancias en tu cuenta" + Style.RESET_ALL)
        case "UnsupportedInstanceAttribute":
            print(Fore.RED + f"Las instancias spot no soportan esta operación" + Style.RESET_ALL)

        # Errores de AMI
        case "InvalidAMIID.NotFound":
            print(Fore.RED + f"La AMI especificada no existe" + Style.RESET_ALL)
        case "InvalidAMIID.Malformed":
            print(Fore.RED + f"El ID de la AMI tiene formato inválido" + Style.RESET_ALL)

        # Errores de Key Pairs
        case "InvalidKeyPair.NotFound":
            print(Fore.RED + f"La key pair especificada no existe" + Style.RESET_ALL)
        case "InvalidKeyPair.Duplicate":
            print(Fore.RED + f"Ya existe una key pair con ese nombre" + Style.RESET_ALL)
        case "KeyPairLimitExceeded":
            print(Fore.RED + f"Has alcanzado el límite de key pairs en tu cuenta" + Style.RESET_ALL)
        case "ErrorSaveKey":
            print(Fore.RED + "Hubo un error al intentar guarda las key pairs en su dispitivo." + Style.RESET_ALL)

        # Errores de Security Groups
        case "InvalidGroup.NotFound":
            print(Fore.RED + f"El security group especificado no existe" + Style.RESET_ALL)
        case "InvalidGroupId.Malformed":
            print(Fore.RED + f"El ID del security group tiene formato inválido" + Style.RESET_ALL)
        case "InvalidPermission.Duplicate":
            print(Fore.RED + f"La regla ya existe en el security group" + Style.RESET_ALL)
        case "InvalidPermission.NotFound":
            print(Fore.RED + f"La regla especificada no existe en el security group" + Style.RESET_ALL)
        case "RulesPerSecurityGroupLimitExceeded":
            print(Fore.RED + f"Has alcanzado el límite de reglas en este security group" + Style.RESET_ALL)

        # Errores de Subnet
        case "InvalidSubnet.NotFound":
            print(Fore.RED + f"La subnet especificada no existe" + Style.RESET_ALL)

        # Errores genéricos
        case "InvalidParameterValue":
            print(Fore.RED + f"Uno de los parámetros tiene un valor inválido" + Style.RESET_ALL)
        case "UnauthorizedOperation":
            print(Fore.RED + f"No tienes permisos para realizar esta operación" + Style.RESET_ALL)
        case "AuthFailure":
            print(Fore.RED + f"Credenciales incorrectas o expiradas" + Style.RESET_ALL)
        case "RequestExpired":
            print(Fore.RED + f"La solicitud expiró, verifica la hora del sistema" + Style.RESET_ALL)

        # No se encontraron credenciales de aws
        case "No se encontraron credenciales":
            print(Fore.RED + "No se encontraron las credenciales de aws, ejecute en su terminal 'aws configure' para validar credenciales."+ Style.RESET_ALL)

        # Catch-all
        case _:
            print(Fore.RED + f"Error inesperado: {code}" + Style.RESET_ALL)

def confirmation()-> bool:

    while True:
        choice = input(Style.BRIGHT + Fore.RED + "Esta acción es irreversible, desea continuar S/N: "+ Style.RESET_ALL).strip().upper()

        if "S" != choice != "N":
            print(Fore.YELLOW + "Valor ingresado no valido, por favor confirmar operacion." + Style.RESET_ALL)
            continue

        return choice == "S"

def get_ip_public()-> str:

    urls = [
        "https://icanhazip.com",
        "https://wtfismyip.com/text",
        "https://ifconfig.me"
        ]
    
    for url in urls:
        try:
            response = requests.get(url,timeout=3).text.strip()
            if response:
                ip_public = f"{response}/32"
                return ip_public
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception:
            continue

def choice_main(dict_options:dict)-> str:

    while True:
        choice = input(Style.BRIGHT + "\nIngrese la opcion que desee : " + Style.RESET_ALL)

        if not choice:
            print(Fore.YELLOW + f"Valor ingresado vacio,por favor ingresar una opción." + Style.RESET_ALL)
            continue
        elif not choice in dict_options:
            print(Fore.YELLOW + "Valor ingresado no esta en el rango valido." + Style.RESET_ALL)
            continue
        return choice

def display_table(data:list,header:list,title:str):

    print(title)
    print(tabulate(data,headers=header,tablefmt="fancy_grid"))


if __name__ == "__main__":
    print(get_ip_public())