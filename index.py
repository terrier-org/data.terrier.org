import importlib
import os
import sys

MD5 = "md5" if sys.platform == 'darwin' else "md5sum"

def calc_md5s(dest_dir : str):
    os.system("cd %s; %s * > md5sums" % (dest_dir, MD5) )
    
    #finally, append file listing
    with open(os.path.join(dest_dir, 'files'), 'wt') as filelist:
        for dirpath, dirnames, filenames in os.walk(dest_dir):
            for i in filenames:
                if i == 'files':
                    continue
                #use join to concatenate all the components of path
                f = os.path.join(dirpath, i)
                filelist.write('%d %s\n' % (os.path.getsize(f), i))

def run_index(dataset : str, variant : str, target_dir : str, date : str):
    import pyterrier_prebuilt

    index_fn = pyterrier_prebuilt.get_thing(dataset, variant, 'index')
    dest_dir = os.path.join(target_dir, dataset, variant, date)
    kwargs={}
    kwargs['variant'] = variant
    index_fn(dest_dir, **kwargs)
    calc_md5s(dest_dir)

def usage(name):
    print("Usage:")
    print("%s dataset variantname builddir" % name)

if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) != 4:
        usage(args[0])
        sys.exit(1)
    else:
        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d')
        import pyterrier as pt
        pt.init(logging='INFO', mem=80 * 1024)
        run_index(args[1], args[2], args[3], date)