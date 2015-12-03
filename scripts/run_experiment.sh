#!/bin/bash

# bash run_experiment.sh experiment_set/test_name


# Run all simulations:
cd ../ss-benchmark/bzip2;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/bzip2.out bzip2_base.i386-m32-gcc42-nn dryer.jpg;

cd ../mcf;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/mcf.out mcf_base.i386-m32-gcc42-nn inp.in;

cd ../hmmer;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/hmmer.out hmmer_base.i386-m32-gcc42-nn bombesin.hmm;

cd ../sjeng;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/sjeng.out sjeng_base.i386-m32-gcc42-nn test.txt;

cd ../milc;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/milc.out milc_base.i386-m32-gcc42-nn < su3imp.in;

cd ../equake;
/home/software/simplesim/simplesim-3.0/sim-outorder -config ../../configs/$1/config.cfg -redir:sim ../../results/$1/equake.out equake_base.pisa_little < inp.in > inp.out;

cd ../../scripts;
