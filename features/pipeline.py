import infra.utils as utils

def run_features(f_file, data_path):
    df = oen(raw_data_from_csv(data_path))
    fns = utils.load_pack(f_file)
    return utils.apply_features(df, fns)
