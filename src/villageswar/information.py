from villageswar.config import get_cmd_args, get_config


def info(s, village=None):
    # Prints in console if info arg was passed in CLI
    
    cmd_args = get_cmd_args()
    config = get_config()
    
    if village and ((cmd_args['info'] is not None) or (cmd_args['dump_file'] is not None)):
        # Computes biggest name among possible used strings as village
        
        biggest_name = max([len(config['village-names'][0]), len(config['village-names'][1]),
                            len(config['world-name']), len('gen')]) + 1
        
        s = ('%-' + str(biggest_name) + 's %s') % ('[%s]' % village, s)
    
    if cmd_args['info']:
        # If info specified, prints
        
        print(s)
    
    if cmd_args['dump-file']:
        # If file specified, dumps info
        
        cmd_args['dump-file'].write('%s\n' % s)
