import importlib
import os
import sys

MD5 = "md5" if sys.platform == 'darwin' else "md5sum"

def calc_md5s(dest_dir : str):
    os.system("cd %s; %s * > md5sums" % (dest_dir, MD5) )

def run_index(dataset : str, variant : str, target_dir : str):
    import pyterrier_prebuilt
    module_name = "pyterrier_prebuilt.%s.%s" % (dataset, variant)
    kwargs={}
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        module_name = "pyterrier_prebuilt.%s" % (dataset)
        module = importlib.import_module(module_name)
        kwargs['variant'] = variant
    function_name = 'index'
    
    index_fn = getattr(module, function_name)
    dest_dir = os.path.join(target_dir, dataset, variant)
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
    else:
        import pyterrier as pt
        pt.init()
        run_index(args[1], args[2], args[3])