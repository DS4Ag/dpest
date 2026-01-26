
########################
from dpest import cul, eco
from dpest import overview, ts, uts, pst



###### SOYBEAN
# ### 1. Create CULTIVAR parameters TPL file
# # Call the function
cultivar_parameters, cultivar_tpl_path = cul(
    cultivar = 'M GROUP   0',
    cul_file_path = 'C:/DSSAT48/Genotype/SBGRO048.CUL'
)

### 2. Create ECOTYPE parameters TPL file
ecotype_parameters, ecotype_tpl_path = eco(
    EARLY_PHEN = 'PL-EM, EM-V1, V1-JU, JU-R0',
    REPRO_TIMING = 'PM06, PM09, LNGSH, R7-R8, FL-VS',
    LEAF_APP = 'TRIFL',
    CANOPY_FORM = 'RHGHT, RWDTH',
    POST_R1_PHOTO = 'R1PPO',
    LOWT_FLO = 'OPTBI, SLOBI',
    ecotype = 'SB0001',
    eco_file_path = 'C:/DSSAT48/Genotype/SBGRO048.ECO'
)

print('ecotype_parameters: ', ecotype_parameters)

print('ecotype_tpl_path', ecotype_tpl_path)
###### WHEAT
### 1. Create CULTIVAR parameters TPL file
# Call the function
cultivar_parameters, cultivar_tpl_path = cul(
    P = 'P1V, P1D, P5', # Why the user should enter the parameters
    G = 'G1, G2, G3',
    PHINT = 'PHINT',
    cultivar = 'MANITOU',
    cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL'
)

### 2. Create ECOTYPE parameters TPL file
ecotype_parameters, ecotype_tpl_path = eco(
    PHEN = 'P1, P2FR1, P2, P3, P4FR1, P4FR2, P4',
    VERN = 'VEFF',
    ecotype = 'CAWH01',
    eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO'
)

## 3. Create OVERVIEW observations INS file

# WHEAT
# overview_observations, overview_ins_path = overview(
#     treatment = '164.0 KG N/HA IRRIG',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     crop = 'wh',
#     model = 'CSCER',
#     # variables_classification = {
#     #     'Emergence (DAP)': 'phenology',
#     #     'Anthesis (DAP)': 'phenology',
#     #     'Maturity (DAP)': 'phenology',
#     #     'Product wt (kg dm/ha;no loss)': 'yield',
#     #     'Maximum leaf area index': 'lai',
#     #     'Canopy (tops) wt (kg dm/ha)': 'biomass',
#     #     'N uptake (kg/ha)': 'nitrogen'
#     # }
# )

# # SOYBEAN
# overview_observations, overview_ins_path = overview(
#     treatment = '76 Equidist BRAGG',
#     overview_file_path = 'C:/DSSAT48/Soybean/OVERVIEW.OUT',
# )

# SOYBEAN
# overview_observations, overview_ins_path = overview(
#     treatment = '76 Equidist BRAGG',
#     overview_file_path = 'C:/DSSAT48/Soybean/OVERVIEW.OUT',
#     variables_classification = {
#         'Yield at harvest maturity (kg [dm]/ha)': 'yield',
#         'Pod/Ear/Panicle weight at maturity (kg [dm]/ha)': 'yield',
#         'Tops weight at maturity (kg [dm]/ha)': 'biomass',
#         'By-product produced (stalk) at maturity (kg[dm]/ha': 'biomass',
#         'Harvest index at maturity': 'yield',
#         'Threshing % at maturity': 'yield',
#         'Leaf area index, maximum': 'yield'
#     }
# )
#
# print(overview_observations)
#
### 4. Create PlantGro observations INS file
plantgro_observations, plantgro_ins_path = ts(
    treatment='76 Equidist BRAGG',
    ts_file_path='C:/DSSAT48/Soybean/PlantGro.OUT',
    variables=['LWAD', 'SWAD', 'GWAD', 'RWAD', 'CWAD', 'HIAD', 'PWAD', 'LN%D', 'SH%D', 'HIPD', 'SLAD'],
)
#
# # SOYBEAN PlantN
# plantgro_observations, plantgro_ins_path = ts(
#     treatment = '76 Equidist BRAGG',
#     ts_file_path = 'C:/DSSAT48/Soybean/PlantN.OUT',
#     variables = ['LN%D', 'SN%D'],
#     variables_classification = {
#         'nitrogen' : 'LN%D',
#         'nitrogen' : 'CWAD',
#     }
# )
#
# # SOYBEAN PlantC
# plantgro_observations, plantgro_ins_path = ts(
#     treatment = '76 Equidist BRAGG',
#     ts_file_path = 'C:/DSSAT48/Soybean/PlantC.OUT',
#     variables = 'CL%D'
# )
#

