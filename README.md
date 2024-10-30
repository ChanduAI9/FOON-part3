
# Monte Carlo Tree Search (MCTS) for Task Planning

This project implements Monte Carlo Tree Search (MCTS) to extract a task tree from a Functional Object-Oriented Network (FOON).

## How to Run the Program

1. Ensure you have Python 3.x installed on your system.

2. Clone or download this project to your local machine.

3. Input files are available in the same directory as the program:
   - `FOON.txt`
   - `kitchen.txt`
   - `motion.txt`

4. Navigate to the directory containing the project files in your terminal or command prompt.

5. Run the MCTS algorithm using the following command:
   ```
   python mcts_algorithm.py
   ```

6. The output task tree will be printed to the console and saved in the file `mcts_task_tree.txt`.

### Running Tests

1. To validate the MCTS functionality, run the following command:
   ```
python -m unittest discover -s . -p "test_script.py"
   ```

2. The test results will be displayed in the console.
