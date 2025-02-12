/* DROP TABLE clb157295.imp_blindagem_clientes;
CREATE COLUMN TABLE clb157295.imp_blindagem_clientes (
	REF	NVARCHAR(6),
	INSTALACAO NVARCHAR(10),
	FATURAMENTO NVARCHAR(30),
	MEDIDOR NVARCHAR(18),
	LEITURA_FAT_KWH NVARCHAR(10),
	NOTA_LEIT NVARCHAR(10),
	MRU NVARCHAR(8),
	LOTE NVARCHAR(2),
	DT_LEIT NVARCHAR(10),
	SETOR NVARCHAR(50),
	UTD NVARCHAR(50),
	CAD_HEMERA NVARCHAR(3),
	NET NVARCHAR(10),
	CS NVARCHAR(10),
	NET_CS NVARCHAR(10),
	NET_CS_POSICAO NVARCHAR(20),
	DT_ULT_LEITURA NVARCHAR(10),
	DIAS_SEM_LEITURA NVARCHAR(5),
	ULT_LEITURA_KWH NVARCHAR(10),
	AGRUPAMENTO NVARCHAR(50),
	LOCALIDADE NVARCHAR(50),
	DT_BAIXA NVARCHAR(10),
	STATUS NVARCHAR(30)
); */

DROP TABLE clb157295.crre_blindagem_clientes;
CREATE COLUMN TABLE clb157295.crre_blindagem_clientes AS (
	 SELECT REF AS referencia,
		    LPAD(INSTALACAO, 10, '0') AS instalacao,
		    FATURAMENTO AS status_faturamento,
		    LPAD(MEDIDOR, 18, '0') AS numero_serie,
		    CAST(REPLACE(LEITURA_FAT_KWH, '.', '') AS BIGINT) AS leitura_faturamento,
		    NOTA_LEIT AS ocorrencia_leitura,
		    MRU AS mru,
		    LOTE AS lote,
		    CAST( RIGHT(DT_LEIT, 4) || '-' || SUBSTRING(DT_LEIT, 4, 2) || '-' || LEFT(DT_LEIT, 2) AS DATE) AS data_faturamento,
			SETOR AS setor,
			UTD AS utd,
			CAD_HEMERA AS flag_hemera,
			TRIM(NET) AS net,
			TRIM(CS) AS cs,
			TRIM(NET_CS) AS net_cs,
			TRIM(NET_CS_POSICAO) AS net_cs_posicao,
			CAST( CASE WHEN TRIM(DT_ULT_LEITURA) = '' THEN NULL ELSE RIGHT(DT_ULT_LEITURA, 4) || '-' || SUBSTRING(DT_ULT_LEITURA, 4, 2) || '-' || LEFT(DT_ULT_LEITURA, 2) END AS DATE) AS data_leitura_hemera,
			CAST( CASE WHEN TRIM(DIAS_SEM_LEITURA) = '' THEN NULL ELSE REPLACE(DIAS_SEM_LEITURA, '.', '') END AS INTEGER) AS dias_sem_leitura,
			CAST( CASE WHEN TRIM(ULT_LEITURA_KWH) = '' THEN NULL ELSE REPLACE(ULT_LEITURA_KWH, '.', '') END AS BIGINT) AS ultima_leitura,
			AGRUPAMENTO AS agrupamento_rede,
			LOCALIDADE AS localidade,
			CAST( RIGHT(DT_BAIXA, 4) || '-' || SUBSTRING(DT_BAIXA, 4, 2) || '-' || LEFT(DT_BAIXA, 2) AS DATE) AS data_baixa,
			STATUS AS status
	  FROM clb157295.imp_blindagem_clientes
);

