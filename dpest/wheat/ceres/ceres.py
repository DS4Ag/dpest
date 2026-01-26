# from dpest.plantgro import plantgro
#
# plantgro_observations, plantgro_ins_path = plantgro(
#     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
#     treatment='WW23_G-1',
#     variables='CWAD'
# )

# from dpest.utils.rstfle import rstfle
# #urstfle('PEST_CONTROL.pst', "restart")
# urstfle('PEST_CONTROL.pst', 'restart')
#
# from dpest.utils.pestmode import pestmode
# upestmode('PEST_CONTROL.pst', 'estimation')

# ##
#
# from dpest.utils.rlambda1 import rlambda1
# urlambda1('PEST_CONTROL.pst', new_value = 5.0)
#
# from dpest.utils.rlamfac import rlamfac
# urlamfac('PEST_CONTROL.pst', 2.0)
#
# from dpest.utils.phiratsuf import phiratsuf
# uphiratsuf('PEST_CONTROL.pst', 0.3)
#
# from dpest.utils.phiredlam import phiredlam
# uphiredlam('PEST_CONTROL.pst', 0.03)
#
# from dpest.utils.numlam import numlam
# unumlam('PEST_CONTROL.pst', 10)
#

##
# from dpest.utils.relparmax import relparmax
# urelparmax('PEST_CONTROL.pst', 0.2)  # Valid

# from dpest.utils.facparmax import facparmax
# ufacparmax('PEST_CONTROL.pst', 2.5)

# from dpest.utils.facorig import facorig
# ufacorig('PEST_CONTROL.pst', 0.001)

###
# from dpest.utils.phiredswh import phiredswh
# uphiredswh('PEST_CONTROL.pst', 0.2)

# from dpest.utils.phiredstp import phiredstp
# uphiredstp('PEST_CONTROL.pst', 0.001)

# from dpest.utils.nphistp import nphistp
# unphistp('PEST_CONTROL.pst', 1)   # Valid

# from dpest.utils.nphinored import nphinored
# unphinored('PEST_CONTROL.pst', 5)    # Valid

# from dpest.utils.relparstp import relparstp
# urelparstp('PEST_CONTROL.pst', 0.02)  # Valid

# from dpest.utils.nrelpar import nrelpar
# unrelpar('PEST_CONTROL.pst', 4)   # Valid

# ##
# from dpest.utils.rmv_splitcols import rmv_splitcols
# rmv_splitcols('PEST_CONTROL.pst')

#######################
# from dpest.utils import lsqr
# lsqr(
#     pst_path = "PEST_CONTROL.pst"
# )

# from dpest.utils import svd
# svd(
#     pst_path = "PEST_CONTROL.pst",
#     maxsing = 500,
#     eigthresh = 0.01,
#     eigwrite = 1
# )
# svd(
#     pst_path="PEST_CONTROL.pst"
# )

# from dpest.utils.lsqr import lsqr
#
# lsqr(
#     pst_path = "PEST_CONTROL.pst", lsqrmode = 1
# )


# from dpest.utils import lsqr
#
# lsqr(
#     pst_path = "PEST_CONTROL.pst",
#     lsqr_atol = 1e-6,
#     lsqr_btol = 1e-6,
#     lsqr_itnlim = 50
# )
########################

# # Create CULTIVAR parameters TPL file
# cultivar_parameters, cultivar_tpl_path = cul('ENTRY 1',
#                                             'C:/DSSAT48/Genotype/WHCER048.CUL')
# # Create OVERVIEW observations INS file
# overview_observations, overview_ins_path = overview(
#     treatment = 'WW23_G-1',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT'
# )
#
# pst(
#     cultivar_parameters,
#     dataframe_observations = [overview_observations],
#     model_comand_line = 'py C:/pest18/run_dssat.py',
#     input_output_file_pairs = [
#         (cultivar_tpl_path, 'C:/DSSAT48/Genotype/WHCER048.CUL'),
#         (overview_ins_path, 'C:/DSSAT48/Wheat/OVERVIEW.OUT')
#     ],
# )

########################
from dpest.wheat.ceres import cul
# from dpest import overview, plantgro, uplantgro, pst

