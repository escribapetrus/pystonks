from file_client import get_contents
from http_client import make_request
from flask import jsonify
from utils import update_dict
import os

def filters(x): 
    fil = [
        x.get("liquidezMediaDiaria", 0) > 100000,
        x.get("roic"),  
        x.get("eV_Ebit"),
        x.get("roic"),  
        x.get("margemEbit", 0) > 0,
        x.get("passivo_Ativo", 100) < 2,
        x.get("liquidezMediaDiaria", 0) > 100000
    ]
    if all(fil):
        return True
    else:
        return False

def apply_filters(stock_list):
    return [stock for stock in stock_list if filters(stock)]

def rank_earning_yield(stock_list):
    crit = lambda x: x.get("eV_Ebit")
    ranked = sorted(stock_list, key=crit, reverse=True)
    return [update_dict(stock, "rank_EY", ranked.index(stock)) for stock in ranked]

def rank_roic(stock_list):
    crit = lambda x: x.get("roic")
    ranked = sorted(stock_list, key=crit, reverse=False)
    return [update_dict(stock, "rank_ROIC", ranked.index(stock)) for stock in ranked]

def rank_greenblatt(stock_list):
    crit = lambda x: x.get("rank_GREENBLATT")
    updated = [update_dict(stock, "rank_GREENBLATT", stock.get("rank_EY") + stock.get("rank_ROIC")) for stock in stock_list]
    return sorted(updated, key=crit, reverse=True)

def rank(stock_list):
    return rank_greenblatt(rank_earning_yield(rank_roic(reducer(apply_filters(stock_list),{}))))
        
def reducer(stock_list, acc):
    new_acc = acc.copy()

    if stock_list == []: 
        return list(acc.values())
    else: 
        stock_in_acc = acc.get(stock_list[0]["companyName"])
        if stock_in_acc:
            if stock_in_acc["liquidezMediaDiaria"] < stock_list[0]["liquidezMediaDiaria"]:
                new_acc[stock_list[0]["companyName"]] = stock_list[0]
                return reducer(stock_list[1:], new_acc) 
            else:
                return reducer(stock_list[1:], new_acc) 
        else: 
            new_acc[stock_list[0]["companyName"]] = stock_list[0]
            return reducer(stock_list[1:], new_acc) 