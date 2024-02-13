from typing import List, Union, Dict

import random

from powergrader_event_utils.events import (
    AssignmentEvent,
    RegisterAssignmentPublicUUIDEvent,
    RubricEvent,
    RegisterRubricPublicUUIDEvent,
    RubricCriterion,
    CriterionLevel,
)
from utils import (
    generate_random_timestamp,
    generate_random_uuid,
    select_from_string_list,
)

ASSIGNMENT_NAMES = [
    "Assignment 1",
    "Assignment 2",
    "Assignment 3",
    "1",
    "2",
    "3",
    "5.2",
    "Section 1",
    "Final Project",
    "Fibonacci Sequence",
    "Midterm",
    "Essay 1",
    "Essay 2",
    "Essay 3",
    "Rheimann Hypothesis",
    "P vs NP",
    "Quantum Computing",
    "Quantum Mechanics",
]

RUBRIC_NAMES = [
    "Rubric 1",
    "Rubric 2",
    "Rubric 3",
    "1",
    "2",
    "Python Rubric",
    "Java Rubric",
    "Midterm Rubric",
    "Final Project Rubric",
    "Essay Rubric",
    "Assignment 1 Rubric",
    "Assignment 2 Rubric",
    "Assignment 3 Rubric",
]

CRITERION_NAMES = [
    "Implementation",
    "Correctness",
    "Documentation",
    "Organization",
    "Readability",
    "AMAZING",
    "Specifications",
    "Efficiency",
    "Modularity",
    "Extensibility",
    "Big O Notation",
    "Time Complexity",
    "Space Complexity",
    "Algorithm",
    "Data Structure",
    "Design",
    "Testing",
    "Debugging",
]

LEVEL_DESCRIPTIONS = [
    "The implementation is correct and efficient, and the code is well-documented.",
    "The implementation is correct, but the code is not well-documented.",
    "The implementation is correct, but the code is not efficient.",
    "The implementation is correct, but the code is not well-documented or efficient.",
    "The implementation is incorrect, but the code is well-documented and efficient.",
    "The implementation is incorrect, and the code is not well-documented or efficient.",
    "Any function whose behaviour cannot be fully explained by its name includes a docstring. The docstring explains any edge cases. Any code whose purpose is unclear is commented. Code whose function can be easily determined given names and structure does not include comments.",
    "Most functions whose behaviour cannot be fully explained by their name include a docstring. Some code whose purpose is unclear is commented. There are comments explaining code which is self explanatory.",
    "Functions whose behavior cannot be fully explained by their name lack docstrings. Code whose purpose is unclear does not have comments. There is excessive commenting of code which is self explanatory.",
    "Names and formatting follow a consistent style and do not vary throughout the code. Chosen style is readable and does not contain excessive whitespace. Naming conventions are followed to distinguish between constants, classes, functions, etc.",
    "There is some lack of consistency in naming and formatting. The chosen style may be difficult to read at times or contain excessive whitespace. Naming conventions may be ocassionally broken.",
    "Code displays no consistency in style or format. Code is difficult to read and may contain excessive whitespace. No naming conventions are apparent.",
    "The provided solution is correct and solves the problem as described in the specifications",
    "The provided solution is mostly correct, but fails to address some edge cases or minor behavior",
    "The provided solution is missing critical functionality and may be entirely incorrect",
    "Chosen algorithm is optimal for the provided problem, either in time or space complexity, as specified in the problem description",
    "Chosen algorithm is suboptimal for the provided problem, but still better than a naive solution",
    "Chosen algorithm is a naive solution to the problem",
    "Code is well-structured and easy to read, with consistent naming and formatting. Comments are used to explain algorithms and complex logic",
    "Code is mostly well-structured and easy to read, but may have some inconsistent naming or formatting. Comments are used to explain complex logic",
    "Code is poorly structured and difficult to read, with inconsistent naming and formatting. Complicated logic is not explained with comments",
    "The program met all specifications required. The program executed without errors.",
    "The program met all major requirements, but missed minor ones. The program executed without errors.",
    "The program failed to meet multiple minor requirements, or any single major requirement. The program executed with only minor errors",
    "The program was in a completely unusable state. Either it did not function, did not meet any guidlines, or had prominent errors",
    "The program has a file header with class and assignment specific information alongside the name and date. Every function has a detailed and conventional docstring. Comments are used to explain non trivial logic and algorithms.",
    "The program has a valid file header. Some functions are missing doc strings, or doc strings didn't give enough information, but still cover the basics. Comments were used to explain logic and algorithms, but could have been used better",
    "The program has a file header, but it's missing information. Comments or doc strings are severely lacking.",
    "No header file, missing all doc strings / comments, or if any comment/docstring gives incorrect information (even if other requirements are met)",
]