# ### 1. Create CULTIVAR parameters TPL file
# # Call the function
cultivar_parameters, cultivar_tpl_path = cul(
    # P = 'P1V, P1D, P5', # Why the user should enter the parameters
    # G = 'G1, G2, G3',
    # PHINT = 'PHINT',
    cultivar = 'MANITOU',
    cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL'
)




# ### 2. Create ECOTYPE parameters TPL file
# ecotype_parameters, ecotype_tpl_path = eco(
#     PHEN = 'P1, P2FR1, P2, P3, P4FR1, P4FR2, P4',
#     VERN = 'VEFF',
#     ecotype = 'CAWH01',
#     eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO'
# )
#
# ## 3. Create OVERVIEW observations INS file
# overview_observations, overview_ins_path = overview(
#     crop = 'wheat',
#     model = 'ceres',
#     treatment = '164.0 KG N/HA IRRIG',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     variables_classification = {
#         'Emergence (DAP)': 'phenology',
#         'Anthesis (DAP)': 'phenology',
#         'Maturity (DAP)': 'phenology',
#         'Product wt (kg dm/ha;no loss)': 'yield',
#         'Maximum leaf area index': 'lai',
#         'Canopy (tops) wt (kg dm/ha)': 'biomass',
#         'N uptake (kg/ha)': 'nitrogen'
#     }
# )

