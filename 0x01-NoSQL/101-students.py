#!/usr/bin/env python3
"""
A python file that interact with mongodb
"""


def top_students(mongo_collection):
    """ A method that sort students base on average score"""
    average_score = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return average_score
