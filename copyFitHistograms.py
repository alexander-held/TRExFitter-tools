##############################################################
#                                                            #
#  Copy histograms produced with TRExFitter"s "n" option     #
#    arguments: - config file used to produce histograms     #
#               - new config file using the same histograms  #
#    produces:  - histograms for new config                  #
#                                                            #
##############################################################

from __future__ import print_function
import sys
import os


def get_folder_name(config_file):
    with open(config_file, "r") as f:
        for line in f.readlines():
            if "Job" in line:
                folder_name = line.split("\"")[1].strip()
    return folder_name


def create_new_folder(old_name, new_name):
    os.system("mkdir -p " + new_name + "/Histograms")
    os.system("cp " + old_name + "/Histograms/" + old_name + "* " + new_name + "/Histograms/.")
    os.system("rename " + old_name + " " + new_name + " " + new_name + "/Histograms/*")
    print("rename " + old_name + " " + new_name + " " + new_name + "/Histograms/*")


if __name__ == "__main__":
    if sys.argv[-1] == __file__:
        print("usage:", "\"python", __file__, "old_config", "new_config\"")
        raise SystemExit

    old_config = sys.argv[-2]
    new_config = sys.argv[-1]
    print("copying from", old_config, "to", new_config)

    old_name = get_folder_name(old_config)
    new_name = get_folder_name(new_config)

    create_new_folder(old_name, new_name)
    print("histograms copied, can now proceed with options w and f")
