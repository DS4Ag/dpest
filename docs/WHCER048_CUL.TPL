ptf ~
$CULTIVARS:WHCER048.20200721   Last edit: 20210-05-06 GH
 
! Coefficients used in the Cropsim-Ceres model differ from those used
! in DSSAT Versions 3.5 and 4.0. They can be calculated (approximately) from
! V3.5 coefficients as follows:
 
! P1V   = P1V(v3.5)*10
! P1D   = P1D(V3.5)*20
! P5    = P5(V3.5)*20 + 430
! G1    = G1(V3.5)*5 + 5
! G2    = (G2(V3.5)*0.35+0.65) * P5/20
! G3    = G3(V3.5)*0.7
! PHINT = PHINT(V3.5)
 
! Converted coefficients,and those listed below,should always be
! tested by using them with real experiments and comparing model
! outputs with measured values.
!
!             P/G/N:Phenology/Growth/Not used for calbration
!
*CULTIVARS:WHCER048
@VAR#  VAR-NAME........  EXP#   ECO#   P1V   P1D    P5    G1    G2    G3 PHINT
!Coeffient #                             1     2     3     4     5     6     7
!Calibration                             P     P     P     G     G     G     N
!                                     Vday %/10h  oC.d   #/g    mg     g  oC.d
999991 MINIMA               . 999991     0     0   100    10    10   0.5    30
999992 MAXIMA               . 999992    60   200   999    50    80   8.0   150
 
DFAULT DEFAULT              . DFAULT     5    75   450    30    35   1.0    60
 
IB1500 MANITOU           1,14 CAWH01 9.333 13.12 331.4 12.11 63.48 2.214 86.00
IB0488 NEWTON             1,6 USWH01 48.45 73.50 505.0 35.42 22.60  0.78 95.00
IB1015 MARIS FUNDIN       1,8 UKWH01 53.02 82.58 529.3 46.99 60.91 6.673 100.0
 
AW0071 Yecora_Rojo      16,33 AZWH18    10  40.0   450    20    60  1.50    95
CI0001 Yecora_Rojo        1,2 CI0001    02    40   570    27    45   4.0   100
KZ0001 North KAZAK1           DFAULT    10   120   670    16    42   2.0    90
 
TX0001 TAMU112              . TXWH01    10  68.0   450    30    30   1.0    30
990015 Hartog_KY          1,4 TWKG01    20    94   700    22    39   1.0   120
 
!-- New cultivars
555175 ENTRY 1            1,1 CAWH01 2.277 58.14 634.4 17.10 46.96 6.350 56.34
457793 ENTRY 2              1 CAWH01 ~P1V~ ~P1D~ ~P5 ~ ~G1 ~ ~G2 ~ ~G3 ~ ~PHI~
518062 ENTRY 3              1 CAWH01 5.066 56.08 365.7 17.43 43.95 .5000 53.63
617502 ENTRY 4              1 CI0001 2.000 26.04 573.6 18.85 49.43 4.169 71.82
617636 ENTRY 5              1 CAWH01 5.793 74.76 350.8 14.48 45.18 .5000 46.75
474812 ENTRY 6              1 CAWH01 1.000 69.09 669.6 18.48 42.14 .5000 52.80
748117 ENTRY 7              1 CI0001 2.000 30.32 571.6 19.69 41.50 4.870 93.72
748118 ENTRY 8              1 CAWH01 1.000 71.82 716.6 16.60 37.29 .5000 52.22
474804 ENTRY 9              1 CAWH01 32.96 53.68 775.5 17.44 39.98 .5000 55.55
474816 ENTRY 10             1 CAWH01 2.000 59.30 571.3 17.00 47.90 8.000 112.2
382535 ENTRY 11             1 CAWH01 1.000 56.76 600.8 15.22 50.11 2.039 58.05
605613 ENTRY 12             1 CAWH01 60.00 50.80 585.2 13.84 53.51 .5000 110.9
542933 ENTRY 13             1 CAWH01 1.000 62.15 609.6 14.90 52.97 1.317 56.19
589328 ENTRY 14             1 CAWH01 2.000 52.94 572.4 18.73 43.59 1.631 114.8
 
 
! 4.8.0 cultivar coefficients (before changes in soil temperature subroutine)
!IB1500 MANITOU           1,14 CAWH01     8   100   320    23    23   2.5    86
!IB0488 NEWTON             1,6 USWH01    45    75   500    25    30   2.0    95
!IB1015 MARIS FUNDIN       1,8 UKWH01    30    83   515    15    44   3.2   100
 
 
! COEFF       DEFINITION
! ========    ==========
! VAR#        Identification code or number for the specific cultivar.
! VAR-NAME    Name of cultivar.
! EXP#        Number of experiments used to generate parameters
! ECO#        Ecotype code for this cultivar,points to entry in ECO file
! P1V         Days,optimum vernalizing temperature,required for vernalization
! P1D         Photoperiod response (% reduction in rate/10 h drop in pp)
! P5          Grain filling (excluding lag) phase duration (oC.d)
! G1          Kernel number per unit canopy weight at anthesis (#/g)
! G2          Standard kernel size under optimum conditions (mg)
! G3          Standard,non-stressed mature tiller wt (incl grain) (g dwt)
! PHINT       Interval between successive leaf tip appearances (oC.d)
