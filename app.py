import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def gerar_sql_create_table(caminho_txt):
    def ler_arquivo_com_encoding(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.readlines()
        except UnicodeDecodeError:
            with open(caminho, 'r', encoding='latin1') as f:
                return f.readlines()

    linhas = ler_arquivo_com_encoding(caminho_txt)
    nome_arquivo = os.path.splitext(os.path.basename(caminho_txt))[0]
    colunas_txt = linhas[0].strip().split('|')
    colunas = [col.strip().replace('-', '_').replace(' ', '_').replace('__', '_') for col in colunas_txt if col.strip()]
    return montar_sql(nome_arquivo, colunas)

def gerar_sql_manual():
    nome_tabela = simpledialog.askstring("Nome da Tabela", "Digite o nome da tabela:")
    if not nome_tabela:
        messagebox.showwarning("Aviso", "Nome da tabela não informado.")
        return

    colunas_raw = simpledialog.askstring(
        "Colunas (separadas por |)",
        "Digite os nomes das colunas separados por '|':\nEx: Ano_Mes_Dia|Sub-Linha|Area|..."
    )
    if not colunas_raw:
        messagebox.showwarning("Aviso", "Colunas não informadas.")
        return

    colunas_txt = colunas_raw.strip().split('|')
    colunas = [col.strip().replace('-', '_').replace(' ', '_').replace('__', '_') for col in colunas_txt if col.strip()]
    sql = montar_sql(nome_tabela, colunas)
    salvar_sql_em_arquivos(sql, nome_tabela)

def montar_sql(nome_arquivo, colunas):
    sql_create = f"USE [DBST_Brasil]\nGO\nCREATE TABLE [DBST_Brasil].[VFBR].[{nome_arquivo}]\n(\n"
    for col in colunas:
        sql_create += f"    [{col}] VARCHAR(255) NULL,\n"
    sql_create += "    -- SEMPRE INSERIR ESSAS DUAS COLUNAS DE CONTROLE ABAIXO--\n"
    sql_create += "    [IDX_Process] INT NULL,\n"
    sql_create += "    [IDX_Track] INT NULL\n"
    sql_create += ")\n"

    nome_tabela = f"VFBR.SRC_{nome_arquivo}"
    nome_interface = f"SRC_{nome_arquivo}@"

    sql_insert = f"""-- Inserindo ETL_Interfaces
INSERT INTO [dbo].[ETL_Interfaces]
       ([SRC_Table]
       ,[File_Interface]
       ,[Interface]
       ,[ETL_SubModulo]
       ,[Separador]
       ,[PrimerRegistro])
 VALUES
       ('{nome_tabela}'
       ,'{nome_interface}'
       ,'VF - Monitora'
       ,'VF Brasil'
       ,'|'
       ,2)
"""
    return sql_create + "\n" + sql_insert

def salvar_sql_em_arquivos(sql, nome_arquivo):
    pasta_sql = filedialog.askdirectory(title="Escolha onde salvar o arquivo .sql")
    if not pasta_sql:
        messagebox.showwarning("Aviso", "Pasta do SQL não selecionada. Operação cancelada.")
        return

    pasta_txt = filedialog.askdirectory(title="Escolha onde salvar o arquivo .txt")
    if not pasta_txt:
        messagebox.showwarning("Aviso", "Pasta do TXT não selecionada. Operação cancelada.")
        return

    caminho_sql = os.path.join(pasta_sql, f"{nome_arquivo}.sql")
    caminho_txt = os.path.join(pasta_txt, f"{nome_arquivo}.txt")

    try:
        with open(caminho_sql, 'w', encoding='utf-8') as f_sql:
            f_sql.write(sql)

        with open(caminho_txt, 'w', encoding='utf-8') as f_txt:
            f_txt.write(sql)

        messagebox.showinfo(
            "Arquivos Salvos",
            f"SQL salvo em:\n{caminho_sql}\n\nTXT salvo em:\n{caminho_txt}"
        )
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar os arquivos:\n{e}")

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo .txt",
        filetypes=[("Arquivos de texto", "*.txt")]
    )
    if caminho:
        nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
        sql = gerar_sql_create_table(caminho)
        salvar_sql_em_arquivos(sql, nome_arquivo)

def menu():
    root = tk.Tk()
    root.withdraw()

    escolha = messagebox.askquestion(
        "Modo de uso",
        "Deseja carregar um arquivo .txt?\n\nClique em 'Sim' para selecionar arquivo\nClique em 'Não' para digitar manualmente"
    )

    if escolha == 'yes':
        selecionar_arquivo()
    else:
        gerar_sql_manual()

if __name__ == "__main__":
    menu()
