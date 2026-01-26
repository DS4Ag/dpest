from dpest import spe

species_parameters, species_tpl_path = spe(
    species_file_path = 'C:/DSSAT48/Genotype/SBGRO048.SPE',
    PARMAX = (4, 1, 20.0, 60.0, 'PHOTOSYN'),
    PARMAY = (4, 2, 40.0, 80.0, 'PHOTOSYN'),
    KCAN = (4, 3, 0.0, 1.0, 'PHOTOSYN'),
    YLMAXT_1 = (14, 1, 0.0, 20.0, 'TEMP_RESP'),
    YLMAXT_2 = (14, 2, 0.0, 20.0, 'TEMP_RESP'),
    YLMAXT_3 = (14, 3, 0.0, 20.0, 'TEMP_RESP'),
    YLMAXT_4 = (14, 4, 0.0, 20.0, 'TEMP_RESP'),
    YLMAXT_6 = (14, 6, 0.0, 20.0, 'TEMP_RESP'),
    FNPGL_1 = (15, 1, 0.0, 20.0, 'TEMP_RESP'),
    FNPGL_2 = (15, 2, 0.0, 20.0, 'TEMP_RESP'),
)

print(species_parameters)


species_parameters, species_tpl_path = spe(
    species_file_path = 'C:/DSSAT48/Genotype/WHCER048.SPE',
    PGERM = (15, 1, 0, 20.0, 'Phase_dur'),
    P0 = (15, 3, -5, 5, 'Phase_dur'),
    Fac = (19, 1, 0, 2, 'Phase_dur'),
    h = (19, 2, 10, 30, 'Phase_dur'),
    GrStg = (19, 3, 0, 4, 'Phase_dur'),
    LWLOS = (30, 3, 0, 6, 'Phase_dur')
)