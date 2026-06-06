from colorama import init,Style,Fore

VERSION_OS = {
            "Ubuntu": {
    "20.04 LTS": {
        "owner": "099720109477",
        "filter": "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"
    },
    "22.04 LTS": {
        "owner": "099720109477",
        "filter": "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    },
    "24.04 LTS": {
        "owner": "099720109477",
        "filter": "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    }
},
                "Windows": {
                    "2019":  {"owner": "amazon", "filter": "Windows_Server-2019*"},
                    }
                }

AWS_REGIONS = {
    "us-east-1": "N. Virginia",
    "us-east-2": "Ohio",
    "us-west-1": "N. California",
    "us-west-2": "Oregon",
    "ap-south-1": "Mumbai",
    "ap-northeast-3": "Osaka",
    "ap-northeast-2": "Seoul",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Sydney",
    "ap-northeast-1": "Tokyo",
    "ca-central-1": "Central",
    "eu-central-1": "Frankfurt",
    "eu-west-1": "Ireland",
    "eu-west-2": "London",
    "eu-west-3": "Paris",
    "eu-north-1": "Stockholm",
    "sa-east-1": "São Paulo"
    }

TYPES_INSTANCES = [

    ["1", "t3.nano", 2, "0.5 GB", "$0.0052", "~$3.74", "✓ Free Tier"],
    ["2", "t3.micro", 2, "1 GB", "$0.0104", "~$7.49", "✓ Free Tier"],
    ["3", "t3.small", 2, "2 GB", "$0.0208", "~$14.98", "✓ Free Tier"],
    ["4", "t3.medium", 2, "4 GB", "$0.0416", "~$29.95", ""],
    ["5", "c5a.large", 2, "4 GB", "$0.077", "~$55.44", ""],
    ["6", "t3.large", 2, "8 GB", "$0.0832", "~$59.90", ""],
    ["7", "c7i-flex.large", 2, "4 GB", "$0.0848", "~$61.06", "✓ Free Tier"],
    ["8", "m7i-flex.large", 2, "8 GB", "$0.0958", "~$68.98", "✓ Free Tier"],
    ["9", "c5a.xlarge", 4, "8 GB", "$0.154", "~$110.88", ""],
    ["10", "t3.xlarge", 4, "16 GB", "$0.1664", "~$119.81", ""],
    ["11", "c5a.2xlarge", 8, "16 GB", "$0.308", "~$221.76", ""],
    ["12", "t3.2xlarge", 8, "32 GB", "$0.3328", "~$239.62", ""],
    ["13", "c5a.4xlarge", 16, "32 GB", "$0.616", "~$443.52", ""],
    ["14", "c5a.12xlarge", 48, "96 GB", "$1.848", "~$1,330.56", ""],
    ["15", "c5a.24xlarge", 96, "192 GB", "$3.696", "~$2,661.12", ""]
]


OS_AVALIBLE = [
    ["1","Amazon Linux","x86_64"],
    ["2","Ubuntu","x86_64"],
    ["3","Windows","x86_64"],
    ["4","Red Hat","x86_64"],
    ["5","SUSE Linux","x86_64"],
    ["6","Debian","x86_64"]
]

dict_type_instances = {sub[0]:sub[1] for sub in TYPES_INSTANCES}

dict_os_general = {sub[0]:sub[1] for sub in OS_AVALIBLE}

headers_types_ec2 =  {"header": [Style.BRIGHT + Fore.CYAN + "Indice",
                                 "Instancia",
                                 "vCPU","RAM",
                                 "$/hora",
                                 "$/mes",
                                  "Free trier" + Style.RESET_ALL],
                    "title": "Tipos de instancias disponibles y costes"}


header_region_name = {"header" :["INDICE",
                                     "Location Name",
                                     "Region ID"],
                     "title": "Regiones disponibles para administrar"}


header_key_pair = {"header" : [Style.BRIGHT + Fore.CYAN + "ID list",
                      Style.BRIGHT + Fore.CYAN + "Key name",
                      Style.BRIGHT + Fore.CYAN + "Key Pair ID",
                      Style.BRIGHT + Fore.CYAN +"Create Time" + Style.RESET_ALL],
                  "title": "Llaves SSH existentes"}

header_sg = {"header":  ["INDICE",
                        "Group ID",
                        "Descripcion"],
            "title":    "Grupos de seguridad existentes"}


header_rules_sg = {"header" : [Style.BRIGHT + "INDICE",
                                "Protocolo",
                                "Puerto inicio",
                                "Puerto fin",
                                "Cdir IP",
                                "Descripción" + Style.RESET_ALL],
                    "title": "Reglas de entradas existentes: "}

header_ec2 = {"header" : [Style.BRIGHT +"INDICE",
                          "Nombre EC2",
                          "Tipo de instancia",
                          "Estado","Arquitectura",
                          "ID instancia",
                          "IP publica","SG ID",
                          "Fecha de lanzamiento" +Style.RESET_ALL],
            "title": "listado y descripcion de instancias :"}


header_os_general = {"header" :["INDICE",
                                "DISTRO",
                                "ARQUITECTURA"],
                    "title": "Selecciones el tipo de sistema operativo que desea desplegar :"}

header_os_version = {"header":["INDICE",
                                    "Distros",
                                    "Arquictectura",
                                    "Distribuidor"],
                     "title": "Versiones del sistema operativo seleccionado : "}

header_selected_ami = {"header": ["INDICE",
                                      "ID AMI",
                                      "Name ",
                                      "Architecture",
                                      "Free tier",
                                      "Date creation"],
                      "title": "AMIS disponible :"}


main_aws = {"1": "Administrar EC2",
            "2": "Administar Security Groups",
            "3": "Administar Key Pairs",
            "4": "Cambiar de region",
            "5": "Salir"}

main_ec2 = {"1": "Listar instancias",
            "2": "Desplegar instancia",
            "3": "Iniciar instancia",
            "4": "Reiniciar instancia",
            "5": "Detener instancia",
            "6": "Terminar instancia",
            "7": "Volver al menu principal"}

main_sg = {"1": "Listar reglas de entrada",
           "2": "Agregar regla de entrada",
           "3": "Eliminar regla de entrada",
           "4": "Cambiar grupo de seguridad",
           "5": "Volver al menu principal"}

main_key_pair = {"1": "Listar llaves SSH",
                 "2": "Crear llave SSH",
                 "3": "Eliminar llave SSH",
                 "4": "Volver al menu principal"}



if __name__ == "__main__":
    pass