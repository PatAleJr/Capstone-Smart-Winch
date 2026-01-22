number_of_possibilities = 0
total_steps = 10

def count(num_steps):
    global number_of_possibilities
    global total_steps
    number_of_possibilities += 1

    if (number_of_possibilities % 100 == 0):
        print(f"Number of possibilities so far: {number_of_possibilities}")

    if num_steps < total_steps:
        count(num_steps + 1)
        count(num_steps + 2)

count(0)
print(number_of_possibilities)