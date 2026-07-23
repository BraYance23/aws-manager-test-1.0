import time
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live


console = Console()

def print_message(message,style_message:str=""):

    console.print(message,style=style_message,justify="center")

def print_message_panel(color_panel:str,message:str,style_message:str=""):

    panel = Panel(f"{message}",border_style=color_panel,style=style_message)
    console.print(Align.center(panel))


def spinner(stop_event,text_spinner,style_message):

    console = Console()
    spinnerr = Spinner("dots",text=f"[green]{text_spinner}[/green]",style=style_message)
  
    spinnerr_center = Align.center(spinnerr)
    with Live(spinnerr_center,console=console,refresh_per_second=12):
        while not stop_event.is_set():
            time.sleep(0.3)

def handle_aws_error(code:str):
    """
    Maneja errores de AWS de forma centralizada
    
    Args:
        code: La excepción ClientError capturada
    """

    match code:
        # Errores de instancias
        case "InvalidInstanceID.NotFound":
            print_message(f"Error: La instancia especificada no existe", style_message="italic red")
        case "InvalidInstanceID.Malformed":
            print_message(f"El ID de la instancia tiene formato inválido", style_message="italic red")
        case "IncorrectInstanceState":
            print_message(f"La instancia no puede realizar esta acción desde su estado actual", style_message="italic red")
        case "OperationNotPermitted":
            print_message(f"La instancia tiene protección de terminación activada", style_message="italic red")
        case "InsufficientInstanceCapacity":
            print_message(f"AWS no tiene capacidad disponible para este tipo de instancia", style_message="italic red")
        case "InstanceLimitExceeded":
            print_message(f"Has alcanzado el límite de instancias en tu cuenta", style_message="italic red")
        case "UnsupportedInstanceAttribute":
            print_message(f"Las instancias spot no soportan esta operación", style_message="italic red")

        # Errores de AMI
        case "InvalidAMIID.NotFound":
            print_message(f"La AMI especificada no existe", style_message="italic red")
        case "InvalidAMIID.Malformed":
            print_message(f"El ID de la AMI tiene formato inválido", style_message="italic red")

        # Errores de Key Pairs
        case "InvalidKeyPair.NotFound":
            print_message(f"La key pair especificada no existe", style_message="italic red")
        case "InvalidKeyPair.Duplicate":
            print_message(f"Ya existe una key pair con ese nombre", style_message="italic red")
        case "KeyPairLimitExceeded":
            print_message(f"Has alcanzado el límite de key pairs en tu cuenta", style_message="italic red")
        case "ErrorSaveKey":
            print_message("Hubo un error al intentar guarda las key pairs en su dispitivo.", style_message="italic red")

        # Errores de Security Groups
        case "InvalidGroup.NotFound":
            print_message(f"El security group especificado no existe", style_message="italic red")
        case "InvalidGroupId.Malformed":
            print_message(f"El ID del security group tiene formato inválido", style_message="italic red")
        case "InvalidPermission.Duplicate":
            print_message(f"La regla ya existe en el security group", style_message="italic red")
        case "InvalidPermission.NotFound":
            print_message(f"La regla especificada no existe en el security group", style_message="italic red")
        case "RulesPerSecurityGroupLimitExceeded":
            print_message(f"Has alcanzado el límite de reglas en este security group", style_message="italic red")

        # Errores de Subnet
        case "InvalidSubnet.NotFound":
            print_message(f"La subnet especificada no existe", style_message="italic red")

        # Errores genéricos
        case "InvalidParameterValue":
            print_message(f"Uno de los parámetros tiene un valor inválido", style_message="italic red")
        case "UnauthorizedOperation":
            print_message(f"No tienes permisos para realizar esta operación", style_message="italic red")
        case "AuthFailure":
            print_message(f"Credenciales incorrectas o expiradas", style_message="italic red")
        case "RequestExpired":
            print_message(f"La solicitud expiró, verifica la hora del sistema", style_message="italic red")

        # No se encontraron credenciales de aws
        case "No se encontraron credenciales":
            print_message("No se encontraron las credenciales de aws, ejecute en su terminal 'aws configure' para validar credenciales.", style_message="italic red")

        # Catch-all
        case _:
            print_message(f"Error inesperado: {code}", style_message="italic red")