DROP TABLE clb157295.crre_blindagem_kpis;
CREATE COLUMN TABLE clb157295.crre_blindagem_kpis AS(
		SELECT cic.setor AS setor_atendimento,
			   cic.utd AS utd_atendimento,
			   cic.localidade,
			   cic.instalacao,
			   SUBSTRING(cic.agrupamento_rede, 10, 2) AS topologia_rede,
			   pc.zcgaccoun,
			   pc.regional,
			   pc.municipio,
			   pc.zcgbairr
		  FROM (SELECT DISTINCT setor,
					   utd,
					   localidade,
					   instalacao,
					   status,
					   agrupamento_rede
				  FROM clb157295.crre_blindagem_clientes
				 WHERE status = 'ATIVO') cic
	 LEFT JOIN clb961851.planilhao_cliente pc ON pc.zcginstal = cic.instalacao );

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_jan23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_jan23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202301'), 0);
	 
ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_fev23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_fev23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202302'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_mar23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_mar23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202303'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_abr23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_abr23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202304'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_mai23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_mai23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202305'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_jun23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_jun23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202306'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_jul23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_jul23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202307'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_ago23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_ago23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202308'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_set23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_set23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202309'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_out23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_out23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202310'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_nov23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_nov23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202311'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (arr_dez23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET arr_dez23 = COALESCE((SELECT SUM(arr.zcgamountdia) 
																 FROM clb_ccs_icc.zct_ds_fco002 arr
																WHERE arr.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
																  AND arr.zcgmtcomp = '01'
																  AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = arr.zcgdocref )
																  AND TO_CHAR(arr.zcgdtcomp, 'YYYYMM') = '202312'), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_jan23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_jan23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202301' ), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_fev23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_fev23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202302' ), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_mar23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_mar23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202303' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_abr23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_abr23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202304' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_mai23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_mai23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202305' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_jun23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_jun23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202306' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_jul23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_jul23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202307' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_ago23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_ago23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202308' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_set23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_set23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202309' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_out23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_out23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202310' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_nov23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_nov23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202311' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (fat_dez23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET fat_dez23 = COALESCE( (SELECT SUM(fpos.zcgamount) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtvenc, 'YYYYMM') = '202312' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_jan23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_jan23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202301' ), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_fev23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_fev23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202302' ), 0);

ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_mar23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_mar23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202303' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_abr23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_abr23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202304' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_mai23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_mai23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202305' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_jun23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_jun23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202306' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_jul23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_jul23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202307' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_ago23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_ago23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202308' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_set23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_set23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202309' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_out23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_out23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202310' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_nov23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_nov23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202311' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (kwh_dez23 DECIMAL(20,8));
UPDATE clb157295.crre_blindagem_kpis SET kwh_dez23 = COALESCE( (SELECT SUM(fpos.zcgfatura) FROM clb_ccs_icc.zct_ds_fat001 fpos
														   	 WHERE fpos.zcgaccoun = clb157295.crre_blindagem_kpis.zcgaccoun
														   	   AND NOT EXISTS ( SELECT 1 FROM "NEO_PEC"."neo.pec.data::MODEL.TABLES.ZCT_DS_FAT_IRREGULARIDADE" irr WHERE irr.zcgdocref = fpos.zcgdocref )
														   	   AND TO_CHAR(fpos.zcgdtdoct, 'YYYYMM') = '202312' ), 0);
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_jan23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_jan23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202301'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
														   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_jan23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_jan23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202301'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_fev23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_fev23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202302'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_mar23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_mar23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202303'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_abr23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_abr23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202304'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_mai23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_mai23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202305'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_jun23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_jun23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202306'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_jul23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_jul23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202307'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_ago23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_ago23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202308'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_set23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_set23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202309'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_out23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_out23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202310'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_nov23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_nov23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202311'
													      AND RIGHT(lei.zcgnotal, 1) = '0');
															   	   
ALTER TABLE clb157295.crre_blindagem_kpis ADD (ocle_dez23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET ocle_dez23 = (SELECT MAX(lei.zcgnotal)
														 FROM clb355750.leitura_clb lei
													    WHERE lei.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(lei.zcgdtleit, 'YYYYMM') = '202312'
													      AND RIGHT(lei.zcgnotal, 1) = '0');

ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_jan23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_jan23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202301'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_fev23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_fev23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202302'
													      AND cs.zcgtpnota = 'CS');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_mar23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_mar23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202303'
													      AND cs.zcgtpnota = 'CS');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_abr23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_abr23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202304'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_mai23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_mai23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202305'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_jun23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_jun23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202306'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_jul23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_jul23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202307'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_ago23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_ago23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202308'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_set23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_set23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202309'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_out23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_out23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202310'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_nov23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_nov23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202311'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cs_dez23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cs_dez23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202312'
													      AND cs.zcgtpnota = 'CS'
													      AND zcgusrsts = 'VREL');

ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_jan23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_jan23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202301'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_fev23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_fev23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202302'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_mar23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_mar23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202303'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_abr23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_abr23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202304'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_mai23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_mai23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202305'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_jun23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_jun23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202306'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_jul23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_jul23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202307'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_ago23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_ago23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202308'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_set23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_set23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202309'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_out23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_out23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202310'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_nov23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_nov23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202311'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');
	
ALTER TABLE clb157295.crre_blindagem_kpis ADD (cr_dez23 NVARCHAR(4));
UPDATE clb157295.crre_blindagem_kpis SET cr_dez23 = (SELECT COUNT(DISTINCT cs.zcgqmnum)
														 FROM clb_ccs_icc.zct_ds_tab004 cs
													    WHERE cs.zcginstal = clb157295.crre_blindagem_kpis.instalacao
													      AND TO_CHAR(cs.zcgdtence, 'YYYYMM') = '202312'
													      AND cs.zcgtpnota = 'CR'
													      AND zcgusrsts = 'VREL');														   	   
SELECT * FROM crre_blindagem_kpis WHERE arr_jan23 >0 LIMIT 10000