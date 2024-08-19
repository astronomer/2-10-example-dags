import json

def get_adoption_data(center):
    data = {
        "center1": [
            {"date": "2022-01-01", "type": "Dog", "name": "Bingo", "age": 4},
            {"date": "2022-02-02", "type": "Cat", "name": "Bob", "age": 7},
            {"date": "2022-03-04", "type": "Fish", "name": "Bubbles", "age": 2}
        ],
        "center2": [
            {"date": "2022-06-10", "type": "Horse", "name": "Seabiscuit", "age": 4},
            {"date": "2022-07-15", "type": "Snake", "name": "Stripes", "age": 8},
            {"date": "2022-08-07", "type": "Rabbit", "name": "Hops", "age": 3}
        ]
    }
    return json.dumps(data[center], indent=4)