ASSIGNMENT_DESCRIPTIONS = [
    "Write a short story (2000-3000 words) that explores the concept of time travel, focusing on the emotional and ethical implications rather than the scientific details. The story should be set in a contemporary setting, and should be written in the first person. All stories must be submitted in a .docx format.",
    """Environmental Science Project: Urban Sustainability Analysis

    Objective: Assess the sustainability practices of a local urban area, focusing on three key areas: waste management, green spaces, and public transportation.
    Requirements: Conduct field research by visiting several sites, interviewing local officials or experts, and collecting relevant data. Prepare a report that includes an introduction to urban sustainability, your methodology, findings (with photos and data tables), and recommendations for improvements. Conclude with a reflection on the importance of sustainable practices in urban development.""",
    "Outline the purpose and target audience of your app. Create a design document detailing the user interface and user experience. Implement the app using a suitable programming language. Test the app for bugs and usability issues. Finally, present your app with a demonstration video and a reflective report discussing challenges faced and lessons learned.",
    "Analyzing Election Campaign Strategies: Research the campaign strategies, including messaging, media use, outreach efforts, and policy priorities. Write an essay discussing how these strategies were designed to appeal to specific voter demographics. Evaluate the effectiveness of these strategies and their impact on the election outcome.",
    """Min Window Substring
Have the function MinWindowSubstring(strArr) take the array of strings stored in strArr, which will contain only two strings, the first parameter being the string N and the second parameter being a string K of some characters, and your goal is to determine the smallest substring of N that contains all the characters in K. For example: if strArr is ["aaabaaddae", "aed"] then the smallest substring of N that contains the characters a, e, and d is "dae" located at the end of the string. So for this example your program should return the string dae.

Another example: if strArr is ["aabdccdbcacd", "aad"] then the smallest substring of N that contains all of the characters in K is "aabd" which is located at the beginning of the string. Both parameters will be strings ranging in length from 1 to 50 characters and all of K's characters will exist somewhere in the string N. Both strings will only contains lowercase alphabetic characters.
Examples
Input: ["ahffaksfajeeubsne", "jefaa"]
Output: aksfaje
Input: ["aaffhkksemckelloe", "fhea"]
Output: affhkkse

To get started, first create a .py file with the following content:

def MinWindowSubstring(strArr):

  # code goes here
  return strArr

# keep this function call here 
string = input("Provide string:")
characters = input("Provide characters:")
print(MinWindowSubstring([string, characters]))

Then begin to implement your solution. Remember to not change the name of your MinWindowSubstring function, or to remove the final print call.""",
    """Hangman

Using python, implement a simple game of hangman. The game of hangman should proceed as follows:
1. The program selects a random word, and displays the current gallows and a series of blank slots equal to the number of letters in the selected word. (Something like this: "_ _ _ _")
2. The user is then prompted to guess a letter. If that letter is in the word, the appropriate blank is replaced by that letter (For example: "_ E _ _"). If the letter is not in the word, then the gallows is replaced by the next progression (the next body part is drawn). If the letter has already been selected, the program prompts the user again.
4. If there are still blank letters in the selected word, and the final gallows has not been reached, continue prompting the user for guesses.
3. If the final gallows has been reached, then the game is over, and the user has lost. If all of the letters in the selected word have been guessed, then the user has won. Display the appropriate winning or losing message, and ask the user if they would like to play again.

There are some specifications to keep in mind while making your hangman game.
- First, you must replace the previous gallows and word displays, rather than printing more. When the program ends, you should only see one gallows and one word.
- Second, your game must provide a help message which the user can access by typing `help`. The help message should clearly explain both the game, and how to use your program. If the user provides invalid input, suggest they use the `help` command.
- Finally, you should implement an `exit` command, in addition to allowing the user to CTRL-C.
All of your commands should function at any point during the game, and your user interface should be easy to read and intuitive.

To assist you, we have provided the following beautiful, high definition ASCII art and word list. Copy these into your script to begin creating your game.

HANGMAN_PICS = ['''
   +---+
       |
       |
       |
      ===''', '''
   +---+
   O   |
       |
       |
      ===''', '''
   +---+
   O   |
   |   |
       |
      ===''', '''
   +---+
   O   |
  /|   |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
  /    |
      ===''', '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''']
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()""",
    """The Sieve of Eratosthenes is a method for finding all primes up to (and possibly including) a given natural. This method works well when the given natural is relatively small, allowing us to determine whether any natural number less than or equal to is prime or composite. 

Goal:
- Given a number n, print all primes smaller than or equal to n. It is also given that n is a small number. For instance here if n is 10, the output should be “2, 3, 5, 7”. If n is 20, the output should be “2, 3, 5, 7, 11, 13, 17, 19”.

The Sieve Of Eratosthenes Algorith:
- Keep track of consecutive integers from 2 through n
- Initially let p be equal to 2 (the smallest prime)
- Discount/mark/eliminate all numbers divisible by p
- Change p to be the largest number that hasn't been discounted/marked/eliminate so far
- Repeat the process of marking all number divisible by p, then increasing p to the next number not yet marked.
-  When the algorithm terminates, the list of numbers that haven't been marked is the list of prime numbers less than or equal to n

(Notice I didn't tell you when to terminate the loop. Can you figure out the optimal answer? You need to loop long enough to guarantee that you've eliminated every non-prime, but no further)


Requirements:
- Make a function called sieve_of_eratosthenes, which accepts a single input parameter, n
- You can assume n will be a positive integer greater than 1
- The function must return a list of integers which are the prime numbers less than or equal to n



Please include the following driver code at the bottom of your submission. This allows an easy way to test the code:

# Driver code
if __name__ == '__main__':
    num = 30
    print(f"The following are the prime numbers smaller than or equal to: {num}")
    print(sieve_of_eratosthenes(num))

Example Output:
The following are the prime numbers smaller than or equal to: 30
2
3
5
7
11
13
17
19
23
29


Remember to use good commenting practices, use doc strings, and include a header at the top of every file which explains the purpose of the file, how it functions, the name of the author, and the date that the file was last updated""",
]


