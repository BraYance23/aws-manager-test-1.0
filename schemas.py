from typing import TypedDict

class DictFormatSGRules(TypedDict):

    filas_tabulate_ingress:list[list[ int | str]]
    dict_rules_egress: dict[ str,dict[ str, str | int | list[ dict[ str,str]]]]
    filas_tabulate_egress:list[list[ int | str]]
    dict_rules_ingress: dict[ str,dict[ str, str | int | list[dict[ str,str]]]]


class DictHeaderRulesSG(TypedDict):
    
    header: list[str]
    title_ingress: str
    title_egress : str