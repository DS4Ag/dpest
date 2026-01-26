import os
from collections import defaultdict

# Raw table copied from simulation.cde (*Simulation/Crop Models section)
SIMULATION_CROP_MODELS = """
BSCER    BS   CERES-Sugarbeet
CRGRO    BC   CROPGRO-Carinata
CRGRO    BH   CROPGRO-Bahia
CRGRO    BN   CROPGRO-Dry bean
CRGRO    BR   CROPGRO-Brachiaria
CRGRO    CB   CROPGRO-Cabbage
CRGRO    CH   CROPGRO-Chickpea
CRGRO    CI   CROPGRO-Chia
CRGRO    CN   CROPGRO-Canola
CRGRO    CO   CROPGRO-Cotton
CRGRO    CP   CROPGRO-Cowpea
CRGRO    FA   CROPGRO-Fallow
CRGRO    FB   CROPGRO-Faba bean
CRGRO    GB   CROPGRO-Grean bean
CRGRO    GY   CROPGRO-Guar
CRGRO    LT   CROPGRO-Lentil
CRGRO    NP   CROPGRO-Napier grass
CRGRO    PE   CROPGRO-Pea
CRGRO    PN   CROPGRO-Peanut
PRFRM    PO   FORAGE-Perennial peanut
CRGRO    PP   CROPGRO-Pigeonpea
CRGRO    PR   CROPGRO-Bellpepper
CRGRO    QU   CROPGRO-Quinoa
CRGRO    SF   CROPGRO-Safflower
CRGRO    SB   CROPGRO-Soybean
CRGRO    SR   CROPGRO-Strawberry
CRGRO    SU   CROPGRO-Sunflower
CRGRO    TM   CROPGRO-Tomato
CRGRO    VB   CROPGRO-Velvetbean
CSCER    BA   CROPSIM-CERES-Barley
CSCER    WH   CROPSIM-CERES-Wheat
CSCRP    BA   CSCRP-Barley
CSCAS    CS   CSCAS-Cassava
CSYCA    CS   MANIHOT-Cassava
CSCRP    WH   CSCRP-Wheat
MLCER    ML   CERES-Millet
MZCER    MZ   CERES-Maize
MZIXM    MZ   IXIM-Maize
PTSUB    PT   SUBSTOR-Potato
RICER    RI   CERES-Rice
SCCAN    SC   CANEGRO-Sugarcane
SCCSP    SC   CASUPRO-Sugarcane
SCSAM    SC   SAMUCA-Sugarcane
SGCER    SG   CERES-Sorghum
SWCER    SW   CERES-Sweetcorn
PIALO    PI   ALOHA-Pineapple
TRARO    TR   AROIDS-Taro
TNARO    TN   AROIDS-Tanier
TFAPS    TF   NWHEAT-Teff
TFCER    TF   CERES-Teff
WHAPS    WH   NWHEAT-Wheat
PRFRM    BM   FORAGE-Bermudagrass
PRFRM    BR   FORAGE-Brachiaria
PRFRM    BH   FORAGE-Bahiagrass
PRFRM    AL   FORAGE-Alfalfa
PRFRM    GG   FORAGE-Guinea grass
SUOIL    SU   OILCROP-Sunflower
"""


def _normalise_crop_name(description: str) -> str:
    """
    Convert the crop part of the Description column to the dpest crop
    directory naming convention: lowercase, no spaces.

    For example:
      'CROPGRO-Dry bean' -> 'drybean'
      'CERES-Maize'      -> 'maize'
      'FORAGE-Bermudagrass' -> 'bermudagrass'
    """
    # The crop name is always after the last '-' in the Description
    crop_part = description.split("-")[-1].strip()
    return crop_part.replace(" ", "").lower()


def _extract_model_name(description: str) -> str:
    """
    Extract the model name from the Description column, i.e. the prefix of
    the string before the last '-' (without the crop name).

    For example:
      'CROPGRO-Dry bean'         -> 'CROPGRO'
      'CROPSIM-CERES-Wheat'      -> 'CROPSIM-CERES'
      'FORAGE-Perennial peanut'  -> 'FORAGE'
    """
    parts = description.split("-")
    if len(parts) <= 1:
        return description.strip()
    # Drop the last part (crop name) and join the rest back
    model_part = "-".join(parts[:-1]).strip()
    return model_part


def create_model_directories(base_dir: str = "."):
    """
    Create model subdirectories inside each crop directory under ``base_dir``
    using the table in ``SIMULATION_CROP_MODELS``.

    The script assumes:
      * It is run from the ``dpest`` directory.
      * Crop directories already exist and are named as lowercase, no spaces
        (e.g. 'wheat', 'sugarbeet', 'bermudagrass').
      * For each line in the table, the crop directory name is derived from
        the crop part of the Description (last token after '-'), lowercased
        and with spaces removed.
      * Model directory names are derived from the Description prefix
        (everything before the last '-'), converted to lowercase and with
        spaces removed (e.g. 'CROPGRO-Dry bean' -> 'cropgro',
        'CROPSIM-CERES-Wheat' -> 'cropsim-ceres').

    At the end, prints:
      * Total number of model directories created.
      * List of crop directories that were not found under ``base_dir``.
    """
    base_dir = os.path.abspath(base_dir)
    created_dirs = []
    missing_crops = defaultdict(int)

    for line in SIMULATION_CROP_MODELS.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("@"):
            continue

        # Split MODEL, CROP, Description. Description can contain spaces.
        parts = line.split()
        if len(parts) < 3:
            continue
        description = " ".join(parts[2:])

        crop_name = _normalise_crop_name(description)
        model_name = _extract_model_name(description)
        model_dir_name = model_name.replace(" ", "").lower()

        crop_dir = os.path.join(base_dir, crop_name)

        if not os.path.isdir(crop_dir):
            missing_crops[crop_name] += 1
            continue

        target_dir = os.path.join(crop_dir, model_dir_name)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            created_dirs.append(target_dir)

    # Reporting
    print(f"Number of model directories created: {len(created_dirs)}")
    for d in created_dirs:
        print(f"  created: {d}")

    if missing_crops:
        print("\nCrop directories not found (with line counts):")
        for crop, count in sorted(missing_crops.items()):
            print(f"  {crop}: {count} entries")
    else:
        print("\nAll crop directories were found.")


if __name__ == "__main__":
    # Run from the dpest directory
    create_model_directories(base_dir=".")