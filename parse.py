#!/usr/bin/env python
import re
import datetime

import lxml.etree
NS = { 'svg': 'http://www.w3.org/2000/svg' }

def parse_page(svg):
    '''
    parse_page(lxml.etree.parse('first page'))[-2]
    >>> ['08/17/2013 06:14 PM', 'Dual-tag exit transaction, fare payment', 'Civic Center (BART)', 'BART HVD 45/48', '3.55', '11.85']

    >>> set(map(len, parse_page(lxml.etree.parse('first page'))))
    set([5])
    '''
    g = svg.xpath('//svg:tspan[text()="TRANSACTION TYPE"]/../..', namespaces = NS)[0]
    cells = g.xpath('svg:text', namespaces = NS)
    header = cells[:7]
    body = [cell.xpath('string()') for cell in cells[7:]]
    a, b = reduce(add_cell, body, ([], []))
    return a

def add_cell(data, cell):
    completed_rows, partial_row = data
    if re.match(r'^\d\d/\d\d/2013 \d\d:\d\d [AP]M$', cell):
        return (completed_rows + [partial_row], [cell])
    else:
        return (completed_rows, partial_row + [cell])

def clean_row(rowlist):
    '''
    >>> type(clean_row(['08/17/2013 06:14 PM', 'Dual-tag exit transaction, fare payment', 'Civic Center (BART)', 'BART HVD 45/48', '3.55', '11.85']))
    dict
    '''
    columns = ['datetime','transaction.type','location','product','debt.or.credit','balance']
    better_rowlist = rowlist[:4] + ['0'] + rowlist[4:] if len(rowlist) == 5 else rowlist

    rowdict = dict(zip(columns, better_rowlist))
    rowdict['datetime'] = datetime.datetime.strptime(rowdict['datetime'], '%m/%d/%Y %I:%M %p')
    rowdict['debt.or.credit'] = float(rowdict['debt.or.credit'])
    rowdict['balance'] = float(rowdict['balance'])
    return rowdict

def go(svg):
    rows = filter(lambda row: len(row) > 0, parse_page(svg))
    return map(clean_row, rows)
