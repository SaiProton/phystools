from sympy import symbols, solve, Eq

def problem_solver(initial: dict[str, float], final: dict[str, float], find: str) -> list[dict[str, float]]:
    """
    Solves a 1D kinematics problem!

    Args:
        initial (dict[str, float]): Variables at the initial point in time
        final (dict[str, float]): Variables at the final point in time

        NOTE: For each dict, use these keys for the variables
            ***INITIAL and FINAL dicts***
            s: (position)
            v: (velocity)
            t: (time)
            
            ***INITIAL dict ONLY***
            a: (acceleration) #! Acceleration is assumed to be constant #!
    """

    variable_prefixes = ['s', 't', 'v', 'a']
    
    # both dicts are grouped to make looping easier
    group_collection = {'initial': initial, 'final': final}

    # loop through each value in both dicts -- if a variable is missing, fill it in with a sympy symbol
    for group_number, group in enumerate(group_collection.values()):
        for name in variable_prefixes:
            if name not in group.keys():
                group[name] = symbols(f'{name}{group_number}')

    # the big 5 kinematic equations... if these can't solve it, i'm too lazy to write anything else so good luck
    big_5 = [
        Eq(final['v'], initial['v'] + initial['a']*(final['t'] - initial['t'])),
        Eq((final['s'] - initial['s']), 0.5*initial['a']*(final['t'] - initial['t'])**2 + initial['v']*(final['t'] - initial['t'])),
        Eq(final['v']**2, initial['v']**2 + 2*initial['a']*(final['s'] - initial['s'])),
        Eq((final['s'] - initial['s']), -0.5*initial['a']*(final['t'] - initial['t'])**2 + final['v']*(final['t'] - initial['t'])),
        Eq((final['s'] - initial['s']), 0.5*(final['s'] + initial['s'])*(final['t'] - initial['t'])),
    ]
    
    # brute forces the big 5 until an answer the user specified is found
    for equation in big_5:
        solution = solve(equation, dict=True)
        if solution:
            for (name, result) in solution[0].items():
                if result.is_number and name.name == find:
                    solution[0][name] = result.evalf()
                    return solution

if __name__ == '__main__':
    initial = {
        's': 0,
        't': 0,
        'v': 0,
        'a': 9.8
    }

    final = {
        'v': 3e8,
        't': 30612244.8979592
    }

    sol = problem_solver(initial=initial, final=final, find='s1')
    print(sol)