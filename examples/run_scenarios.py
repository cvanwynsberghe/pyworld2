# -*- coding: utf-8 -*-
import pyworld2
from pyworld2.utils import plot_world_variables

# Scenario 1 - Standard run
w2_std = pyworld2.World2()
w2_std.set_state_variables()
w2_std.set_initial_state()
w2_std.set_table_functions()
w2_std.set_switch_functions()
w2_std.run()
plot_world_variables(w2_std.time,
                     [w2_std.p, w2_std.polr, w2_std.ci, w2_std.ql, w2_std.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 1 [Standard run]")

# Scenario 2 - Pollution crisis
w2_sc2 = pyworld2.World2()
w2_sc2.set_state_variables()
w2_sc2.set_initial_state()
w2_sc2.set_table_functions()
w2_sc2.set_switch_functions("./scenarios/functions_switch_scenario_2.json")
w2_sc2.run()
plot_world_variables(w2_sc2.time,
                     [w2_sc2.p, w2_sc2.polr, w2_sc2.ci, w2_sc2.ql,
                      w2_sc2.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 2 [cf. 4.3 Pollution crisis]")

# Scenario 3 - Crowding
w2_sc3 = pyworld2.World2(year_max=2300)
w2_sc3.set_state_variables()
w2_sc3.set_initial_state()
w2_sc3.set_table_functions()
w2_sc3.set_switch_functions("./scenarios/functions_switch_scenario_3.json")
w2_sc3.run()
plot_world_variables(w2_sc3.time,
                     [w2_sc3.p, w2_sc3.polr, w2_sc3.ci, w2_sc3.ql,
                      w2_sc3.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 16e9], [0, 80], [0, 40e9], [0, 4], [0, 2000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 3 [cf. 4.4 Crowding]")

# Scenario 4 - Food shortage
w2_sc4 = pyworld2.World2(year_max=2300)
w2_sc4.set_state_variables()
w2_sc4.set_initial_state()
w2_sc4.set_table_functions("./scenarios/functions_table_scenario_4.json")
w2_sc4.set_switch_functions("./scenarios/functions_switch_scenario_4.json")
w2_sc4.run()
plot_world_variables(w2_sc4.time,
                     [w2_sc4.p, w2_sc4.polr, w2_sc4.ci, w2_sc4.ql,
                      w2_sc4.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 16e9], [0, 80], [0, 40e9], [0, 4], [0, 2000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 4 [cf. 4.5 Food shortage]")

# Scenario 5 - Increased capital-investment generation
w2_sc5 = pyworld2.World2()
w2_sc5.set_state_variables()
w2_sc5.set_initial_state()
w2_sc5.set_table_functions()
w2_sc5.set_switch_functions("./scenarios/functions_switch_scenario_5.json")
w2_sc5.run()
plot_world_variables(w2_sc5.time,
                     [w2_sc5.p, w2_sc5.polr, w2_sc5.ci, w2_sc5.ql,
                      w2_sc5.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 5 [cf. 5.1 Boost capital investment]")

# Scenario 6.1: Birth control
w2_sc6 = pyworld2.World2()
w2_sc6.set_state_variables()
w2_sc6.set_initial_state()
w2_sc6.set_table_functions()
w2_sc6.set_switch_functions("./scenarios/functions_switch_scenario_6.1.json")
w2_sc6.run()
plot_world_variables(w2_sc6.time,
                     [w2_sc6.p, w2_sc6.polr, w2_sc6.ci, w2_sc6.ql,
                      w2_sc6.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 6.1 [fig. 5.2 Birth Control]")

# Scenario 6.2: Birth control + Reduced natural resource usage
w2_sc62 = pyworld2.World2()
w2_sc62.set_state_variables()
w2_sc62.set_initial_state()
w2_sc62.set_table_functions()
w2_sc62.set_switch_functions("./scenarios/functions_switch_scenario_6.2.json")
w2_sc62.run()
plot_world_variables(w2_sc62.time,
                     [w2_sc62.p, w2_sc62.polr, w2_sc62.ci, w2_sc62.ql,
                      w2_sc62.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 6.2 [fig. 5.4]")

# Scenario 6.3 - Birth control + Reduced natural resource usage + reduced pollution
w2_sc63 = pyworld2.World2()
w2_sc63.set_state_variables()
w2_sc63.set_initial_state()
w2_sc63.set_table_functions()
w2_sc63.set_switch_functions("./scenarios/functions_switch_scenario_6.3.json")
w2_sc63.run()
plot_world_variables(w2_sc63.time,
                     [w2_sc63.p, w2_sc63.polr, w2_sc63.ci, w2_sc63.ql,
                      w2_sc63.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 6.3 [fig. 5.5]")

# Scenario 6.4 - Strong Birth control + Reduced natural resource usage + reduced pollution
w2_sc64 = pyworld2.World2()
w2_sc64.set_state_variables()
w2_sc64.set_initial_state()
w2_sc64.set_table_functions()
w2_sc64.set_switch_functions("./scenarios/functions_switch_scenario_6.4.json")
w2_sc64.run()
plot_world_variables(w2_sc64.time,
                     [w2_sc64.p, w2_sc64.polr, w2_sc64.ci, w2_sc64.ql,
                      w2_sc64.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 6.4 [fig. 5.6]")

# Scenario 7 - Less pollution
w2_sc7 = pyworld2.World2()
w2_sc7.set_state_variables()
w2_sc7.set_initial_state()
w2_sc7.set_table_functions()
w2_sc7.set_switch_functions("./scenarios/functions_switch_scenario_7.json")
w2_sc7.run()
plot_world_variables(w2_sc7.time,
                     [w2_sc7.p, w2_sc7.polr, w2_sc7.ci, w2_sc7.ql,
                      w2_sc7.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 7 [fig. 5.8 Less pollution]")

# Scenario 8 - Increased food production, higher agricultural productivity
w2_sc81 = pyworld2.World2()
w2_sc81.set_state_variables()
w2_sc81.set_initial_state()
w2_sc81.set_table_functions()
w2_sc81.set_switch_functions("./scenarios/functions_switch_scenario_8.1.json")
w2_sc81.run()
plot_world_variables(w2_sc81.time,
                     [w2_sc81.p, w2_sc81.polr, w2_sc81.ci, w2_sc81.ql,
                      w2_sc81.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 8.1 [fig. 5.9 More food]")

# Scenario 8.2 - More food, less resource usage and less pollution
w2_sc82 = pyworld2.World2()
w2_sc82.set_state_variables()
w2_sc82.set_initial_state()
w2_sc82.set_table_functions()
w2_sc82.set_switch_functions("./scenarios/functions_switch_scenario_8.2.json")
w2_sc82.run()
plot_world_variables(w2_sc82.time,
                     [w2_sc82.p, w2_sc82.polr, w2_sc82.ci, w2_sc82.ql,
                      w2_sc82.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 8.2 [fig. 5.11]")

# Scenario 8.3 - More food, less resource usage and less pollution, more capital investment
w2_sc83 = pyworld2.World2()
w2_sc83.set_state_variables()
w2_sc83.set_initial_state()
w2_sc83.set_table_functions()
w2_sc83.set_switch_functions("./scenarios/functions_switch_scenario_8.3.json")
w2_sc83.run()
plot_world_variables(w2_sc83.time,
                     [w2_sc83.p, w2_sc83.polr, w2_sc83.ci, w2_sc83.ql,
                      w2_sc83.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 8.3 [fig. 5.12]")

# Scenario 9 - Towards stability by reduced resource usage and pollution
w2_sc9 = pyworld2.World2()
w2_sc9.set_state_variables()
w2_sc9.set_initial_state()
w2_sc9.set_table_functions()
w2_sc9.set_switch_functions("./scenarios/functions_switch_scenario_9.json")
w2_sc9.run()
plot_world_variables(w2_sc9.time,
                     [w2_sc9.p, w2_sc9.polr, w2_sc9.ci, w2_sc9.ql,
                      w2_sc9.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 9 [fig. 6.3]")

# Scenario 10 - Towards stability
w2_sc10 = pyworld2.World2()
w2_sc10.set_state_variables()
w2_sc10.set_initial_state()
w2_sc10.set_table_functions()
w2_sc10.set_switch_functions("./scenarios/functions_switch_scenario_10.json")
w2_sc10.run()
plot_world_variables(w2_sc10.time,
                     [w2_sc10.p, w2_sc10.polr, w2_sc10.ci, w2_sc10.ql,
                      w2_sc10.nr],
                      ["P", "POLR", "CI", "QL", "NR"],
                      [[0, 8e9], [0, 40], [0, 20e9], [0, 2], [0, 1000e9]],
                      figsize=(7, 4), grid=True,
                      title="World2 - Scenario 10 [fig. 6.7]")

# save figures
import matplotlib.pyplot as plt
for n in range(1, 16):
    fig = plt.figure(n)
    figname = fig._suptitle.get_text()
    plt.savefig(figname + ".pdf")

plt.show()
