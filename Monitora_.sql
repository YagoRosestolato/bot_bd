USE [DBST_Brasil]
GO
CREATE TABLE [DBST_Brasil].[VFBR].[Monitora_]
(
    [Ano_Mes_Dia] VARCHAR(255) NULL,
    [Sub_Linha] VARCHAR(255) NULL,
    [Area] VARCHAR(255) NULL,
    [Equipamento] VARCHAR(255) NULL,
    [DWH] VARCHAR(255) NULL,
    [Fato] VARCHAR(255) NULL,
    [VF] VARCHAR(255) NULL,
    [Rep_VF] VARCHAR(255) NULL,
    [Desvio_VF_x_SGL] VARCHAR(255) NULL,
    [Status] VARCHAR(255) NULL,
    [.] VARCHAR(255) NULL,
    -- SEMPRE INSERIR ESSAS DUAS COLUNAS DE CONTROLE ABAIXO--
    [IDX_Process] INT NULL,
    [IDX_Track] INT NULL
)

-- Inserindo ETL_Interfaces
INSERT INTO [dbo].[ETL_Interfaces]
       ([SRC_Table]
       ,[File_Interface]
       ,[Interface]
       ,[ETL_SubModulo]
       ,[Separador]
       ,[PrimerRegistro])
 VALUES
       ('VFBR.SRC_Monitora_'
       ,'SRC_Monitora_@'
       ,'VF - Monitora'
       ,'VF Brasil'
       ,'|'
       ,2)
