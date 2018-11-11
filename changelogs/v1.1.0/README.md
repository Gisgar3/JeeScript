# Changelog
### Local Debugging
* Debugging of **JeeScript** files can be done using the ``MODE DEBUG`` line at the end of the file.
### Interpreter
* Relabeled sections of interpreter-file.
* Renamed interpreter-file from ``lexer.py`` to ``interpreter.py``; ``interpreter.py`` includes the lexer, parser, and correction functions.
* Changed ``if`` statement for the debugging mode to ``elif`` to prevent command-prompt errors from occurring.
* Made the interpreter check the file being executed to see if it's a compatible **JeeScript** file.
* Added the ``funcdata`` variable for use collecting function information.
### Command-Prompt/Terminal
* Debugging can now be enabled via the command-prompt by adding ``DEBUG`` to the end of the arguments. This is the equivalent to adding ``MODE DEBUG`` within a **JeeScript** file, but this method is less-dependent on when the tokens are added to the interpreter.
### Functions
* **JeeScript's** interpreter now comes with a built-in function that can be used by typing ``LOAD`` or ``load``. This function allows developers to load separate **JeeScript** files programmatically for execution.