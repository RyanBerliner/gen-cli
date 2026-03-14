def user_confirmation(question):
    answer = input(f'{question} [y/N]: ')

    while answer.lower() not in {'y', 'n'}:
        return user_confirmation(question)

    return answer == 'y'
