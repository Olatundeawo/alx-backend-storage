#!/usr/bin/env python3
"""
A python script that interact with mongodb
"""


def list_all(mongo_colletion):
    """ A function that lists all documents in a collection"""
    for doc in mongo_colletion.find():
        print(doc)
