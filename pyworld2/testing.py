# -*- coding: utf-8 -*-

from math import isclose

from .world2 import World2


def test_standard_run():
    """
    Testing function: checks final values of the state variables.

    """
    end_state = {"time":   2100,
                 "QL":     0.54940464789,
                 "POLR":   2.58741372815,
                 "NR":     278240023740,
                 "CI":      6010240430.13}

    # scenario: standard run
    w2_std = World2()
    w2_std.set_all_standard()
    w2_std.run()

    for val_name, val_end in end_state.items():
        arr_w2 = getattr(w2_std, val_name.lower())
        # print(val_name, "... ", np.allclose(val_end, arr_w2[-1]))
        assert isclose(val_end, arr_w2[-1],
                       rel_tol=1e-10), f"{val_name} is not close to {val_end}"
