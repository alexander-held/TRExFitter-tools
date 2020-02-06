# TRExFitter-tools

Collection of tools for use with the [`TRExFitter`](https://gitlab.cern.ch/TRExStats/TRExFitter) framework used by the ATLAS experiment at the LHC. Some of these are also found on [gitlab](https://gitlab.cern.ch/alheld/).

- `getRatioTable.py`: produces a table of post- to pre-fit yield ratio, works with both `.tex` and `.txt` inputs. Call with the paths to pre-fit table and post-fit tables as arguments. Known limitation: does not properly treat positioning of `\hline` and does not update table caption for the `.tex` case.
- `copyFitHistograms.py`: copy histograms produced by one config to the right place for use by another config (useful if the same inputs are needed).
- `customAsimov.py`: produce the input for the NPValues option with all nuisance parameters fixed to their best-fit point. Takes a fit result `.txt` file as input.
- `removePulls.py`: center best-fit results at nominal pre-fit value, useful to combine constraints on nuisance parameters. Takes fit results `.txt` as input and creates a new file as output.
- `createPruningFunction.py`: create a function to prune nuisance parameters with small impact.
