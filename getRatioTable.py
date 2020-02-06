from __future__ import print_function

import sys
import re
from collections import OrderedDict


def split_table_field(field):
    if "\\pm" in field:
        split = field.split("\pm")
    elif "pm" in field:
        split = field.split("pm")
    else:
        print("cannot determine how to split string, aborting")
        raise SystemExit
    split = [s.strip("\\") for s in split]  # strip line breaks
    count = float(split[0])
    uncertainty = float(split[1])
    return count, uncertainty


def get_dict_with_info(line_split, yields):
    """add sample yields/uncertainties per region to ordered dict yields"""
    sample = line_split[0]
    regions = []
    for field in line_split[1:]:
        count, uncertainty = split_table_field(field)
        regions.append([count, uncertainty])
    yields.update({sample: regions})
    return yields


def check_line_skip(line):
    if "Data" in line:
        print("found data, skipping")
        return True
    else:
        return False


def parse_txt(content):
    skeleton_above = content[0]  # all the lines above the table
    yields = OrderedDict()       # dict with all info needed
    for line in content[1:]:
        if check_line_skip(line):
            continue
        line = line.strip()
        line_split = line.split("|")[1:-1]
        yields = get_dict_with_info(line_split, yields)
    return yields, [skeleton_above], []


def parse_tex(content):
    inTable = False
    belowTable = False
    skeleton_above = []
    skeleton_below = []  # lines below table
    yields = OrderedDict()
    for line in content:
        if check_line_skip(line):
            continue
        line = line.strip()
        if "\\end{tabular}" in line:
            inTable = False
            belowTable = True
        if inTable and line[0] != "&" and ("\\hline" not in line):
            line_split = re.split(r'(?<!\\)&', line)  # regex magic https://stackoverflow.com/a/21107911
            yields = get_dict_with_info(line_split, yields)
        else:
            if not belowTable:
                skeleton_above.append(line)
            else:
                skeleton_below.append(line)
        if "\\begin{tabular}" in line:
            inTable = True
    return yields, "\n".join(skeleton_above), "\n".join(skeleton_below)


def read_file(fname):
    print("reading", fname)
    with open(fname) as f:
        content = f.readlines()
    if ".tex" in fname:
        parsed = parse_tex(content)
        outputFormat = "tex"
    elif ".txt" in fname:
        parsed = parse_txt(content)
        outputFormat = "txt"
    else:
        print("could not identify file format of " + fname + ", aborting")
        raise SystemExit
    return parsed[0], parsed[1], parsed[2], outputFormat


def calculate_ratio(yields_prefit, yields_postfit):
    ratioDict = OrderedDict()
    for sample in yields_prefit:
        try:
            assert len(yields_prefit[sample]) == len(yields_postfit[sample])
        except KeyError:
            print("sample", sample, "not found, probably due to blinding? skipping it")
            continue
        regions = []
        for iRegion in range(len(yields_prefit[sample])):
            yieldPrefit  = yields_prefit[sample][iRegion][0]
            uncPrefit    = yields_prefit[sample][iRegion][1]
            yieldPostfit = yields_postfit[sample][iRegion][0]
            uncPostfit   = yields_postfit[sample][iRegion][1]
            try:
                ratio = yieldPostfit / yieldPrefit
            except ZeroDivisionError:
                ratio = 0
            # for uncertainty: sum in quadrature
            try:
                unc = ((uncPrefit/yieldPrefit)**2 + (uncPostfit/yieldPostfit)**2)**0.5 * ratio
            except ZeroDivisionError:
                unc = 0
            regions.append([ratio, unc])
        ratioDict.update({sample: regions})
    return ratioDict


def fix_name(name):
    """fix sample names"""
    if "#geq" in name:
        if name[name.find("#geq")+5] != " ":
            # no whitespace after command
            name = name.replace("#geq", "#geq ")
    if "#" in name:
        print("exchaning # in", name, "by \\")
        name = name.replace("#", "\\")
    if "\\" in name:
        name = "$" + name + "$"
    return name


def ratio_list_to_string(name, ratio_list, outputFormat):
    if outputFormat == "tex":
        delimiter = " & "
        line_end = " \\\\\n"
        pm = " \pm "
    elif outputFormat == "txt":
        delimiter = " | "
        line_end = "\n"
        pm = " pm "
    if outputFormat == "tex":
        name = fix_name(name)
    if outputFormat == "txt":
        ratio_string = " |" + name
    else:
        ratio_string = name
    for region in ratio_list:
        region_string = str(round(region[0], 3)) + pm + str(round(region[1], 3))
        ratio_string += delimiter
        ratio_string += region_string
    ratio_string += line_end
    return ratio_string


def save_to_file(skeleton_above, skeleton_below, ratioDict, outputFormat):
    with open("Yields_ratio." + outputFormat, "w") as f:
        # write header
        for line in skeleton_above:
            f.write(line)
        if outputFormat == "tex":
            f.write("\n")
        # write content
        for sample in ratioDict:
            name = sample
            ratio = ratioDict[sample]
            line = ratio_list_to_string(name, ratio, outputFormat)
            f.write(line)
        # write the bottom part for latex
        for line in skeleton_below:
            f.write(line)
        f.write("\n")


if __name__ == "__main__":
    if sys.argv[-1] == __file__ or len(sys.argv) != 3:
        print("run as \"python " + __file__ + " Yields.tex Yields_postFit.tex\" (or with the .txt files)")
        raise SystemExit

    prefit_yields, skeleton_above, skeleton_below, outputFormat = read_file(sys.argv[-2])
    postfit_yields, _, _, _ = read_file(sys.argv[-1])

    ratioDict = calculate_ratio(prefit_yields, postfit_yields)
    save_to_file(skeleton_above, skeleton_below, ratioDict, outputFormat)