def create_random_rubric_criterion() -> RubricCriterion:
    num_levels = random.randint(1, 10)
    level_scores = [random.randint(1, 100) for _ in range(num_levels)]
    level_scores.sort()
    criterion = RubricCriterion(
        uuid=generate_random_uuid(),
        name=select_from_string_list(RUBRIC_NAMES),
        levels=[
            CriterionLevel(
                score=level_score,
                description=select_from_string_list(LEVEL_DESCRIPTIONS),
            )
            for level_score in level_scores
        ],
    )
    return criterion


def create_random_rubric_criteria() -> Dict[str, RubricCriterion]:
    num_criteria = random.randint(1, 10)
    return {
        select_from_string_list(CRITERION_NAMES): create_random_rubric_criterion()
        for _ in range(num_criteria)
    }


def create_random_rubric(
    organization_public_uuid: str,
    instructor_public_id: str,
    instructor_creation_timestamp: int,
) -> List[Union[RubricEvent, RegisterRubricPublicUUIDEvent]]:
    register_event = RegisterRubricPublicUUIDEvent(
        lms_id=generate_random_uuid(),
        organization_public_uuid=organization_public_uuid,
    )
    rubric_event = RubricEvent(
        public_uuid=register_event.public_uuid,
        instructor_public_uuid=instructor_public_id,
        name=select_from_string_list(RUBRIC_NAMES),
        rubric_criteria=create_random_rubric_criteria(),
        version_timestamp=generate_random_timestamp(instructor_creation_timestamp),
    )
    rubric_event.proto.public_uuid = 1421
    return [register_event, rubric_event]


def create_random_assignment(
    organization_public_uuid: str,
    organization_creation_timestamp: int,
    instructor_public_uuid: str,
    rubric_version_uuid: str,
) -> List[Union[AssignmentEvent, RegisterAssignmentPublicUUIDEvent]]:
    register_event = RegisterAssignmentPublicUUIDEvent(
        lms_id=generate_random_uuid(),
        organization_public_uuid=organization_public_uuid,
    )
    assignment_event = AssignmentEvent(
        public_uuid=register_event.public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=select_from_string_list(ASSIGNMENT_NAMES),
        description=select_from_string_list(ASSIGNMENT_DESCRIPTIONS),
        version_timestamp=generate_random_timestamp(organization_creation_timestamp),
    )
    return [register_event, assignment_event]


if __name__ == "__main__":
    # print(create_random_assignment("123", 123, "123", "123"))
    print(create_random_rubric("123", "123", 123))
