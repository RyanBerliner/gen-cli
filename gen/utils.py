def user_selection(question, options={'y': True, 'n': False}):
    # use the option * when you want allow someone to input any string they
    # would like, so long as its more than N (its value) characters long

    abbr_str = '/'.join(options.keys())
    answer = input(f'{question} [{abbr_str}]: ')
    abbreviations = [o.lower() for o in options.keys()]

    while answer.lower() not in abbreviations:
        if min_len := options.get('*'):
            if len(answer) >= min_len:
                return answer

        return user_selection(question, options=options)

    return options[answer.lower()]
