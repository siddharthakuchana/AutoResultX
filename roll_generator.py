def generate_roll_numbers(base_roll, start, end):
    return [base_roll + str(i).zfill(2) for i in range(start, end + 1)]
