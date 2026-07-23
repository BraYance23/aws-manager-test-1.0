from rich.console import Console
from rich.columns import Columns
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()

def print_menu_kp(region):

    kp_menu_options = Text.from_markup(
        f"[italic]Operando sobre la region[/italic] : [bold bright_white]{region}[/bold bright_white]\n\n"
        "[yellow][1][/yellow] -> Listar llaves SSH\n"
        "[yellow][2][/yellow] -> Crear llave SSH\n"
        "[yellow][3][/yellow] -> Eliminar llave SSH\n"
        "[red][4][/red] -> Volver al menu principal\n"
    )
    
    panel = Panel(
    Align.center(kp_menu_options),
    title=f"[bold bright_white]Manager Key Paris[/bold bright_white]",
    border_style="Yellow",
    padding=(1, 5),
    expand=False,)

    console.print(Align.center(panel))

def print_menu_sg(sg_id):

    grid = Table(
        title=f"Operando sobre : [italic]{sg_id}[/italic]\n",
        show_header=False,
        show_edge=False,
        box=None,
        padding=(0,2)
    )

    grid.add_column("colum1")
    grid.add_column("separador")
    grid.add_column("colum2")

    grid.add_row("[blue][1][/blue]Listar reglas de entrada","[dim cyan]│[/dim cyan]","[blue][2][/blue]Listar reglas de salida")
    grid.add_row("[blue][3][/blue]Agregar regla de entrada","[dim cyan]│[/dim cyan]","[blue][4][/blue]Agregar regla de salida")
    grid.add_row("[blue][5][/blue]Eliminar regla de entrada","[dim cyan]│[/dim cyan]","[blue][6][/blue]eliminar regla de salida")
    grid.add_row("[yellow][7][/yellow]Cambiar de Security Groups","[dim cyan]│[/dim cyan]","[yellow][8][/yellow]Volver al menu Principal")

    panel = Panel(
        Align.center(grid),
        title="[bold bright_white]Manager Security Groups[/bold bright_white]",
        border_style="blue",
        padding=(1,3),
        expand=False
    )

    console.print("\n\n")
    console.print(Align.center(panel))

def print_menu_ec2():

    ec2_menu_options = Text.from_markup(
        "[green][1][/green] -> Listar instancias\n"
        "[green][2][/green] -> Desplegar instancias\n"
        "[green][3][/green] -> Iniciar instancia\n"
        "[green][4][/green] -> Reiniciar instancia\n"
        "[green][5][/green] -> Detener instancia\n"
        "[green][6][/green] -> Terminar instancia\n"
        "[yellow ][7][/yellow] -> Volver al menu principal\n")
    

    panel = Panel(
    Align.center(ec2_menu_options),
    title=f"[bold bright_white]Manager EC2[/bold bright_white]",
    border_style="green",
    padding=(1, 5),
    expand=False,
)
    console.print(Align.center(panel))

def build_metrics_budges(summary_total,widht_container_main):

    instance_on = summary_total["instance_on"]
    instance_off = summary_total["instance_off"]
    sg_total = summary_total["sg_total"]
    key_pairs_total = summary_total["key_pairs_total"]


    width_badge = widht_container_main // 3

    badge_ec2 = Panel(
        Align.center(f"[bold green]EC2:[/bold green] {instance_on} ON / {instance_off} OFF"),
        border_style="green",
        width= width_badge,
        padding=(0,0)
    )

    badge_sg = Panel(
        Align.center(f"[bold blue]SG:[/bold blue] {sg_total}"),
        border_style="blue",
        width= width_badge,
        padding=(0,0)
    )

    badge_kp = Panel(
        Align.center(f"[bold yellow]Keys:[/bold yellow] {key_pairs_total}"),
        border_style="yellow",
        width= width_badge,
        padding=(0,0)
    )

    columns_badge = Columns([badge_ec2,badge_sg,badge_kp])
    return columns_badge

def build_menu_panel(width_container_main):


    texto_opciones = Text.from_markup(
        "[green][1][/green] -> Administrar EC2\n"
        "[blue][2][/blue] -> Administrar Security Groups\n"
        "[yellow][3][/yellow] -> Administrar Key Pairs\n"
        "[cyan][4][/cyan] -> Actualizar Dashboard\n"
        "[cyan][5][/cyan] -> Cambiar de región\n"
        "[red][6][/red] -> Salir"
    )

    panel_menu = Panel(
        Align.center(texto_opciones),
        title="[bold white]Menu de Acciones AWS[/bold white]",
        border_style="cyan",
        width=width_container_main,
        padding=(1,0)
    )
    return panel_menu

def build_table_account(width_container,account_data):

    

    table_account = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        width=width_container
    )

    table_account.add_column("Account ID", justify="center", ratio=2)
    table_account.add_column("ARN", justify="center", ratio=4)
    table_account.add_column("Location Name", justify="center", ratio=2)
    table_account.add_column("Region Name", justify="center", ratio=2)
    table_account.add_row(*account_data)
    return table_account
    
def print_root_menu(account_data,summary,update_dashboard=""):

    console.clear()

    width_container = 110
    title = Text("Bienvenido a Manage AWS",style="bold cyan")
    subtitle= Text("Datos aosciados a su cuenta de AWS",style="italic gray")


    rows_badge = build_metrics_budges(widht_container_main=width_container,summary_total=summary)
    panel_menu = build_menu_panel(width_container_main=width_container)
    table_account = build_table_account(width_container=width_container,account_data=account_data)
    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print(Align.center(table_account))
    console.print(Align.center(rows_badge))
    if update_dashboard:
        console.print(Align.center(update_dashboard))
    console.print(Align.center(panel_menu))
    console.print()
