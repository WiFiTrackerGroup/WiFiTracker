snr = parse.search('INTEGER: {}', line)[0]
rssi = parse.search('INTEGER: {}', line)[0]
ap_mac = parse.search('Hex-STRING: {}', line)[0]
ap_web = parse.search('Hex-STRING: {}', line)[0]
ap_name = parse.search('STRING: "{}"', line)[0]
bytes_rx = parse.search('Counter64: {}', line)[0]
bytes_tx = parse.search('Counter64: {}', line)[0]


pd.merge(self.df_username, self.df_snr, on='mac')