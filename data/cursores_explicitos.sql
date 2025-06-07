-- Última leitura por tipo de sensor
DECLARE
    CURSOR c_tipos IS
        SELECT DISTINCT TP_SENSOR FROM T_FV_SENSOR;

    v_tipo_sensor T_FV_SENSOR.TP_SENSOR%TYPE;
    v_id_sensor   T_FV_SENSOR.ID_SENSOR%TYPE;
    v_valor       T_FV_REGISTRO_MEDIDA.NR_RESULTADO%TYPE;
    v_data        T_FV_REGISTRO_MEDIDA.DT_REGISTRO%TYPE;
BEGIN
    OPEN c_tipos;
    LOOP
        FETCH c_tipos INTO v_tipo_sensor;
        EXIT WHEN c_tipos%NOTFOUND;

        SELECT r.ID_SENSOR, r.NR_RESULTADO, r.DT_REGISTRO
        INTO v_id_sensor, v_valor, v_data
        FROM T_FV_REGISTRO_MEDIDA r
        JOIN T_FV_SENSOR s ON s.ID_SENSOR = r.ID_SENSOR
        WHERE s.TP_SENSOR = v_tipo_sensor
        AND r.DT_REGISTRO = (
            SELECT MAX(DT_REGISTRO)
            FROM T_FV_REGISTRO_MEDIDA r2
            JOIN T_FV_SENSOR s2 ON s2.ID_SENSOR = r2.ID_SENSOR
            WHERE s2.TP_SENSOR = v_tipo_sensor
        )
        FETCH FIRST 1 ROWS ONLY;

        DBMS_OUTPUT.PUT_LINE(
            'Sensor: ' || v_tipo_sensor || 
            ' | Última leitura: ' || v_valor || 
            ' em ' || TO_CHAR(v_data, 'YYYY-MM-DD') || 
            ' (ID Sensor: ' || v_id_sensor || ')'
        );
    END LOOP;
    CLOSE c_tipos;
END;
/

-- Estoque médio por tipo de material
DECLARE
    CURSOR c_materiais IS
        SELECT TP_MATERIAL, ROUND(AVG(NR_QUANT_ESTOQUE)) AS MEDIA_ESTOQUE
        FROM T_FV_MATERIAL
        GROUP BY TP_MATERIAL;

    v_tipo     T_FV_MATERIAL.TP_MATERIAL%TYPE;
    v_media    NUMBER;
BEGIN
    OPEN c_materiais;
    LOOP
        FETCH c_materiais INTO v_tipo, v_media;
        EXIT WHEN c_materiais%NOTFOUND;

        IF v_media < 20 THEN
            DBMS_OUTPUT.PUT_LINE('Tipo: ' || v_tipo || ' | MÉDIA BAIXA: ' || ROUND(v_media, 2));
        ELSE
            DBMS_OUTPUT.PUT_LINE('Tipo: ' || v_tipo || ' | Média ok: ' || ROUND(v_media, 2));
        END IF;
    END LOOP;
    CLOSE c_materiais;
END;
/
