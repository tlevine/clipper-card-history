#!/usr/bin/env python

def parse_page(svg):
    '''
    parse_page(lxml.etree.parse('first page'))[-2]
    >>> ('08/17/2013 06:14 PM', 'Dual-tag exit transaction, fare payment', 'Civic Center (BART)', 'BART HVD 45/48', 3.55, 11.85)
    '''
