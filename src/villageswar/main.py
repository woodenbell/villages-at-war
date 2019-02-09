from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import open
from traceback import format_exc

from future import standard_library
from jsonschema import ValidationError

standard_library.install_aliases()
from argparse import ArgumentParser
from json import load
from threading import Thread

from villageswar.config import configs, get_config, get_generator, close_dump_file, get_cmd_args
from villageswar.information import info
from villageswar.exception import SimulationError, InvalidConfigError, InvalidGeneratorError
from villageswar.generator import Generator
from villageswar.validator import validate_config, validate_generator
from villageswar.village import Village
from villageswar.world import World
from villageswar.plot import PlotAnim
from villageswar.util import Barrier


class WorldUpdater(Thread):
    def __init__(self, world, barrier):
        self.world_obj = world
        self.barrier = barrier
        self.should_run = True
        
        super().__init__()
    
    def run(self):
        while True:
            if not self.should_run:
                # Should stop
                break
            
            # Waits at barrier before updating again
            
            self.barrier.wait()
            
            try:
                self.world_obj.day_pass()
                
                if get_cmd_args()['victory']:
                    if len(self.world_obj.village1.population) == 0:
                        info('%s wins' % self.world_obj.village1.name, village=self.world_obj.name)
                        close_dump_file()
                        exit(0)
                    elif len(self.world_obj.village2.population) == 0:
                        info('%s wins' % self.world_obj.village1.name, village=self.world_obj.name)
                        close_dump_file()
                        exit(0)
            except Exception as exc:
                # Exception occurred, simulation is over
                
                raise SimulationError('Exception occurred during simulation %s' % exc.__class__.__name__, exc)
        
        close_dump_file()


def main():
    argp = ArgumentParser()
    argp.add_argument('-i', '--info', action='store_true', help='Enables info logs')
    argp.add_argument('-c', '--config', action='store', help='Uses custom config file')
    argp.add_argument('-f', '--file', action='store', help='Specifies a file to dump info')
    argp.add_argument('-g', '--generator', action='store', help='Specifies a custom generator file')
    argp.add_argument('-x', '--xlim', action='store', type=int, help='Specifies a custom x limit to graph')
    argp.add_argument('-y', '--ylim', action='store', type=int, help='Specifies a custom y limit to graph')
    argp.add_argument('-u', '--until', action='store', type=int, help='Specifies a limit of days to the simulation')
    argp.add_argument('-v', '--victory', action='store_true', help='Stops simulation when a village is annihilated')
    args = argp.parse_args()
    
    cmd_args = {}
    
    if args.config:
        with open(args.config) as f:
            try:
                cfg = validate_config(load(f))
                configs['config'] = cfg
            except ValidationError:
                raise InvalidConfigError('Invalid custom config')
    
    if args.generator:
        with open(args.config) as f:
            try:
                cfg = validate_generator(load(f))
                configs['generator'] = cfg
            except ValidationError:
                raise InvalidGeneratorError('Invalid custom generator')
    
    if args.file:
        # Opens file, creating it if it doesn't exist
        
        cmd_args['dump-file'] = open(args.file, 'w+')
    else:
        cmd_args['dump-file'] = None
    
    # Indicates whether or not info should be printed on console
        
    cmd_args['info'] = bool(args.info)

    if args.xlim:
        # Specifies x limit
        
        cmd_args['xlim'] = args.xlim
    
    if args.ylim:
        # Specifies y limit
        
        cmd_args['ylim'] = args.ylim
    
    if args.until:
        # Specifies day limit
        
        cmd_args['until'] = args.until
        
    # Specifies whether or not simulation should stop when a village has no population
    
    cmd_args['victory'] = bool(args.victory)
    
    # Sets values on config variable
    
    configs['cmd-args'] = cmd_args
    config = get_config()
    
    # Instantiates both villages
    
    v1 = Village(config['village-names'][0])
    v2 = Village(config['village-names'][1])
    
    # Creates a generator and generates population
    
    generator = Generator(get_generator())
    generator.generate(v1, v2)
    
    # Instantiates a barrier to keep plotting and world updating synchronized
    
    barrier = Barrier(2)
    
    # Instantiates world object
    
    w = World(v1, v2)
    
    # Instantiates an updater thread object to deal with day loops
    
    wu = WorldUpdater(w, barrier)
    
    # Instantiates plot animation handler
    
    pl = PlotAnim(config['village-names'], wu, barrier)
    
    # Starts day loop and plotting
    
    wu.start()
    pl.start_animation()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # If any exception occurs, logs it and exits
        
        info('')
        info('[EXCEPTION]')
        info('Exception occurred during program execution:\n %s:\n %s' % (e, format_exc()))
        
        print('Exception occurred during program execution:\n %s:\n %s' % (e, format_exc()))
        exit(-1)
