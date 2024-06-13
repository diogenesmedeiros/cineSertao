def formata_data(data):
    data_lancamento_ = data
    data_lancamento_ = data_lancamento_.split("-")

    date_lancamento_formatada = f"{data_lancamento_[2]}/{data_lancamento_[1]}/{data_lancamento_[0]}"

    return date_lancamento_formatada