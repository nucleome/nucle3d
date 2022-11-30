#!/home/yangz6/Software/Python-2.7.5/python-2.7.5
# Programmer : Yang Zhang 
# Contact: yzhan116@illinois.edu
# Last-modified: 30 Nov 2022 01:30:55 PM

import os,sys,argparse
import math

def parse_arg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency :')
    p.add_argument('-v','--version',action='version',version='%(prog)s 0.1')
    p.add_argument('-i','--input',type=str,dest="input",help="input file")
    p.add_argument('-f','--format',type=str,dest="format",help="input format, pdb, cmm, n3d, etc")
    p.add_argument('--assembly',type=str,dest="assembly",help="assembly id, eg., hg19, hg38, sacCer3, etc")
    p.add_argument('-o','--output',type=str,dest="output",help="output file prefix (ie, without suffix)")
    if len(sys.argv) < 2:
        print(p.print_help())
        exit(1)
    return p.parse_args()

class Pos(object):
    def __init__(self, X, Y, Z):
        """
        An internal object used to represent 3D position in 3D space as Cartesian coordinates in three-dimensional Euclidean space
        """
        self.x = X
        self.y = Y
        self.z = Z

class Bin(object):
    def __init__(self, chrom, start, end, x, y, z):
        """
        An internal object used to represent a bin and its spatial position
        """
        self.chrom = chrom
        self.start = start
        self.end = end
        self.pos = Pos(x, y, z)
    def __repr__(self):
        return "%s\t%d\t%d\t%.9f\t%.9f\t%.9f\n" % (self.chrom, self.start, self.end, self.pos.x, self.pos.y, self.pos.z)

class Structure(object):
    def __init__(self):
        """
        3D structure object for chromtin
        """
        self.model_id = None
        self.model_name = None
        self.species = None
        self.assembly_id = None
        self.res = None # resolution of structure in base pair
        self.data = []
    def __repr__(self):
        self.sort_bin_by_pos()
        text = ""
        text += "model_id: %s\n" % (self.model_id)
        text += "model_name: %s\n" % (self.model_name)
        text += "species: %s\n" % (self.species)
        text += "assembly id: %s\n" % (self.assembly_id)
        text += "bin resolution: %s\n" % (self.res)
        for _bin in self.data:
            text += str(_bin)
        return text
    def sort_bin_by_pos(self):
        self.data = sorted(self.data, key = lambda bin: (bin.chrom, bin.start))
    def add_assembly(self, assembly_id):
        self.assembly_id = assembly_id
        self.species = species_lookup(assembly_id)
    def to_nucle3d(self, fout):
        """
        export to nucle3d file which can be visualized on Nucleome Browser
        """
        self.data = sorted(self.data, key = lambda bin: (bin.chrom, bin.start))
        print("TITLE\t%s" % (self.model_name), file = fout)
        print("GENOME\t%s" % (self.assembly_id), file = fout)
        print("BINSIZE\t%d"  % (self.res), file = fout)
        last_chrom = None
        for _bin in self.data:
            if last_chrom != _bin.chrom:
                print("CHR\t%s" % (_bin.chrom), file = fout)
                last_chrom = _bin.chrom
            idx = math.floor(_bin.start / self.res)
            print("%d,%.8f.%.8f,%.8f" % (idx, _bin.pos.x, _bin.pos.y, _bin.pos.z), file = fout)
 
def species_lookup(assembly_id):
    table = {'hg19': 'human', 'hg38': 'human', 'mm10': 'mouse', 'sacCer3': 'yeast'}
    return table[assembly_id]

def n3d_parser(filename):
    bin_size = None
    last_start = None
    model_table = {}
    with open(filename, 'r') as fin:
        for line in fin:
            if line.strip().startswith('#') or line.strip() == '':
                continue
            # 
            row = line.strip().split()
            if len(row) == 3: # block header
                chrom = row[0]
                num_coords = int(row[1])
                num_models = int(row[2])
                for nn in range(num_models):
                    model_id = nn + 1
                    if model_table.get(model_id, None) is None: # use 1,2,3, as model id
                        model_table[model_id] = Structure()
                        model_table[model_id].model_id = 'model_%d' % (model_id)
                        model_table[model_id].model_name = 'model_%d' % (model_id)
                # resett
                last_start = None
                first_bin = None
            elif len(row) > 3: # data
                # check the number of column should be 3*num_model + 1
                try:
                    assert len(row) == int(3 * num_models + 1)
                except AssertionError:
                    print("Number of column does not match block header", file = sys.stderr)
                    exit(1)
                # parse data
                start = int(row[0])
                # assign last_start
                if last_start is None:
                    last_start = start
                else:
                    # get bin_size
                    if bin_size is None:
                        bin_size = start - last_start
                    else:
                        # bin size should be consistent across the file
                        try:
                            assert start - last_start == bin_size
                        except AssertionError:
                            print("Detect multiple resolution %d and %d" %(bin_size, start - last_start), file = sys.stderr)
                            exit(1)
                    last_start = start
                # parse 
                pos_data = [float(col) for col in row[1::]]
                for nn in range(num_models):
                    model_id = nn + 1
                    model = model_table[model_id]
                    idx_x = int(nn * 3 + 0)
                    idx_y = int(nn * 3 + 1)
                    idx_z = int(nn * 3 + 2)
                    pos_x = pos_data[idx_x]
                    pos_y = pos_data[idx_y]
                    pos_z = pos_data[idx_z]
                    if bin_size is None: 
                        first_bin = Bin(chrom, start, start, pos_x, pos_y, pos_z)
                    else:
                        if first_bin is not None:
                            model.data = [Bin(first_bin.chrom, first_bin.start, first_bin.start + bin_size, first_bin.pos.x, first_bin.pos.y, first_bin.pos.z)] + model.data 
                            first_bin = None
                        model.data.append(Bin(chrom, start, start + bin_size, pos_x, pos_y, pos_z))
            else: # unknown
                print("Can't recognize element in line, skip it: %s" %(line.strip()), file = sys.stderr)
    for model_id in model_table.keys():
        model_table[model_id].res = int(bin_size)
    return model_table

def main():
    global args
    args = parse_arg()
    # 
    if args.format == 'n3d':
        model_table = n3d_parser(args.input)
    elif args.format == 'pdb':
        pass
    elif args.foramt == 'cmm':
        pass
    else:
        pass
    # 
    if args.assembly is not None:
        for model_id in model_table.keys():
            model_table[model_id].add_assembly(args.assembly)
    # 
    for model_id in model_table.keys():
        model = model_table[model_id]
        with open(args.output + '_' + model.model_id + '.nul3d', 'w') as fout: 
            model_table[model_id].to_nucle3d(fout)
    
if __name__=="__main__":
    main()
