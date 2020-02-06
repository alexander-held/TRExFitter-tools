# ########################################
# remove pulls from TRExFitter results
# (to compare data constraints to Asimov)
# ########################################

from __future__ import print_function
import sys

if sys.argv[-1] != __file__:
    input_fit_file = sys.argv[-1]
else:
    print("execute via python", __file__, "input_fit_file.txt")
    raise SystemExit

output_fit_file = input_fit_file[0:-4] + "_no_pulls.txt"

if __name__ == "__main__":
    f = open(input_fit_file)
    content = f.readlines()

    end_of_NPs = content.index("CORRELATION_MATRIX\n")  # all NPs to edit are before this position

    for iline, line in enumerate(content[0:end_of_NPs]):
        line_split = line.split()
        if len(line_split) == 4:
            if "gamma" not in line:
                content[iline] = line_split[0] + " " + "0.0" + " " + line_split[2] + " " + line_split[3] + "\n"
            else:
                content[iline] = line_split[0] + " " + "1.0" + " " + line_split[2] + " " + line_split[3] + "\n"

    out_f = open(output_fit_file, "w")
    for line in content:
        out_f.write(line)
    out_f.close()
