from typing import List, Any

from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from villageswar.main import WorldUpdater
from villageswar.util import Barrier
from villageswar.village import Village
from villageswar.world import World


def get_jobs(village): ...

class PlotAnim(object):
    ...

    def __init__(self, titles: List[str], world_updater: WorldUpdater, barrier: Barrier):
        self.xlim = None  # type: int
        self.ylim = None  # type: int
        self.curr_xlim = None  # type: int
        self.curr_ylim = None  # type: int
        self.world_obj = None  # type: World
        self.world_updater = None  # type: WorldUpdater
        self.village_obj1 = None  # type: Village
        self.village_obj2 = None  # type: Village
        self.barrier = None  # type: Barrier
        self.titles = None  # type: List[str]
        self.animation = None  # type: FuncAnimation
        self.fig = None  # type: Figure
        
        self.pop_ax1 = None  # type: Axes
        self.pop_ax2 = None  # type: Axes
        self.pop_line1 = None  # type: Line2D
        self.pop_line2 = None  # type: Line2D
        self.pop_data_x = None  # type: (List[int], List[int])
        self.pop_data_y = None  # type: (List[int], List[int])
        
        self.job_ax1 = None  # type: Axes
        self.job_ax2 = None  # type: Axes
        self.job_line1_w = None  # type: Line2D
        self.job_line1_b = None  # type: Line2D
        self.job_line1_h = None  # type: Line2D
        self.job_line2_w = None  # type: Line2D
        self.job_line2_b = None  # type: Line2D
        self.job_line2_h = None  # type: Line2D
        self.job_data_x = None  # type: (List[(int, int, int)], List[(int, int, int)])
        self.job_data_y = None  # type: (List[(int, int, int)], List[(int, int, int)])
        
        self.dead_ax1 = None  # type: Axes
        self.dead_ax2 = None  # type: Axes
        self.dead_line1 = None  # type: Line2D
        self.dead_line2 = None  # type: Line2D
        self.dead_data_x = None  # type: (List[int], List[int])
        self.dead_data_y = None  # type: (List[int], List[int])
        
        self.all_lines = None  # type: List[Line2D]
        ...

    def init(self) -> List[Line2D]: ...

    def update_data(self): ...

    def update_limits(self): ...

    def animate(self, *unused: List[Any]) -> List[Line2D]: ...

    def start_animation(self): ...

    def handle_close(self, *unused): ...