# print(plantgro_observations)
#
# pst(
#     cultivar_parameters = cultivar_parameters,
#     ecotype_parameters = ecotype_parameters,
#     dataframe_observations = [overview_observations, plantgro_observations],
#     model_comand_line = r'py "C:\pest18\run_dssat.py"',
#     input_output_file_pairs = [
#         (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
#         (ecotype_tpl_path, 'C://DSSAT48/Genotype/WHCER048.ECO'),
#         (overview_ins_path , 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
#         (plantgro_ins_path , 'C://DSSAT48/Wheat/PlantGro.OUT')
#     ]
# )
#
#
# pst(
#     cultivar_parameters=cultivar_parameters,
#     dataframe_observations= plantgro_observations,
#     model_comand_line=r'py "C:\pest18\run_dssat.py"',
#     input_output_file_pairs=[
#         (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
#         (plantgro_ins_path, 'C://DSSAT48/Wheat/PlantGro.OUT')
#     ]
# )
# #
# uts(
#     'C:/DSSAT48/Wheat/PlantGro.OUT',
#     #'164.0 KG N/HA IRRIG',
#     #'123.0 KG N/HA IRRIG',
#     #['LAID', 'CWAD']
#     'DR22_G-14',
#     'LAID')


# #### 1 Create CULTIVAR parameters TPL file ROOTS ANATOMY
# # Call the function
# cultivar_parameters, cultivar_tpl_path = cul(
#     # P = 'P1V, P1D, P5', # Why the user should enter the parameters
#     # G = 'G1, G2, G3',
#     # PHINT = 'PHINT',
#     cultivar = 'ENTRY 2',
#     cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL',
#     #output_path = "C:/Users/luizv/OneDrive_Purdue/OneDrive - purdue.edu/Thesis/PEST_DSSAT_function",
# )
#
# #### 2. Create ECOTYPE parameters TPL file
# # Call the function
# ecotype_parameters, ecotype_tpl_path = eco(
#     PHEN = 'P1, P2FR1, P2, P3, P4FR1, P4FR2, P4',
#     VERN = 'VEFF',
#     ecotype = 'CAWH02',
#     eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO',
# )

## 3. Create OVERVIEW observations INS file
# Call the function
# overview_observations, overview_ins_path = overview(
#     treatment = 'WW23_G-1',
#     overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
#     variables = ['Emergence (DAP)', 'Maturity (DAP)', 'Product wt (kg dm/ha;no loss)']
#     output_filename=
#     # variable_classifications={
#     #     'Anthesis (DAP)': 'phenology',
#     #     'Maturity (DAP)': 'phenology',
#     #     'Product wt (kg dm/ha;no loss)': 'yield',
#     #     'Maximum leaf area index': 'lai',
#     #     'Canopy (tops) wt (kg dm/ha)': 'biomass',
#     #     'Above-ground N (kg/ha)': 'nitrogen'
#     # }
# )
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


# Display all columns
# pd.set_option('display.max_columns', None)
# print(overview_observations_trt3)

#### 4. Create PlantGro observations INS file
# plantgro_observations, plantgro_ins_path = plantgro(
#     plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
#     treatment = 'WW23_G-1',
#     variables = ['LAID', 'CWAD']
# )
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

#print(plantgro_observations)
#
# #
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
#
# uplantgro(
#     'C:/DSSAT48/Wheat/PlantGro.OUT',
#     #'164.0 KG N/HA IRRIG',
#     #'123.0 KG N/HA IRRIG',
#     #['LAID', 'CWAD']
#     'DR22_G-14',
#     'LAID',
#     nspaces_year_header = 5)
# var_stats = (
#     improved_df
#     .groupby('variable')['value']
#     .agg(['mean', 'max', 'min'])
# )

