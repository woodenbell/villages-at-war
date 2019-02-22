from builtins import object
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.lines import Line2D
from villageswar.config import get_cmd_args


def get_jobs(village):
    jobs = [0, 0, 0]
    
    for i in village.population:
        if i.job is not None:
            if i.job.name == 'warrior':
                jobs[0] += 1
            if i.job.name == 'breeder':
                jobs[1] += 1
            if i.job.name == 'healer':
                jobs[2] += 1
    
    return tuple(jobs)


class PlotAnim(object):
    def __init__(self, titles, world_updater, barrier):
        cmd_args = get_cmd_args()
        
        if 'xlim' in cmd_args:
            self.xlim = cmd_args['xlim']
        else:
            self.xlim = 100
        
        if 'ylim' in cmd_args:
            self.ylim = cmd_args['ylim']
        else:
            self.ylim = 100
        
        self.curr_xlim = self.xlim
        self.curr_ylim = self.ylim
        
        self.world_obj = world_updater.world_obj
        self.world_updater = world_updater
        self.village_obj1 = self.world_obj.village1
        self.village_obj2 = self.world_obj.village2
        self.barrier = barrier
        self.titles = titles
        self.animation = None
        self.fig = plt.figure()
        self.fig.canvas.set_window_title('villages-at-war')
        
        self.pop_ax1 = self.fig.add_subplot(3, 3, 1)
        self.pop_ax2 = self.fig.add_subplot(3, 3, 4)
        self.pop_line1 = Line2D([], [], lw=2, color='blue', label='Population')
        self.pop_line2 = Line2D([], [], lw=2, color='red', label='Population')
        self.pop_ax1.add_line(self.pop_line1)
        self.pop_ax2.add_line(self.pop_line2)
        self.pop_ax1.legend(loc='upper left', fontsize=8)
        self.pop_ax2.legend(loc='upper left', fontsize=8)
        self.pop_ax1.set_xlim(0, self.xlim)
        self.pop_ax1.set_ylim(0, self.ylim)
        self.pop_ax2.set_xlim(0, self.xlim)
        self.pop_ax2.set_ylim(0, self.ylim)
        self.pop_data_x = ([], [])
        self.pop_data_y = ([], [])
        
        self.job_ax1 = self.fig.add_subplot(3, 3, 2)
        self.job_ax2 = self.fig.add_subplot(3, 3, 5)
        self.job_line1_w = Line2D([], [], lw=1, color='red', label='Warriors')
        self.job_line1_b = Line2D([], [], lw=1, color='orange', label='Breeders')
        self.job_line1_h = Line2D([], [], lw=1, color='green', label='Healers')
        self.job_line2_w = Line2D([], [], lw=1, color='red', label='Warriors')
        self.job_line2_b = Line2D([], [], lw=1, color='orange', label='Breeders')
        self.job_line2_h = Line2D([], [], lw=1, color='green', label='Healers')
        self.job_ax1.add_line(self.job_line1_w)
        self.job_ax1.add_line(self.job_line1_b)
        self.job_ax1.add_line(self.job_line1_h)
        self.job_ax2.add_line(self.job_line2_w)
        self.job_ax2.add_line(self.job_line2_b)
        self.job_ax2.add_line(self.job_line2_h)
        self.job_ax1.legend(loc='upper left', fontsize=8)
        self.job_ax2.legend(loc='upper left', fontsize=8)
        self.job_ax1.set_xlim(0, self.xlim)
        self.job_ax1.set_ylim(0, self.ylim)
        self.job_ax2.set_xlim(0, self.xlim)
        self.job_ax2.set_ylim(0, self.ylim)
        self.job_data_x = ([], [])
        self.job_data_y = ([], [])
        
        self.dead_ax1 = self.fig.add_subplot(3, 3, 3)
        self.dead_ax2 = self.fig.add_subplot(3, 3, 6)
        self.dead_line1 = Line2D([], [], lw=2, color='blue', label='Dead')
        self.dead_line2 = Line2D([], [], lw=2, color='red', label='Dead')
        self.dead_ax1.add_line(self.dead_line1)
        self.dead_ax2.add_line(self.dead_line2)
        self.dead_ax1.legend(loc='upper left', fontsize=8)
        self.dead_ax2.legend(loc='upper left', fontsize=8)
        self.dead_ax1.set_xlim(0, self.xlim)
        self.dead_ax1.set_ylim(0, self.ylim)
        self.dead_ax2.set_xlim(0, self.xlim)
        self.dead_ax2.set_ylim(0, self.ylim)
        self.dead_data_x = ([], [])
        self.dead_data_y = ([], [])
        
        self.all_lines = [self.pop_line1, self.pop_line2,
                          self.job_line1_w, self.job_line1_b, self.job_line1_h,
                          self.job_line2_w, self.job_line2_b, self.job_line2_h,
                          self.dead_line1, self.dead_line2]
    
    def init(self):
        self.pop_line1.set_data([], [])
        self.pop_line2.set_data([], [])
        self.job_line1_w.set_data([], [])
        self.job_line1_b.set_data([], [])
        self.job_line1_h.set_data([], [])
        self.job_line2_w.set_data([], [])
        self.job_line2_b.set_data([], [])
        self.job_line2_h.set_data([], [])
        self.dead_line1.set_data([], [])
        self.dead_line2.set_data([], [])
        return self.all_lines
    
    def update_data(self):
        # Updates data
        
        # Stores new data bout population
        
        self.pop_data_x[0].append(self.world_obj.date['days'])
        self.pop_data_y[0].append(len(self.village_obj1.population))
        self.pop_data_x[1].append(self.world_obj.date['days'])
        self.pop_data_y[1].append(len(self.village_obj2.population))
        
        # Stores data about jobs
        
        self.job_data_x[0].append(self.world_obj.date['days'])
        self.job_data_y[0].append(get_jobs(self.village_obj1))
        self.job_data_x[1].append(self.world_obj.date['days'])
        self.job_data_y[1].append(get_jobs(self.village_obj2))
        
        # Stores data about deaths
        
        self.dead_data_x[0].append(self.world_obj.date['days'])
        self.dead_data_x[1].append(self.world_obj.date['days'])
        self.dead_data_y[0].append(self.village_obj1.data['dead'])
        self.dead_data_y[1].append(self.village_obj2.data['dead'])
    
    def update_limits(self):
        # Updates limits
        
        # Updates x limits
        
        if self.world_obj.date['days'] > self.curr_xlim:
            self.curr_xlim = self.world_obj.date['days']
            self.curr_ylim = self.curr_xlim / self.xlim * self.ylim
            
            self.pop_ax1.set_xlim(0, self.curr_xlim)
            self.pop_ax2.set_xlim(0, self.curr_xlim)
            self.job_ax1.set_xlim(0, self.curr_xlim)
            self.job_ax2.set_xlim(0, self.curr_xlim)
            self.dead_ax1.set_xlim(0, self.curr_xlim)
            self.dead_ax2.set_xlim(0, self.curr_xlim)
            
            self.pop_ax1.set_ylim(0, self.curr_ylim)
            self.pop_ax2.set_ylim(0, self.curr_ylim)
            self.job_ax1.set_ylim(0, self.curr_ylim)
            self.job_ax2.set_ylim(0, self.curr_ylim)
            self.dead_ax1.set_ylim(0, self.curr_ylim)
            self.dead_ax2.set_ylim(0, self.curr_ylim)
    
    def animate(self, *unused):
        del unused
        
        # Checks whether or not data has been updated
        
        # Updates data
        
        self.update_data()
        
        # Updates limits
        
        self.update_limits()
        
        # Sets data for population
        
        self.pop_line1.set_data(self.pop_data_x[0], self.pop_data_y[0])
        self.pop_line2.set_data(self.pop_data_x[1], self.pop_data_y[1])
        
        # Sets data for jobs
        
        self.job_line1_w.set_data(self.job_data_x[0], list(map(lambda a: a[0], self.job_data_y[0])))
        self.job_line1_b.set_data(self.job_data_x[0], list(map(lambda a: a[1], self.job_data_y[0])))
        self.job_line1_h.set_data(self.job_data_x[0], list(map(lambda a: a[2], self.job_data_y[0])))
        self.job_line2_w.set_data(self.job_data_x[1], list(map(lambda a: a[0], self.job_data_y[1])))
        self.job_line2_b.set_data(self.job_data_x[1], list(map(lambda a: a[1], self.job_data_y[1])))
        self.job_line2_h.set_data(self.job_data_x[1], list(map(lambda a: a[2], self.job_data_y[1])))
        
        # Sets data for dead
        
        self.dead_line1.set_data(self.dead_data_x[0], self.dead_data_y[0])
        self.dead_line2.set_data(self.dead_data_x[1], self.dead_data_y[1])
        
        # Waits at barrier before updating
        
        self.barrier.wait()
        
        return self.all_lines
    
    def start_animation(self):
        # Adds event handler for closing
        
        self.fig.canvas.mpl_connect('close_event', lambda evt: self.handle_close(evt))
        
        self.animation = animation.FuncAnimation(self.fig, lambda i: self.animate(i),
                                                 init_func=lambda: self.init(),
                                                 frames=60, interval=20, blit=True)
        
        plt.show()
    
    def handle_close(self, *unused):
        del unused
        
        # Tells world updater to stop
        
        self.world_updater.should_run = False
        self.barrier.release()
        
        exit(0)
