# Main Guidelines
- Use python type hinting in every function and class, including return types.
- Always use docstrings for Classes and Functions/Methods.
- Always prefer double-quotes rather than single quotes.
- Adhere as close as possible to google style docstrings, auto-generated documentation is dependent on it and a merge request will not make it into dev if they are missing.
- Always indent with 4 spaces, no more, no less.
- Naming of classes should always be CamelCase and functions should be snake_case.
- Never raise exceptions from the base Exception, write custom ones if required.

# Other Guidelines
- Minimum version of Python to use during development and testing must be 3.11.
- Always use f-strings when possible as they are far more superior than % and .format() in most cases.
- Always write tests for any new functions/API calls implemented or changed (if the logic has changed).
- List comprehensions should always be used where possible unless the code is too ugly and readable, that is for you and the reviewer to agree with :-)