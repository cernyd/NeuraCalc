from exercise import ExerciseGenerator

gen = ExerciseGenerator()


for e in gen:
    print(f"--- SET {gen.curr_set+1} REP {gen.curr_rep} ---")
    print(e.prompt)

    correct = False
    while True:
        try:
            answer = input("Enter answer: ")
            correct = e.check_answer(answer)
            break
        except ValueError as err:
            print(str(err))

    print(f"Took {round(e.duration, 2)} seconds.")
    if correct:
        print("Answer correct!")
    else:
        print("Answer incorrect!")
        print(f"Correct solution: {e.solution}")

    print()
