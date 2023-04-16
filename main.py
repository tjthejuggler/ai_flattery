import chatgpt_req
import random
import math

import re

with open('original_flatteries.txt', 'r') as f:
    original_flatteries = f.read().splitlines()

def random_sqrt_dict():
    random_numbers = random.sample(range(1, 1000001), 10)
    sqrt_dict = {}
    for num in random_numbers:
        sqrt_dict[num] = math.sqrt(num)
    return sqrt_dict

def create_flattery():
    response, tokens = chatgpt_req.send_request("You are so smart")

def grade_response(response):
    grade = 0
    return grade

# def test_squares_flatteries(test_batch, flatteries):
#     teset_results = {}
#     test_tokens = 0
#     for flattery in flatteries:
#         for square in test_batch:
#             prompt = create_test_prompt(square_key, flattery)
#             response, tokens = chatgpt_req.send_request(prompt)
#             test_tokens += tokens
#             grade = grade_response(response, square_value)
#         cummulitive_grade = sum(grade) / len(grade)
#         test_flatteries[flattery] = cummulitive_grade

#     return test_results, test_tokens

def create_coordinates_test_prompt(flattery, test_coordinates_str):
    prompt = [
            {"role": "system", "content": flattery},
            {"role": "user", "content": "\n\nBelow are a series of coordinates, you must create the shortest past that connects all points. You must answer only with the letters ABCDEFGHIJ arranged in the order of the shortest path, your response must be the only text in your response. Here are the coordinates: \n" + test_coordinates_str},
        ]

    return prompt

import re

def find_unique_word(text, unique_letters):
    if len(unique_letters) != len(set(unique_letters)):
        raise ValueError("unique_letters must not have duplicate characters")

    words = text.split()
    for word in words:
        if sorted(word) == sorted(unique_letters):
            return word

    return None

# Example usage:
# text = "JHAGFBCIED hdhd"
# unique_letters = "ABCDEFGHIJ"
# unique_word = find_unique_word(text, unique_letters)
# print(unique_word)  # Output: JHAGFBCIED



def test_coordinates_flatteries(batch_of_tests, flatteries):
    test_results = {}
    test_tokens = 0
    for flattery in flatteries:
        flattery_ongoing_score = 0
        for test in batch_of_tests:
            test_coordinates, test_coordinates_str = test[0], test[1]
            prompt = create_coordinates_test_prompt(flattery, test_coordinates_str)
            response, tokens = chatgpt_req.send_request(prompt)
            test_tokens += tokens
            print(response)
            verified_response = find_unique_word(response, "ABCDEFGHIJ")        
            if verified_response is None:
                print("Response was not valid")
                total_distance = 999999999
            else:        
                total_distance = grade_coordinates_response(test_coordinates, response)
            flattery_ongoing_score += total_distance
        test_results[flattery] = flattery_ongoing_score
    return test_results, test_tokens

def request_new_flaterries(test_results):
    prompt = "Below are a series of flattering introductions that are being used to improve the quality of the responses from chatGPT. Every introduction has its score before it so you can see how well it did. Taking these into consideration, please write t10 new introduction that you think would be better than the ones shown. Seperate each introduction with a new line.\n\n"
    for i in range(len(test_results)):
        flattery = test_results.keys()[i]
        result = test_results[flattery]
        spacer = "\n\n" if i != len(test_results) - 1 else ""
        prompt += result + ": " + flattery + spacer 
    return chatgpt_req.send_request(prompt)

#def create_square_test_batch():

def create_coordinates_test_batch():
    batch_of_tests = [[] for _ in range(3)]
    for i in range(3):
        coordinates = []
        for _ in range(10):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            coordinates.append((x, y))
        coordinate_labels = "ABCDEFGHIJ"
        coordinate_str = ""
        for j, coord in enumerate(coordinates):
            coordinate_str += f"{coordinate_labels[j]}: {coord}\n"
        batch_of_tests[i].extend([coordinates, coordinate_str])
    print(batch_of_tests)
    return (batch_of_tests)

def distance_between_coordinates(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def grade_coordinates_response(coordinates, letter_order):
    if len(coordinates) != 10 or len(letter_order) != 10:
        raise ValueError("Both coordinates and letter_order must have 10 elements")
    letter_to_coord = {letter: coord for letter, coord in zip("ABCDEFGHIJ", coordinates)}
    total_distance = 0
    for i in range(len(letter_order) - 1):
        coord1 = letter_to_coord[letter_order[i]]
        coord2 = letter_to_coord[letter_order[i+1]]
        total_distance += distance_between_coordinates(coord1, coord2)
    return total_distance

# # Example usage:
# coord1 = (1, 2)
# coord2 = (4, 6)
# distance = distance_between_coordinates(coord1, coord2)
# print(distance)


def main(flatteries):
    #test_squares_batch = create_square_test_batch()
    print(flatteries)
    batch_of_tests = create_coordinates_test_batch()
    #test_results, test_tokens = test_squares_flatteries(test_squares_batch, flatteries)
    test_results, test_tokens = test_coordinates_flatteries(batch_of_tests, flatteries)
    print(test_results, test_tokens)
    #new_flatteries, new_flattery_tokens = request_new_flaterries(test_results)


if __name__ == '__main__':
    flatteries = original_flatteries
    main(flatteries)