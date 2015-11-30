# Computer Architecture, Final Project

## Contents
* Project Workflow
* Project Layout
* Coding Tasks
* Research Tasks
* Writing Tasks

## Project Workflow

** The proposed workflow is to: **
* (Research) Determine what variables we should change, and give reasoning
* Log our changes from the base config in a Google Spreadsheet with the experiment name
* (Coding) Parse the spreadsheet, create a config file (dropped into the ./configs/{experiment_name}/ directory, where {experiment_name} is the name provided in the spreadsheet)
* (Coding) Automatically read in a config file, run all six experiments, and drop the raw output into a results directory, following the same format as the config directories (./results/{experiment_name}/bzip2.out, etc)
* (Coding) Parse the raw results, pull out desired results
* (Coding) Create graphs / charts / tables as needed
* (Writing) Writing the actual paper

More details are listed under the Tasks section.

## Project Layout

### Rationale

When we run the experiments, we should have a full record of the changes that lead to any results. This is to avoid having to redo work, as once a config is created and a test is run, we should (theoretically) never have to run the experiment again, as long as we keep the original config and raw results.

### Proposed Layout

./configs/
  {experiment_name}/
    config.cfg
./paper/
  images/
    ... (any images used in the paper)
  project.tex
  ... (latex-produced files)
./results/
  {experiment_name}/
    bzip2.out
    equake.out
    hmmer.out
    mcf.out
    milc.out
    sjeng.out
./scripts/
  ... (the scripts listed below, and any others)

## Tasks

### Coding Tasks

1. Write script to parse changes from base config and produce usable config file
  * Quang did this already
2. Write script to accept config file, run experiments, and produce raw result files
3. Write script to parse raw result files, pull out desired data
4. Write script to parse results, produce graphs
  * We probably shouldn't do this in isolation, but rather wait until we know what graphs / charts we need for the paper. It's likely that we can make several really short, one-off scripts, so this isn't a major task.

### Research Tasks

1. Research and compile the available variables and those that can't be modified
2. Record any dependencies between variables
3. Determine which combinations that we expect will work best, why we should use those combinations, and keep a record of our reasons (this will be needed for the writing portion)

### Writing Tasks

1. Create Latex base file
2. Determine the layout for the paper, divide the work up
3. If needed, write script to automatically generate tables
  * Ben did this already
