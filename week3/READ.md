Values and Types

Python has different data types for storing different kinds of values. int is used for whole numbers such as 42, float is used for decimal numbers such as 3.14, str is used for text, bool stores True or False, and None represents the absence of a value. Python is dynamically typed, which means you don't have to specify the type of a variable when creating it. The type belongs to the value, not the variable name.

2. Type Conversion

Type conversion means changing a value from one data type to another. For example, int("5") converts the string "5" into the integer 5, while str(5) converts the number into the string "5". Similarly, float("3.5") converts a string into a decimal number. This is useful when data comes in as one type but your program needs another type.

3. Arithmetic Operators

Python provides operators for performing mathematical calculations. + is addition, - is subtraction, * is multiplication, / performs normal division and always gives a float, // performs floor division and gives the whole-number part, % gives the remainder, and ** is used for powers. For example, 10 / 3 gives approximately 3.33, while 10 // 3 gives 3.

4. f-Strings

An f-string is an easy way to put variables or expressions inside a string. We write f before the string and put the values inside {}. For example, f"{name} is {age}" can produce "Priya is 21". We can also perform calculations inside the braces and format numbers, such as displaying a decimal with only two digits.

5. Truthiness

Truthiness means Python can treat certain values as either true or false when used in an if condition. Values such as 0, 0.0, an empty string "", an empty list [], an empty dictionary {}, and None are considered falsy. Most other values are truthy. For example, if items: can be used to check whether a list contains something without explicitly checking its length.

6. Control Flow

Control flow determines which parts of the program execute and when. Python uses if, elif, and else to make decisions based on conditions. For example, we can check a student's marks and assign different grades depending on the value. Python also uses comparison operators such as ==, !=, <, >, <=, and >=, along with Boolean operators such as and, or, and not.

7. Indentation

Indentation is part of Python's syntax. Python does not use {} braces to define blocks of code. Instead, it uses indentation, normally four spaces, to show which statements belong to an if, loop, function, or other block. A colon : starts the block, and the following lines must be properly indented.

8. for Loop

A for loop is used when we want to repeat something for each item in a sequence. For example, for ch in "abc" goes through each character one by one. range(1, 6) produces 1, 2, 3, 4, 5; the ending value 6 is not included. enumerate() is useful when we need both the index and the value while looping.

9. while Loop

A while loop repeatedly executes code as long as its condition remains true. For example, if n starts at 3, while n > 0 can print 3, 2, and 1, while n -= 1 decreases the value each time. We must make sure the condition eventually becomes false; otherwise, the loop can continue forever.

10. break and continue

break is used to stop a loop completely, even if the loop condition is still true. continue does something different: it skips the remaining code in the current iteration and moves to the next iteration. These are useful when we need more control over how a loop behaves.

11. Functions

A function is a reusable block of code that performs a particular task. We create a function using def, give it parameters if needed, and use return to send a result back. Functions can also have default arguments, such as greeting="Hello", which means that value is automatically used when the caller doesn't provide one.

12. return and None

If a function does not contain a return statement, calling that function gives back None. return is used when we want the function to send a value back to the code that called it. Also, variables created inside a function are normally local variables, meaning they are available only inside that function.

13. Docstrings

A docstring is a string placed at the beginning of a function to describe what the function does. It is written using triple quotes such as """Return a greeting line.""". Tools and Python's help() function can read these docstrings, making them useful for documenting code.

14. Mutable Default Argument

We should be careful when using a mutable object such as a list as a function's default argument. For example, def add(item, bucket=[]): is dangerous because that same list is created once and shared between calls. Instead, we can use bucket=None and create a new list inside the function when needed.

15. Collections

Python has four important collection types: list, tuple, set, and dictionary. A list is ordered and changeable, so it is useful for a sequence of items. A tuple is ordered but cannot be changed, so it is useful for fixed data. A set is useful when we need unique values or fast membership checking. A dictionary stores values using keys, making it useful when we need to look something up by a key.

16. Lists

A list stores multiple values in an ordered and changeable collection. We can add items using append(), sort the list using sort(), access the first item using index 0, access the last item using -1, and get a portion of the list using slicing. For example, [3, 1, 2] can be changed into [1, 2, 3] using sort().

17. Dictionaries

A dictionary stores data as key-value pairs. For example, {"name": "Priya", "role": "intern"} has name and role as keys. We can access a value using its key, add new key-value pairs, and use .get() when we want to safely retrieve a value that may not exist. .items() allows us to loop through both keys and values.

18. List Comprehension

A list comprehension provides a short way to create a new list from another sequence. For example, [n * n for n in range(5)] creates a list containing the squares of numbers from 0 to 4. We can also add a condition, such as [n for n in range(10) if n % 2 == 0], to create a list containing only even numbers.

19. Input and Output

The input() function is used to receive information from the user, and it always returns a string. If we need a number, we must convert the result using something like int(input()). The print() function displays output on the screen, and we can control how multiple values are separated using the sep argument.

20. Working with Files

Python can read from and write to files using the open() function. The recommended approach is to use a with block because Python automatically closes the file after the block finishes, even if an error occurs. For example, "w" mode can write data to a file, while the default reading mode can read the file's contents.

21. JSON

JSON is a common format for storing and exchanging structured data. Python provides the built-in json module for working with JSON files. json.dump() can save Python data such as dictionaries and lists into a JSON file, while json.load() reads the JSON file and converts it back into Python data.

22. Handling Errors

An exception is an error that interrupts normal program execution. Python provides try and except to handle errors instead of allowing the program to crash. else runs when no exception occurs, while finally runs regardless of whether an exception happened. We can also use raise to deliberately create an exception when a particular condition occurs.

23. Common Exceptions

Python has different exception types for different problems. ValueError happens when a value has the wrong content, TypeError happens when an operation receives an inappropriate type, KeyError occurs when a dictionary key is missing, IndexError occurs when a list index doesn't exist, FileNotFoundError occurs when a requested file cannot be found, and ZeroDivisionError occurs when we try to divide by zero.

24. Specific Exception Handling

We should catch specific exceptions instead of using a general except:. For example, if converting user input into an integer, we can catch ValueError. Catching only the expected error makes debugging easier because unexpected programming errors are not silently hidden.

25. Structuring a Python Project

A Python project can be divided into multiple files based on responsibility. For example, main.py can contain the main program while storage.py contains functions for loading and saving data. We can import functions from one file into another, which makes a larger project easier to understand and maintain.

26. Virtual Environment

A virtual environment (venv) creates an isolated Python environment for a project. We can install packages inside that environment without affecting other projects on the computer. Each project can therefore use its own versions of libraries, which prevents dependency conflicts between projects.

27. requirements.txt

requirements.txt records the Python packages and their versions required by a project. After installing packages in a virtual environment, pip freeze > requirements.txt can save the installed versions. Another person can then use pip install -r requirements.txt to install the same dependencies for the project.

28. .gitignore

A .gitignore file tells Git which files and folders should not be committed to the repository. For Python projects, .venv/ and __pycache__/ should normally be ignored because they contain local environment files and generated Python cache files rather than source code.

29. Open Source

Open source means the source code is publicly available and can generally be viewed, modified, and shared according to its licence. Open source often means software is available without a purchase price, but "open source" and "free of charge" are not exactly the same thing. A licence defines what users are allowed to do with the software.
