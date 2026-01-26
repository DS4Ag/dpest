ptf ~
$ECOTYPES:WHCER048.20200721   Last edit: 2020-07-21 CHP
!
! COEFF   DEFINITION
! =====   ==========
! AWNS    Awn score (0-10;10=very long)
! ECO#    Code for the ecotype (code)
! GN%MN   Minimum grain N (%)
! GN%S    Standard grain N (%)
! HTSTD   Standard canopy height (cm)
! KCAN    PAR extinction coefficient (#)
! LA1S    Area of standard first leaf (cm2)
! LAFR    Increase in potential area of leaves,reproductive phase (fr/leaf)
! LAFV    Increase in potential area of leaves,vegetative phase (fr/leaf)
! LARS    Area of standard reproductive phase leaf (cm2)
! LAVS    Area of standard vegetative phase leaf (cm2)
! LLIFE   Life of leaves during vegetative phase (phyllochrons)
! LSPHE   Final leaf senescence ends (GrowhStage)
! LSPHS   Final leaf senescence starts (GrowhStage)
! P1      Duration of phase end juvenile to terminal spikelet (PVTU)
! P2      Duration of phase terminal spikelet to end leaf growth (TU)
! P2FR1   Duration of phase terminal spikelet to jointing (fr P2)
! P3      Duration of phase end leaf growth to end spike growth (TU)
! P4      Duration of phase end spike growth to end grain fill lag (TU)
! P4FR1   Duration of phase end spike growth to anthesis (fr P4)
! P4FR2   Duration of phase anthesis start to anthesis end (fr P4)
! PARU2   PAR conversion to dm ratio,after last leaf (g/MJ) (If -99,set to PARUE)
! PARUE   PAR conversion to dm ratio,before last leaf stage (g/MJ)
! PHFn    Factor by which PHINTS is multiplied -> PHINT for phase (#)
! PHLn    Leaf # produced during phyllochron phase (#)
! PPFPE   Daylength factor,pre emergence (#,0-1)
! RDGS    Root depth growth rate,early phase (cm/standard d)
! RS%S    Reserves part of assimilates going to stem (%)
! SLAS    Specific leaf area,standard first leaf (cm2/g)
! TDFAC   Tiller death factor (%/st.day when tiller wt 2xstandard wt)
! TDPHE   Tiller death ending stage (GrowthStage)
! TDPHS   Tiller death start stage (GrowthStage)
! TIFAC   Tiller initiation (rate) factor (fr of phyllochron based) (#)
! TIL#S   Tiller production starts (leaf #)
! TIPHE   Tillering phase end stage (GrowthStage)
! TKFH    Temperature at which killed when fully hardened (oC)
! VEFF    Vernalization effect (Rate reduction when unvernalized (fr)
! WFGU    Water stress factor,growth,upper (fr)
! WFPU    Water stress factor,photosynthesis,upper (fr)
!
! Coefficients presented here differ from those used in DSSAT
! Version 3.5. They have been developed from 'parameters'
! embedded in the code of the Ceres model,from the Cropsim model,
! and from the literature. They are likely to change as more
! experience is gained, and should not yet be taken as fixed.
 
! In Ceres3.5, P1=400 for PHINT=95; P2=phint*3; P3=phint*2; P4=200,
! with anthesis occurring in P4 after 80 units.
 
*ECOTYPE:WHCER048
!         ------PHENOLOGY(PHASE_DURATIONS)------ P.MOD --MAX_RUE--  LEAF PRODN  ------LEAF_SIZES------ LEAF_SENESC TILLER_PRODUCTION ---TILLER_DEATH-- ROOTS -----CANOPY------  ---COMPOSITION--  KILL
@ECO#     P1 P2FR1    P2    P3 P4FR1 P4FR2    P4  VEFF PARUE PARU2  PHL2  PHF3  LA1S  LAFV  LAFR  SLAS LSPHS LSPHE TIL#S TIPHE TIFAC TDPHS TDPHE TDFAC  RDGS HTSTD  AWNS  KCAN  RS%S  GN%S GN%MN  TKFH
!          1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32
!       oC.d    fr  oC.d  oC.d    fr    fr  oC.d    fr  g/MJ  g/MJ   Lf#   Fac   cm2 fr/lf fr/lf cm2/g GrStg GrStg   Lf# GrStg   Fac GrStg GrStg.  Fac  cm/d    cm Score   Exp     %     %     %    oC
999991   100     0   100   100  0.15  0.05   100   0.0   1.0   1.0   4.0   1.0   1.0  0.01  0.10   100   4.0   5.5   2.3  1.95   0.5   1.5   2.0   0.0   1.0    60   0.0   .65    10   1.0   0.0   -25
999992   500   .60   500   500  0.35  0.50   500   1.0   6.0   6.0   200   1.6  20.0  0.80  3.00   600   5.7   6.5   7.0   4.0   2.0   4.0   6.0  20.0   5.0   150  10.0   .95    60   3.5   6.0   -10
 
DFAULT   200   .25   200   200  0.25  0.10   200   0.6   2.7   2.7    15   1.3   5.0  0.10  0.50   400   5.5   6.3   3.5   2.5   1.0   2.5   6.0   4.0   3.0   100   0.0   .85    30   3.0   0.0   -10
 
CAWH01 ~P1 ~ ~P2F~ ~P2 ~ ~P3 ~ ~P4F~ ~P41~ ~P4 ~ ~VEF~   2.7   2.7    13   1.0   3.0  0.05  0.30   300   4.2   6.0   3.0   2.5   1.0   2.7   6.0   4.0   3.0   100   0.0   .85    30   3.0   2.0   -10
USWH01   400   .25   285   190   .25   .10   200   1.0   2.3   2.3    13   1.0   2.0  0.15  0.01   400   5.1   6.5   4.5   2.0   0.8   2.2   6.0   4.0   3.0   100   5.0   .85    30   2.2   1.9   -20
UKWH01   421   .25   300   200   .25   .10   200   0.5   2.7   2.7    13   1.0   2.0  0.10  0.30   485   5.7   6.3   4.5   2.0   0.5   2.2   6.0  20.0   3.0   100   0.0   .85    60   2.0   1.0   -15
 
AZWH18   460   .25   328   219   .25   .10   200   0.6   2.7   2.7    13   1.0   2.0  0.15  0.50   400   5.3   6.5   4.5   2.0   0.8   2.2   6.0   4.0   3.0   100   5.0   .85    30   2.2   1.9   -20
!@ECO#     P1 P2FR1    P2    P3 P4FR1 P4FR2    P4  VEFF PARUE PARU2  PHL2  PHF3  LA1S  LAFV  LAFR  SLAS LSPHS LSPHE TIL#S TIPHE TIFAC TDPHS TDPHE TDFAC  RDGS HTSTD  AWNS  KCAN  RS%S  GN%S GN%MN  TKFH
CI0001   400   .25   280   200   .25   .10   260   0.6   2.0   2.5    13   1.0  10.0  0.30  0.40   350   5.4   6.1   2.3  1.95   2.0   2.8   6.0   4.0   3.0   100   5.0   .85    30   2.2   1.9   -20
 
TXWH01   400   .25   285   190   .25   .10   200   1.0   1.5   1.5    13   1.0   2.0  0.15  0.01   400   5.1   6.5   4.5   2.0   0.8   2.2   6.0   4.0   3.0   100   5.0   .85    30   2.2   1.9   -20
TWKG01   421   .25   300   240   .25   .10   240   1.0   2.3   2.3    13   1.0   5.0  0.10  0.55   400   5.7   6.3   4.5   2.0   0.5   2.0   5.0   0.5   3.0   100   0.0   .85    60   2.0   0.0   -15

! ----------------------------------------------------------------------------
! 1. Ecotype calibration
! ----------------------------------------------------------------------------
!@ECO#     P1 P2FR1    P2    P3 P4FR1 P4FR2    P4  VEFF PARUE PARU2  PHL2  PHF3  LA1S  LAFV  LAFR  SLAS LSPHS LSPHE TIL#S TIPHE TIFAC TDPHS TDPHE TDFAC  RDGS HTSTD  AWNS  KCAN  RS%S  GN%S GN%MN  TKFH
! ------ Data subset A ------
CI0500 400.0 .2500 280.0 200.0 .1540 .0500 260.0 .5386 1.791 2.691 13.00 1.000 9.971 .2978 .3984 350.0 5.520 6.283 2.300 1.950 1.999 3.254 6.000 3.997 3.281 100.0 5.000 .8643 30.01 2.137 1.900 -20.0
CI0501 400.0 .2500 280.0 200.0 .1500 .0500 260.0 .5208 1.926 2.745 13.00 1.000 10.00 .3021 .4000 350.0 5.513 6.126 2.300 1.950 1.998 2.795 6.000 3.991 2.660 100.0 5.000 .6500 30.00 2.100 1.900 -20.0
CI0502 400.0 .2500 280.0 199.9 .2375 .0870 259.9 .4570 2.013 2.441 13.00 1.000 10.01 .2298 .4507 350.0 5.558 6.222 2.300 1.950 1.961 2.982 6.000 4.001 2.683 100.0 5.000 .8835 30.00 2.114 1.900 -20.0
CI0503 400.0 .2500 280.0 200.0 .1500 .0997 260.0 .4873 1.879 2.461 13.00 1.000 10.00 .2998 .3999 350.0 5.426 6.164 2.300 1.951 1.999 2.807 6.000 4.000 2.972 100.0 5.000 .8535 30.00 2.203 1.900 -20.0
 
! ------ Data subset B ------
CI0600 400.0 .2500 280.0 200.0 .1540 .0500 260.0 .5386 1.791 2.691 13.00 1.000 9.971 .2978 .3984 350.0 5.520 6.283 2.300 1.950 1.999 3.254 6.000 3.997 3.281 100.0 5.000 .8643 30.01 2.137 1.900 -20.0
CI0601 400.0 .2500 280.0 200.0 .2307 .0999 260.0 .5658 1.668 2.697 13.00 1.000 10.00 .3000 .3999 350.0 5.471 6.129 2.300 1.950 1.995 2.813 6.000 3.997 2.965 100.0 5.000 .8311 30.00 2.190 1.900 -20.0
CI0602 400.0 .2500 280.0 200.0 .1801 .0500 260.0 .4756 1.862 2.437 13.00 1.000 10.00 .3000 .4000 350.0 5.447 6.180 2.300 1.950 1.999 2.870 5.999 3.999 2.989 100.0 5.000 .9500 30.00 2.195 1.900 -20.0
CI0603 400.0 .2500 280.0 200.0 .2358 .1000 260.0 .4567 1.930 2.443 13.00 1.000 9.989 .3000 .4000 350.0 5.585 6.250 2.300 1.950 1.996 2.813 6.000 3.996 2.983 100.0 5.000 .8914 30.00 2.203 1.900 -20.0
 
! ------ Data subset C ------
CI0700 400.0 .2500 279.9 199.7 .2194 .0710 260.0 .5896 1.609 3.129 13.00 1.000 10.03 .3000 .3996 350.0 5.692 6.313 2.300 2.085 1.957 4.000 5.997 4.004 3.512 100.0 5.000 .9500 30.00 1.656 1.922 -20.0
CI0701 400.0 .2500 280.0 200.0 .1665 .0500 260.0 .5037 2.015 2.483 13.00 1.000 10.00 .3009 .3992 350.0 5.543 6.204 2.300 1.950 1.991 2.717 6.000 3.994 2.390 100.0 5.000 .7638 30.00 2.120 1.900 -20.0
CI0702 400.0 .2500 279.9 199.8 .1565 .0543 259.9 .4963 1.947 2.551 13.00 1.000 9.960 .2446 .3584 350.0 5.700 6.497 2.301 1.950 1.997 3.165 5.995 3.669 3.597 100.0 5.000 .6500 30.03 2.132 1.900 -20.0
 
! ------ Data subset D ------
CI0800 400.0 .2500 279.5 199.3 .1500 .0500 260.0 .6049 1.690 3.160 13.00 1.000 10.01 .3000 .4000 350.0 5.451 6.131 2.300 1.950 1.991 2.823 6.000 4.003 2.972 100.0 5.000 .8870 30.00 2.148 1.900 -20.0
CI0801 400.1 .2500 280.0 200.0 .1534 .1000 260.0 .5409 1.788 2.389 13.00 1.000 10.00 .3002 .3998 350.0 5.563 6.210 2.300 1.950 1.994 2.875 6.000 4.005 2.896 100.0 5.000 .8444 30.01 2.209 1.900 -20.0
CI0802 400.0 .2500 280.0 200.0 .2758 .1000 260.0 .4615 1.991 2.541 13.00 1.000 9.918 .3000 .4000 350.0 5.700 6.291 2.300 1.950 1.969 3.122 6.000 3.988 3.007 100.0 5.000 .6500 30.03 2.124 1.900 -20.0
CI0803 400.0 .2500 280.0 200.0 .1959 .0915 260.0 .5271 1.759 2.839 13.00 1.000 9.994 .3013 .3989 350.0 5.480 6.166 2.300 1.950 1.999 2.822 6.000 3.976 2.937 100.0 5.000 .8648 30.00 2.178 1.900 -20.0
