class Node:
    """
    Represents a node in the maze's state graph.
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    """
    Implements a LIFO (Last-In-First-Out) frontier using a stack.
    """
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()  
            return node


class QueueFrontier(StackFrontier):
    """
    Implements a FIFO (First-In-First-Out) frontier using a queue.
    """
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)  # First in, first out
            return node


class Maze:
    """
    Class representing the maze.
    """
    def __init__(self, filename):
        # Read the file and determine the height and width of the maze
        with open(filename) as f:
            contents = f.read()

        # Validate the existence of exactly one start and one goal point
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Convert the file into a list of lines
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Initialize the maze structures
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == "#":
                        row.append(True)
                    else:
                        row.append(False)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        """
        Prints the maze with the solution if available.
        """
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")  # Represents the walls
                elif (i, j) == self.start:
                    print("A", end="")  # Represents the start point
                elif (i, j) == self.goal:
                    print("B", end="")  # Represents the goal point
                elif solution is not None and (i, j) in solution:
                    print("*", end="")  # Represents the solution path
                else:
                    print(" ", end="")  # Represents open paths
            print()
        print()

    def neighbors(self, state):
        """
        Returns the valid neighboring states from the given state.
        """
        row, col = state

        # Possible moves
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Filter valid moves
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """
        Finds a solution to the maze if it exists.
        """
        # Initialize the frontier with the start node
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Set of already explored states
        self.explored = set()

        # Search loop
        while True:
            # If the frontier is empty, no solution exists
            if frontier.empty():
                raise Exception("no solution")

            # Remove a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If the node is the goal, reconstruct the path
            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark the node as explored
            self.explored.add(node.state)

            # Add unexplored neighbors to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


# Main code to load the maze, solve it, and print it
def main():
    maze = Maze("maze1.txt")  # Make sure the file exists and has the proper format
    print("Maze:")
    maze.print()

    print("Solving...")
    maze.solve()
    print("Solution:")
    maze.print()


# Run the main code if called as a script
if __name__ == "__main__":
    main()
