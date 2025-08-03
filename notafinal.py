import pandas as pd
import sys

# URL do jogador
url = "https://fbref.com/en/players/34e12499/Nico-Schlotterbeck"

try:
    tables = pd.read_html(url)
except Exception as e:
    sys.exit(f"Erro ao aceder à URL: {e}")

# --- Encontra a tabela correta ---
scouting_report_df = None
for table in tables:
    if 'Statistic' in table.columns and 'Percentile' in table.columns:
        scouting_report_df = table
        break

if scouting_report_df is not None:
    # --- Calcula e armazena os dados internamente ---
    
    metricas_a_usar = [
        'Tackles',
        'Interceptions',
        'Aerials Won',
        'Progressive Passes',
        'Pass Completion %'
    ]
    
    if isinstance(scouting_report_df.columns, pd.MultiIndex):
        scouting_report_df.columns = scouting_report_df.columns.droplevel(0)

    stats_percentis = dict(zip(scouting_report_df['Statistic'], scouting_report_df['Percentile']))

    stats_escaladas_10 = {}
    for metrica in metricas_a_usar:
        if metrica in stats_percentis:
            percentil = pd.to_numeric(stats_percentis[metrica], errors='coerce')
            stats_escaladas_10[metrica] = (percentil / 99.0) * 10 if not pd.isna(percentil) else 0
        else:
            stats_escaladas_10[metrica] = 0
    
    # Percentagens definidas
    pesos_ajustados = {
        'Tackles': 25,
        'Interceptions': 25,
        'Pass Completion %': 20,
        'Progressive Passes': 20,
        'Aerials Won': 10
    }
    
    nota_final = 0
    soma_pesos = sum(pesos_ajustados.values())

    for metrica, nota_10 in stats_escaladas_10.items():
        if metrica in pesos_ajustados:
            nota_final += nota_10 * (pesos_ajustados[metrica] / 100.0)
            
    # --- Imprime o resultado final formatado ---
    
    print("--- Notas Individuais (0-10) ---")
    for metrica, nota in stats_escaladas_10.items():
        print(f"{metrica}: {nota:.2f}")
    
    print("\n--- Nota Final Ponderada ---")
    print(f"{nota_final:.2f}")

else:
    sys.exit("Erro: Não foi possível encontrar a tabela 'Scouting Report'.")