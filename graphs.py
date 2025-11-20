import matplotlib.pyplot as plt

# Optional: whether to overlay multiple runs
_HOLD_ON = False


def set_hold(on: bool = True):
    global _HOLD_ON
    _HOLD_ON = on


def _maybe_new_figure():
    if not _HOLD_ON:
        plt.figure()
    else:
        if not plt.get_fignums():
            plt.figure()


def _extract_from_engine_results(results: dict):
    """
    Extract station labels, T0 list, and P0 list from results
    returned by Engine.solve().

    Expected keys in results:
        T02, T03, T04, T05
    Each value is ThermoState(P0=?, T0=?)
    """
    station_keys = ["T02", "T03", "T04", "T05"]

    stations = []
    T0_list = []
    P0_list = []

    for key in station_keys:
        if key in results:
            state = results[key]
            stations.append(key[-1])   # '2','3','4','5'
            T0_list.append(state.T0)
            P0_list.append(state.P0)

    if not stations:
        raise ValueError("Engine.solve() 的结果里没有 T02/T03/T04/T05 ")

    return stations, T0_list, P0_list


def plot_temperature_stations(results: dict, label: str | None = None):
    stations, T0_list, _ = _extract_from_engine_results(results)

    _maybe_new_figure()

    x = list(range(len(stations)))
    if label is None:
        label = "T0"

    plt.plot(x, T0_list, marker="o", linestyle="-", label=label)
    plt.xticks(x, stations)
    plt.xlabel("Station")
    plt.ylabel("Stagnation Temperature T0 [K]")
    plt.title("Stagnation Temperature vs Station")
    plt.grid(True)
    plt.legend()


def plot_pressure_stations(results: dict, label: str | None = None):
    stations, _, P0_list = _extract_from_engine_results(results)

    _maybe_new_figure()
        x = list(range(len(stations)))
    if label is None:
        label = "P0"

    plt.semilogy(x, P0_list, marker="o", linestyle="-", label=label)
    plt.xticks(x, stations)
    plt.xlabel("Station")
    plt.ylabel("Stagnation Pressure P0 [Pa]")
    plt.title("Stagnation Pressure vs Station")
    plt.grid(True, which="both")
    plt.legend()

