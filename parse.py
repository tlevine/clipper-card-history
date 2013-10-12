#!/usr/bin/env python
import re
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

def clean_row(row):
    '''
    >>> type(clean_row(['08/17/2013 06:14 PM', 'Dual-tag exit transaction, fare payment', 'Civic Center (BART)', 'BART HVD 45/48', '3.55', '11.85']))
    dict
    '''
    columns = ['datetime','transaction.type','location','product','debt.or.credit','balance']
    return dict(zip(columns, row))

def go(svg):
    return map(clean_row, parse_page(svg))
