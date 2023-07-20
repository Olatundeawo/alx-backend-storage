#!/usr/bin/env python3
"""
A python function that interact with mongodb
"""


def insert_school(mongo_collection, **kwargs):
    """A method that insert into a collection"""
    value = mongo_collection.insert_one(kwargs)
    return value.inserted_id
