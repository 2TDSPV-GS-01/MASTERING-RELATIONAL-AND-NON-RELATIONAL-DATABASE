-- monitoramento de pH por responsável
DECLARE
    CURSOR c_ph IS
        SELECT 
            r.NR_RESULTADO AS VALOR_PH,
            rs.NM_RESPONSAVEL,
            r.DT_REGISTRO
        FROM T_FV_REGISTRO_MEDIDA r
        JOIN T_FV_SENSOR s ON s.ID_SENSOR = r.ID_SENSOR
        JOIN T_FV_ESTACAO_TRATAMENTO e ON e.ID_ESTACAO_TRATAMENTO = s.ID_ESTACAO_TRATAMENTO
        JOIN T_FV_RESPONSAVEL rs ON rs.DS_CPF = e.DS_CPF
        WHERE s.TP_SENSOR = 'PH'
        ORDER BY r.DT_REGISTRO;

    v_valor NUMBER;
    v_nome  T_FV_RESPONSAVEL.NM_RESPONSAVEL%TYPE;
    v_data  DATE;
    v_classificacao VARCHAR2(10);
BEGIN
    OPEN c_ph;
    LOOP
        FETCH c_ph INTO v_valor, v_nome, v_data;
        EXIT WHEN c_ph%NOTFOUND;

        IF v_valor > 7.5 THEN
            v_classificacao := 'BASICO';
        ELSIF v_valor < 6.5 THEN
            v_classificacao := 'ACIDO';
        ELSE
            v_classificacao := 'NEUTRO';
        END IF;

        DBMS_OUTPUT.PUT_LINE(TO_CHAR(v_data, 'YYYY-MM-DD') || ' Responsável: ' || v_nome || ' | pH: ' || v_valor || ' - ' || v_classificacao);
    END LOOP;
    CLOSE c_ph;
END;
/


-- Monitoramento geral de sensores por estação
DECLARE
    CURSOR c_estacoes IS
        SELECT e.ID_ESTACAO_TRATAMENTO, COUNT(s.ID_SENSOR) AS QTD_SENSORES
        FROM T_FV_ESTACAO_TRATAMENTO e
        LEFT JOIN T_FV_SENSOR s ON s.ID_ESTACAO_TRATAMENTO = e.ID_ESTACAO_TRATAMENTO
        WHERE e.ST_ESTACAO = 'A'
        GROUP BY e.ID_ESTACAO_TRATAMENTO;

    v_id_estacao T_FV_ESTACAO_TRATAMENTO.ID_ESTACAO_TRATAMENTO%TYPE;
    v_qtd_sensores NUMBER;
    v_status VARCHAR2(15);
BEGIN
    OPEN c_estacoes;
    LOOP
        FETCH c_estacoes INTO v_id_estacao, v_qtd_sensores;
        EXIT WHEN c_estacoes%NOTFOUND;

        IF v_qtd_sensores = 5 THEN
            v_status := 'COMPLETA';
        ELSIF v_qtd_sensores > 5 THEN
            v_status := 'EXCESSO';
        ELSE
            v_status := 'INCOMPLETA';
        END IF;

        DBMS_OUTPUT.PUT_LINE(
            'Estação: ' || v_id_estacao ||
            ' | Sensores: ' || v_qtd_sensores ||
            ' | Status: ' || v_status
        );
    END LOOP;
    CLOSE c_estacoes;
END;
/
