# Python Training

Project to improve the knowledge in Python, acquire some more proficiency with the language and trying (possible) to stop writing Java-ish python code. In addition, to play with different technologies usually outside the standard enterprise software development environments. Like AI, ML, games, cryptocurrencies ... Maybe, some DevOps or DevSecOps
automation ... Anything fits here.

More a learning playground than anything else. Code will be correct (I hope) but this does not mean it is going to be the best code or to follow the best practices.

## Exercises

* **sudoku_resolver**: Just some recursion and some general python syntax.

* **minesweeper**: A bit more recursion and general python syntax. Special attention to create/initialise structures (matrix/arrays) syntax replacing two nested for loops:
  ```python
  obj = [[None for _ in range(10)] for _ in range(10)]
  ```

* **tic_tac_toe_ia**: A Tic Tac Toe game using a Minimax algorithm. Nothing special, just for fun.

* **contact_book**: Small DB (in memory) and a bit of regexp. Special attention to the groups in regular expression. It is not the same `(,\\s)*` than `[,\\s]+` or `(,\\s)+`. First one matches groups and matches groups with `None`.
  ```python
  re.split(',(\\s)*', 'qwer,qwer,qwer,qwer') >>> ['qwer', None, 'qwer', None, 'qwer', None, 'qwer']
  
  re.split('[,\\s]+', 'qwer, qwer  ,qwer  , qwer') >>> ['qwer', 'qwer', 'qwer', 'qwer']
  
  re.split(',(\\s)+', 'qwer,qwer,qwer,qwer') >>> ['qwer,qwer,qwer,qwer']
  ```

* **subdomain_discovery**: Tool to discover subdomains for a given domain. Works with a wordlist given as argument or file. Read files, argparse, thread executor.
