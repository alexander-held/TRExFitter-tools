"""
this script reads a TRExFitter .txt fit results file provided via
a command line argument, and creates a string for the NPValues
setting to produce an Asimov dataset with all NPs located at their
best-fit point during workspace creation

make sure to list all normalization factors in the NF_names variable!
"""

from __future__ import print_function
import sys

# config
NF_names    = ["ttb_norm"]
skip_gammas = True


class NP:
    """contains all relevant information about NPs """
    def __init__(self, NP_string):
        str_split = NP_string.strip().split()
        self.name        = str_split[0]         # name of NP
        self.val         = float(str_split[1])  # pull
        self.err_hi      = float(str_split[2])  # upper error
        self.err_lo      = float(str_split[3])  # lower error
        self.isGamma     = "gamma_stat" in self.name
        self.isNF        = any([NFname in self.name for NFname in NF_names])
        if (not self.isGamma) and (not self.isNF):
            # need to prepend string for normal NPs
            self.name    = "alpha_" + self.name

    def __repr__(self):
        return self.name + " " + str(self.val)


def CreateConfigSetting(NP_list):
    """create config setting to fix NPs to their best-fit point
    make sure all NFs are listed in NF_names
    input: list of NP class instance
    """
    setting_string = "NPValues: "
    for NP in NP_list:
        if skip_gammas and NP.isGamma:          # option to skip all gammas
            continue
        else:
            setting_string += NP.name + ":" + str(NP.val) + ","
    setting_string = setting_string[0:-1]     # remove the last comma
    print(setting_string)


def RunEverything():
    """execute everything required to get NPValues settings string"""
    if sys.argv[-1] == __file__:
        print("call via \"python", __file__, "fit_result.txt\"")
        raise SystemExit

    fit_file  = sys.argv[-1]                  # txt file with fit results
    NP_list = []                              # list of NPs

    with open(fit_file) as f:
        for line in f.readlines():
            if "CORRELATION_MATRIX" in line:
                break                               # all NPs already processed
            elif len(line.split()) < 4:           # skip lines without NPs
                continue
            else:
                NP_list.append(NP(line))            # add NPs to the list

    CreateConfigSetting(NP_list)


if __name__ == "__main__":
    RunEverything()
