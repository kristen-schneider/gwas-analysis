def read_colors(colors_file):
    '''
    read comma delimited colors file and store in a dict
    :param colors_file:
    :return:
    '''
    colors = {}
    with open(colors_file, 'r') as f:
        for line in f:
            codec, color = line.strip().split(',')
            colors[codec] = color

    return colors

def read_gwas_file_names(gwas_names_file):
    '''
    Read the names of the gwas files from a file
    :param gwas_names_file: text file containing the names of the gwas files to include in plot
    :return: list of gwas file names
    '''
    gwas_files = []
    with open(gwas_names_file, 'r') as f:
        for line in f:
            gwas_files.append(line.strip())
    return gwas_files

def read_gwas_file_sizes(gwas_sizes_file):
    '''
    Read the file sizes of the gwas files from a file
    :param gwas_sizes_file: text file containing the file sizes of the gwas files
    :return: dictionary of file names and their sizes in bytes
    '''
    file_sizes = {}
    with open(gwas_sizes_file, 'r') as f:
        header = f.readline()
        for line in f:
            file_name, file_size = line.strip().split(', ')
            file_sizes[file_name] = int(file_size)
    return file_sizes

def read_timing_file(timing_file,
                     codecs):
    '''
    Read the timing data from a file
    :param timing_file: text file containing timing data
    :return: dictionary of codec names and their timing data
    '''

    timing = {}

    for codec in codecs:
        timing[codec] = {'compression': 0,
                          'indexing': 0,
                          'decompression': 0}

    '''
    Running for codec: bz2
    Compressing...
    /Users/krsc0813/CLionProjects/gwas_local/cmake-build-debug/bin/gwas_compress   105.95s user 1.43s system 99% cpu 1:48.10 total
    Indexing...
    /Users/krsc0813/CLionProjects/gwas_local/cmake-build-debug/bin/gwas_index  >>  5.14s user 0.12s system 99% cpu 5.308 total
    Decompressing...
    /Users/krsc0813/CLionProjects/gwas_local/cmake-build-debug/bin/gwas_decompres  101.57s user 0.13s system 99% cpu 1:42.24 total
    Running for codec: deflate
    Compressing...
    ...
    '''
    with open(timing_file, 'r') as f:
        for line in f:
            if 'Running for codec' in line:
                codec = line.split(': ')[1].strip()
            elif 'Compressing...' in line:
                total_time = f.readline().split()[7]
                try:
                    minutes = int(total_time.split(':')[0]) * 60
                    seconds = float(total_time.split(':')[1])
                except:
                    minutes = 0
                    seconds = float(total_time)
                timing[codec]['compression'] = minutes + seconds
            elif 'Indexing...' in line:
                total_time = f.readline().split()[8]
                try:
                    minutes = int(total_time.split(':')[0]) * 60
                    seconds = float(total_time.split(':')[1])
                except:
                    minutes = 0
                    seconds = float(total_time)
                timing[codec]['indexing'] = minutes + seconds
            elif 'Decompressing...' in line:
                total_time = f.readline().split()[7]
                try:
                    minutes = int(total_time.split(':')[0]) * 60
                    seconds = float(total_time.split(':')[1])
                except:
                    minutes = 0
                    seconds = float(total_time)
                timing[codec]['decompression'] = minutes + seconds

    return timing