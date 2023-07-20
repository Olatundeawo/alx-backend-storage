#!/usr/bin/env python3
"""
A python script that interact with mingodb
"""


def schools_by_topic(mongo_collection, topic):
    """A method that returns the list
       of school having a specific topic
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
