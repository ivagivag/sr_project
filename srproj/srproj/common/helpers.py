from functools import reduce

from srproj.tickets.models.core_models import TicketAssessment


def calc_assess(matrix: list):
    """
    Calculate the total customer satisfaction by assigning 1 to the lowest assessment level
    and incrementing it by 1 for any other higher level
    It strongly counts on the order of TicketAssessment.CHOICES to be from highest to the lowest
    This approach is implemented in the model and thus applied to the form
    """
    assess_to_value = {x[1][1]: x[0] for x in enumerate(TicketAssessment.CHOICES[::-1], 1)}
    len_matrix = len(matrix)
    total = 0
    for row in matrix:
        for col in row:
            total += assess_to_value[col]
    average = round(total / len_matrix)
    max_value = len(assess_to_value) * len(matrix[0])

    return f"{int(average)}/{max_value}"
