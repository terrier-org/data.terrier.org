
def promote(dataset : str, date : str, builddir : str):
    import os
    datasetdir = os.path.join(builddir, dataset)
    for variant in os.listdir(datasetdir):
        variant_dated_dir = os.path.join(datasetdir, variant, date)
        if not os.path.exists(variant_dated_dir):
            continue
        symlink = os.path.join(datasetdir, variant, "latest")
        if os.path.exists(symlink):
            os.remove(symlink)
        import os
        fd  = os.open( os.path.join(datasetdir, variant), os.O_RDONLY )
        os.symlink(date, "latest", dir_fd=fd)
        os.close(fd)
        print("Promoting %s to be latest"  % variant_dated_dir)

def usage(name):
    print("Usage:")
    print("%s dataset date builddir" % name)

if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) != 4:
        usage(args[0])
        sys.exit(1)
    else:
        dataset = args[1]
        date = args[2]
        builddir = args[3]
        promote(dataset, date, builddir)