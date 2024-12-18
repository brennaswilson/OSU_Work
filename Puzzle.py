import heapq


def solve_puzzle(Board, Source, Destination):
    # number of rows
    m = len(Board)

    # number of columns
    n = len(Board[0])

    # source row/column
    source_row, source_column = Source

    # destination row/column
    destination_row, destination_column = Destination

    # direction
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbor_dict = {(0, 1): 'R', (0, -1): 'L', (1, 0): 'D', (-1, 0): 'U'}

    # initialize queue with source
    min_p_queue = [(0, source_row, source_column)]

    # track effort in dictionary, add 0,0
    effort_dict = {(source_row, source_column): 0}

    previous_dict = {}

    path = []
    directions = []

    if Source == Destination:
        return [Source], ""

    # while min_p_queue still has something to check
    while min_p_queue:

        effort, row, column = heapq.heappop(min_p_queue)

        if row == destination_row and column == destination_column:
            current_node = Destination
            while current_node in previous_dict:
                path.insert(0, current_node)
                current_node, direction = previous_dict[current_node]
                directions.insert(0, direction)

            path.insert(0, Source)
            return path, "".join(directions)

        # check each valid neighbor
        for x, y in neighbors:
            new_row = row + x
            new_column = column + y
            if 0 <= new_row < m and 0 <= new_column < n:
                if Board[new_row][new_column] == '-':
                    new_effort = effort + 1
                    if (new_row, new_column) not in effort_dict or new_effort < effort_dict[(new_row, new_column)]:
                        effort_dict[(new_row, new_column)] = new_effort
                        direction = neighbor_dict[(x, y)]
                        previous_dict[(new_row, new_column)] = ((row, column), direction)
                        heapq.heappush(min_p_queue, (new_effort, new_row, new_column))

    return None