# # # print(overview_observations)
# #
# # ### 4. Create PlantGro observations INS file
# # plantgro_observations, plantgro_ins_path = plantgro(
# #     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
# #     treatment = '164.0 KG N/HA IRRIG',
# #     variables = ['LAID', 'CWAD', 'T#AD']
# #     # variable_classifications = {
# #     #     'lai' : 'LAID',
# #     #     'biomass' : 'CWAD',
# #     #     'plant_structure': 'T#AD'
# #     # }
# # )
# #
# # print(plantgro_observations)
# #
# # # pst(
# # #     cultivar_parameters = cultivar_parameters,
# # #     ecotype_parameters = ecotype_parameters,
# # #     dataframe_observations = [overview_observations, plantgro_observations],
# # #     model_comand_line = r'py "C:\pest18\run_dssat.py"',
# # #     input_output_file_pairs = [
# # #         (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
# # #         (ecotype_tpl_path, 'C://DSSAT48/Genotype/WHCER048.ECO'),
# # #         (overview_ins_path , 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
# # #         (plantgro_ins_path , 'C://DSSAT48/Wheat/PlantGro.OUT')
# # #     ]
# # # )
# #
# #
# # pst(
# #     cultivar_parameters=cultivar_parameters,
# #     dataframe_observations= plantgro_observations,
# #     model_comand_line=r'py "C:\pest18\run_dssat.py"',
# #     input_output_file_pairs=[
# #         (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
# #         (plantgro_ins_path, 'C://DSSAT48/Wheat/PlantGro.OUT')
# #     ]
# # )
# # #
# # # # uplantgro(
# # # #     'C:/DSSAT48/Wheat/PlantGro.OUT',
# # # #     #'164.0 KG N/HA IRRIG',
# # # #     #'123.0 KG N/HA IRRIG',
# # # #     #['LAID', 'CWAD']
# # # #     'DR22_G-14',
# # # #     'LAID')
# #
#
#
# # #### 1 Create CULTIVAR parameters TPL file ROOTS ANATOMY
# # # Call the function
# # cultivar_parameters, cultivar_tpl_path = cul(
# #     # P = 'P1V, P1D, P5', # Why the user should enter the parameters
# #     # G = 'G1, G2, G3',
# #     # PHINT = 'PHINT',
# #     cultivar = 'ENTRY 2',
# #     cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL',
# #     #output_path = "C:/Users/luizv/OneDrive_Purdue/OneDrive - purdue.edu/Thesis/PEST_DSSAT_function",
# # )
# #
# # #### 2. Create ECOTYPE parameters TPL file
# # # Call the function
# # ecotype_parameters, ecotype_tpl_path = eco(
# #     PHEN = 'P1, P2FR1, P2, P3, P4FR1, P4FR2, P4',
# #     VERN = 'VEFF',
# #     ecotype = 'CAWH02',
# #     eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO',
# # )
#
# ## 3. Create OVERVIEW observations INS file
# # Call the function
# # overview_observations, overview_ins_path = overview(
# #     treatment = 'WW23_G-1',
# #     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
# #     variables = ['Emergence (DAP)', 'Maturity (DAP)', 'Product wt (kg dm/ha;no loss)']
# #     output_filename=
# #     # variable_classifications={
# #     #     'Anthesis (DAP)': 'phenology',
# #     #     'Maturity (DAP)': 'phenology',
# #     #     'Product wt (kg dm/ha;no loss)': 'yield',
# #     #     'Maximum leaf area index': 'lai',
# #     #     'Canopy (tops) wt (kg dm/ha)': 'biomass',
# #     #     'Above-ground N (kg/ha)': 'nitrogen'
# #     # }
# # )
#
# overview_observations_trt1,  overview_ins_path_trt1 = overview(
#     treatment = '82.0 KG N/HA IRRIG',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     suffix = 'TRT1'
# )
#
# overview_observations_trt2,  overview_ins_path_trt2 = overview(
#     treatment = '123.0 KG N/HA IRRIG',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     suffix = 'TRT2'
# )
#
# overview_observations_trt3,  overview_ins_path_trt3 = overview(
#     treatment = '164.0 KG N/HA IRRIG',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     suffix = 'TRT3'
# )
#
#
# # Display all columns
# # pd.set_option('display.max_columns', None)
# # print(overview_observations_trt3)
#
# #### 4. Create PlantGro observations INS file
# # plantgro_observations, plantgro_ins_path = plantgro(
# #     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
# #     treatment = 'WW23_G-1',
# #     variables = ['LAID', 'CWAD']
# # )
#
# plantgro_observations_trt1, plantgro_ins_path_trt1 = plantgro(
#     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
#     treatment = '82.0 KG N/HA IRRIG',
#     variables = ['LAID', 'CWAD', 'T#AD'],
#     suffix = 'TRT1'
# )
#
# plantgro_observations_trt2, plantgro_ins_path_trt2 = plantgro(
#     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
#     treatment = '123.0 KG N/HA IRRIG',
#     variables = ['LAID', 'CWAD', 'T#AD'],
#     suffix = 'TRT2'
# )
#
# plantgro_observations_trt3, plantgro_ins_path_trt3 = plantgro(
#     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
#     treatment = '164.0 KG N/HA IRRIG',
#     variables = ['LAID', 'CWAD', 'T#AD'],
#     suffix = 'TRT3'
# )
#
# #print(plantgro_observations)
# #
# # #
# #### 5. Create the PST file
# pst(
#     cultivar_parameters = cultivar_parameters,
#     dataframe_observations = [overview_observations_trt1, overview_observations_trt2, overview_observations_trt3,
#                               plantgro_observations_trt1, plantgro_observations_trt2, plantgro_observations_trt3],
#     model_comand_line = r'py "C:\pest18\run_dssat.py"',
#     input_output_file_pairs = [
#         (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
#         (overview_ins_path_trt1, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
#         (overview_ins_path_trt2, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
#         (overview_ins_path_trt3, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
#         (plantgro_ins_path_trt1, 'C:/DSSAT48/Wheat/PlantGro.OUT'),
#         (plantgro_ins_path_trt2, 'C:/DSSAT48/Wheat/PlantGro.OUT'),
#         (plantgro_ins_path_trt3, 'C:/DSSAT48/Wheat/PlantGro.OUT')
#     ]
# )
# #
# # uplantgro(
# #     'C:/DSSAT48/Wheat/PlantGro.OUT',
# #     #'164.0 KG N/HA IRRIG',
# #     #'123.0 KG N/HA IRRIG',
# #     #['LAID', 'CWAD']
# #     'DR22_G-14',
# #     'LAID',
# #     nspaces_year_header = 5)
# # var_stats = (
# #     improved_df
# #     .groupby('variable')['value']
# #     .agg(['mean', 'max', 'min'])
# # )

