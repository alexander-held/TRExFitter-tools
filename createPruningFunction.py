"""
This script creates a file (fixNPs.C) containing a function used to
prune NPs in RooStats workspaces, uses fit ranking file as input.
Change the nNPsToPrune parameter to select how many NPs to prune.
"""

from __future__ import print_function
import sys

nNPsToPrune = 50                            # number of pruned NPs


class NP:
    """contains all relevant information about NPs """
    def __init__(self, NP_string):
        str_split = NP_string.strip().split()
        self.name        = str_split[0]         # name of NP
        self.val         = float(str_split[1])  # pull
        self.err_hi      = float(str_split[2])  # upper error
        self.err_lo      = float(str_split[3])  # lower error
        self.imp_post_hi = float(str_split[4])  # upper impact on mu, post-fit
        self.imp_post_lo = float(str_split[5])  # lower impact on mu, post-fit
        self.imp_pre_hi  = float(str_split[6])  # upper impact on mu, pre-fit
        self.imp_pre_lo  = float(str_split[7])  # lower impact on mu, pre-fit


def CreateOutputFile(filename, NP_list_to_prune):
    """save the pruning function to a file
    inputs: name of output file, list of NP class instances to prune
    """
    with open(filename, "w") as f:
        f.write("void fixNPs(RooWorkspace* w) {\n")
        for NP in NP_list_to_prune[0:nNPsToPrune]:
            f.write("  w->var(\"" + NP.name + "\")->setConstant(1);\n")
            f.write("  w->var(\"" + NP.name + "\")->setVal(" +\
                    str(NP.val) + ");\n")
        f.write("}")


def RunEverything():
    """execute everything required to produce file with pruning function"""
    if sys.argv[-1] == __file__:
        print("call via \"python", __file__, "fit_result.txt\"")
        raise SystemExit

    ranking_file = sys.argv[-1]              # txt file with ranking results
    NP_list = []                             # list of NPs in ranking_file

    with open(ranking_file) as f:
        for line in f.readlines():
            if "CORRELATION_MATRIX" in line:
                break                               # all NPs already processed
            elif len(line.split()) < 8:
                continue                            # skip empty lines
            elif "gamma" in line:
                continue                            # gammas are ignored for this
            else:
                NP_list.append(NP(line))            # add NPs to the list

    # sort NPs by increasing post-fit impact
    NP_list.sort(key=lambda k: max(abs(k.imp_post_hi), abs(k.imp_post_lo)))

    CreateOutputFile("fixNPs.C", NP_list)


if __name__ == "__main__":
    RunEverything()
