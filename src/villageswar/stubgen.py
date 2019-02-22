from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import filter
from future import standard_library
standard_library.install_aliases()
from os import listdir  # noqa: E402
from os.path import isfile, splitext  # noqa: E402
from re import compile  # noqa: E402

class_patt = compile(r'^\s*class ([a-zA-Z_]+)(\s*\([^)]*\))?:[ ]*$')
method_patt = compile(r'^(\s*)def ([a-zA-Z_]+)\([^)]*\):[ ]*$')
member_patt = compile(r'^(\s*self\.[a-zA-Z_]+\s*=\s*).*$')
var_patt = compile(r'^([a-zA-Z_]+\s*=\s*).*$')


def mk_stub(m):
    res = []
    
    with open(m, 'r') as f:
        s = f.read().split('\n')
    
    inside_init = False
    spaces = None
    
    for i in s:
        if inside_init:
            mm = member_patt.match(i)
            
            if mm:
                res.append('%sNone # type: ' % mm.group(1))
                continue
        
        mc = class_patt.match(i)
        mp = method_patt.match(i)
        mv = var_patt.match(i)
    
        if inside_init:
            inside_init = False
            res.append('    %s...' % spaces)
            res.append('')
            
        if mv:
            res.append('%sNone # type: ' % mv.group(1))
            continue
    
        if mc:
            res.append(i)
            res.append('    ...')
            res.append('')
            continue
        
        if mp:
            
            if mp.group(2) == '__init__':
                res.append(i)
                inside_init = True
                spaces = mp.group(1)
                continue
            else:
                res.append('%s ...' % i)
                res.append('')
                continue
    
    if inside_init:
        res.append('    %s...' % spaces)
        res.append('')

    
    fn = '%s.pyi' % splitext(m)[0]

    with open(fn, 'w') as f:
        
        f.write('\n'.join(res))
        print('Generated %s' % fn)


def main():
    modules = list(
        filter(lambda f: f != '__init__.py' and f != 'stubgen.py' and isfile(f) and splitext(f)[1] == '.py',
               listdir('.'))
    )
    print(modules)
    
    for i in modules:
        mk_stub(i)


if __name__ == '__main__':
    main()
