def load_pack(packname):
    import yaml
    return yaml.safe_load("packs/{}.yaml".format(packname))

def apply_features(df, fns):
    for f in fns:
        df[f] = fns[f](df)
    return df
