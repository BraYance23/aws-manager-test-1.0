from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.align import Align
from ui.prompt_general import choice_options_table
from data.data_ec2 import AWS_REGIONS


console = Console()

def print_table_sg(title:str,list_rows:list):

    console = Console()
    
    table = Table(
        box=box.DOUBLE_EDGE,
        show_lines=True,
        header_style="bold blue"
    )
    table.add_column("#", justify="center", width=4)

    table.add_column("Group ID",justify="center", style="italic")

    table.add_column("Description", justify="center")

    for row in list_rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]Listado Security Groups[/bold bright_white]",
        border_style="blue",
        padding=(1,3),
        expand=False
    )
    console.print(Align.center(panel))

def print_regions(title_regions,rows):

    grid = Table(show_header=False, show_edge=False, box=None, padding=(0, 2))
    grid.add_column("Col1")
    grid.add_column("Separador", justify="center")
    grid.add_column("Col2")

    cols = 2
    for i in range(0, len(rows), cols):
        chunk = rows[i : i + cols]

        r1 = chunk[0]
        cell1 = f"[bold cyan][ {r1['id']:02d} ][/bold cyan] [white]{r1['region_name']:<15}[/white] [dim magenta]<{r1['location_name']}>[/dim magenta]"

        if len(chunk) > 1:
            r2 = chunk[1]
            cell2 = f"[bold cyan][ {r2['id']:02d} ][/bold cyan] [white]{r2['region_name']:<15}[/white] [dim magenta]<{r2['location_name']}>[/dim magenta]"
            grid.add_row(cell1, "[dim cyan]│[/dim cyan]", cell2)
        else:
            grid.add_row(cell1, "", "")

    panel = Panel(
        Align.center(grid),
        title=f"[bold bright_white]{title_regions}[/bold bright_white]",
        border_style="cyan",
        padding=(1, 3),
        expand=False,  
    )

    console.print(Align.center(panel))

def formate_region_name()-> tuple[list,dict]:

    rich_rows= []
    dict_region_id = {}

    for indice,(region_name,location_name) in enumerate(AWS_REGIONS.items(),start=1):  
        dict_region_id[str(indice)] = region_name
        rich_rows.append(
            {
                "id": indice,
                "region_name": region_name,
                "location_name": location_name
            }
        )

    return rich_rows,dict_region_id

def select_region_name():
     
    rich_rows,dict_region_name = formate_region_name()
    print_regions(title_regions="Regiones disponibles para administrar",rows=rich_rows)
    region_name = choice_options_table(dict_data=dict_region_name,context="de la region que desea administrar ")

    if region_name == "cancel":
        return "cancel","cancel"
    
    location_name = AWS_REGIONS[region_name]
    return region_name,location_name

def print_table_ec2(title:str,list_rows:list):
    
    table = Table(
        box=box.DOUBLE_EDGE,
        show_lines=True,
        header_style="bold cyan"
    )

    table.add_column("#", justify="center", width=4)

    table.add_column("Nombre",justify="center", style="italic")

    table.add_column("Tipo de instancia", justify="center")

    table.add_column("Estado", justify="center")

    table.add_column("Arquitectura",justify="center")

    table.add_column("ID instancia",justify="center", style="bold")

    table.add_column("IP Publica", justify="center")

    table.add_column("Fecha Despliegue",justify="center")

    for row in list_rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style="green",
        padding=(1,3),
        expand=False
    )
    console.print(Align.center(panel))

def print_table_kp(title:str,list_rows:list):

    table = Table(
    box=box.DOUBLE_EDGE,
    show_lines=True,
    header_style="bold yellow"
)

    table.add_column("#", justify="center", width=4)

    table.add_column("Name Key",justify="center")

    table.add_column("Key ID", justify="center")

    table.add_column("Fecha de creacion", justify="center")


    for row in list_rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style="yellow",
        padding=(1,3),
        expand=False
    )
    console.print(Align.center(panel))

def print_table_sg_rules(title:str,list_rows:list):
    
    table = Table(
        box=box.DOUBLE_EDGE,
        show_lines=True,
        header_style="bold blue"
    )

    table.add_column("#", justify="center")

    table.add_column("Protocolo",justify="center", style="italic")

    table.add_column("Puerto inico", justify="center")

    table.add_column("Puerto fin", justify="center")

    table.add_column("CDIR IP",justify="center", style="bold")

    table.add_column("Descripción", justify="center")

    for row in list_rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style="blue",
        padding=(1,3),
        expand=False
    )
    console.print(Align.center(panel))

def print_table_ami(list_header:list,title:str,list_rows:list):


    table = Table(
            box=box.DOUBLE_EDGE,
            show_lines=True,
            header_style="bold blue"
        )

    for header in list_header:
        table.add_column(header=header,justify="center")

    for row in list_rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style="green",
        padding=(1,3),
        expand=False
    )
    console.print(Align.center(panel))



if __name__ == "__main__":
    pass