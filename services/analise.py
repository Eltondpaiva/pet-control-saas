import pandas as pd
from datetime import datetime

def processar_dados(df):

    df.columns = df.columns.str.replace('"', '').str.strip()

    df = df.rename(columns={
        'Data e hora': 'Data',
        'Produto/serviço': 'Servico',
        'Animal': 'Pet'
    })

    banhos = df[df['Servico'].str.contains('banho', case=False, na=False)]
    banhos['Data'] = pd.to_datetime(banhos['Data'], dayfirst=True, errors='coerce')

    resultados = []

    for (cliente, pet), grupo in banhos.groupby(['Cliente', 'Pet']):
        datas = grupo['Data'].dropna().sort_values()

        if len(datas) == 0:
            continue

        ultima = datas.iloc[-1]
        dias_sem = (datetime.now() - ultima).days

        if len(datas) > 1:
            freq = int(datas.diff().dt.days.dropna().mean())
        else:
            freq = None

        if dias_sem > 14:
            status = "Sumido"
        elif freq and dias_sem > freq:
            status = "Fora do padrão"
        else:
            status = "OK"

        resultados.append({
            "Cliente": cliente,
            "Pet": pet,
            "Última visita": ultima.date(),
            "Dias sem vir": dias_sem,
            "Frequência média": freq,
            "Status": status
        })

    return pd.DataFrame(resultados)
