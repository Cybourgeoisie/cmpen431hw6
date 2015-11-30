# The assignment has the following restrictions:

0. Issue width restrictions (assumed by provided clock cycle times)
  * Static, issue:width: 1, 2, 3, 4
  * Dynamic, issue:width: 2, 4, 8

1. il1 block size must match the ifq size and dl1 block size
  * Note: The il1/dl1 block sizes are in Bytes, the ifq size are in Words, which is 8B (determined by example given for point 1)
    * ifqsize = il1, dl1 block sizes / word size

2. maximum ul2 block size is 128 B, must be at least double the dl1 block size
  * ul2 size must be at least as large as il1 + dl1 sizes
  * from the above, we know that maximum dl1/il1 block size is 64 B and max ifqsize is 8
  * also, from simplescalar doc: ifqsize must be a power of 2 - this means only 4 different sizes (1,2,4,8)

3. il1 & dl1 latencies are defined by the il1 sizes:
  * All of the below also hold for dl1
  * Direct mapped:
    * il1 = 8 KB (baseline, minimum size) means il1lat = 1
    * il1 = 16 KB means il1lat = 2
    * il1 = 32 KB means il1lat = 3
    * il1 = 64 KB (maximum size) means il1lat = 4
  * 2-way set associative:
    * il1 = 8 KB (baseline, minimum size) means il1lat = 2
    * il1 = 16 KB means il1lat = 3
    * il1 = 32 KB means il1lat = 4
    * il1 = 64 KB (maximum size) means il1lat = 5
  * 4-way set associative:
    * il1 = 8 KB (baseline, minimum size) means il1lat = 3
    * il1 = 16 KB means il1lat = 4
    * il1 = 32 KB means il1lat = 5
    * il1 = 64 KB (maximum size) means il1lat = 6

3.5. By inference from above, cache associativity is limited to 1, 2, 4

4. ul2 latencies are defined by the ul2 sizes:
  * Direct mapped:
    * ul2 = 64KB (baseline, minimum size) means ul2lat = 4
    * ul2 = 128 KB means ul2lat = 5
    * ul2 = 256 KB means ul2lat = 6
    * ul2 = 512 KB means ul2 lat = 7
    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 8
  * 2-way set associative:
    * ul2 = 64KB (baseline, minimum size) means ul2lat = 5
    * ul2 = 128 KB means ul2lat = 6
    * ul2 = 256 KB means ul2lat = 7
    * ul2 = 512 KB means ul2 lat = 8
    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 9
  * 4-way set associative:
    * ul2 = 64KB (baseline, minimum size) means ul2lat = 6
    * ul2 = 128 KB means ul2lat = 7
    * ul2 = 256 KB means ul2lat = 8
    * ul2 = 512 KB means ul2 lat = 9
    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 10
  * 8-way set associative:
    * ul2 = 64KB (baseline, minimum size) means ul2lat = 7
    * ul2 = 128 KB means ul2lat = 8
    * ul2 = 256 KB means ul2lat = 9
    * ul2 = 512 KB means ul2 lat = 10
    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 11
  * 16-way set associative:
    * ul2 = 64KB (baseline, minimum size) means ul2lat = 8
    * ul2 = 128 KB means ul2lat = 9
    * ul2 = 256 KB means ul2lat = 10
    * ul2 = 512 KB means ul2 lat = 11
    * ul2 = 1024 KB (1 MB) (maximum size) means ul2lat = 12

4.5. By inference, ul2 associativity is limited to 1, 2, 4, 8, 16

5. Miscellaneous:
  * bpred can be any EXCEPT perfect
  * mplat is fixed at 3
  * fetch:speed ratio max is 4
    * **Question: can the ratio be a decimal?**
  * ifqsize can be set to a maximum of 16 words (64B)
    * **Inconsistent: doesn't match restriction 1, which suggests that 1 word is 8B**
  * decode:width <= fetch:ifqsize; decode:width = 1, 2, 4, 8
  * imult + ialu <= 2 * issue:width
  * fpalu + fpmult <= 2 * issue:width
  * mem:width = 8, 16
  * res:memport = 1, 2 (probably just want to keep this as 2 for all experiments)
  * mem:lat is fixed at 90 + 10 cycles
  * tlb:lat is fixed at 30 (default), page size 4096 (default)
  * maximum tlb sizes of 256 entries for itlb and 512 entries for dtlb
    * itlb entries: 1,2,4,8,16,32,64,128,256
    * dtlb entries: 1,2,4,8,16,32,64,128,256,512
    * **Question: Does "entries" mean sets or sets x associativity?**
  * bpred:ras between 0 and 16, inclusive
  * bpred:btb max of 1024 sets, 1-, 2-, 4-way
  * ruu:size - no more than 8 times the issue width, max 64
  * lsq:size - no more than 4 times the issue width, max 32