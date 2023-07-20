#!/usr/bin/env python3
"""
A python function that interact with mongodb
"""


def update_topics(mongo_collection, name, topics):
    """A method that changes some attribute
       in a coolection
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
