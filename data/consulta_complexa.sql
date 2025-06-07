-- Quantidade de sensores por estação
select e.id_estacao_tratamento,
       count(s.id_sensor) as qtd_sensores
  from t_fv_estacao_tratamento e
  join t_fv_sensor s
on e.id_estacao_tratamento = s.id_estacao_tratamento
 group by e.id_estacao_tratamento
 order by qtd_sensores desc;

-- Total investido por fornecedor
select f.ds_cnpj,
       sum(m.nr_quant_estoque * m.nr_preco_unidade) as total_estoque
  from t_fv_fornecedor f
  join t_fv_material m
on f.ds_cnpj = m.ds_cnpj
 group by f.ds_cnpj
 order by total_estoque desc;

-- Quantidade de materiais por tipo
select tp_material,
       count(*) as qtd_material
  from t_fv_material
 group by tp_material
having count(*) >= 1
 order by qtd_material desc;

-- Estações com status e quantidade de sensores instalados
select e.id_estacao_tratamento,
       e.st_estacao,
       count(s.id_sensor) as qtd_sensores
  from t_fv_estacao_tratamento e
  left join t_fv_sensor s
on e.id_estacao_tratamento = s.id_estacao_tratamento
 group by e.id_estacao_tratamento,
          e.st_estacao
 order by qtd_sensores desc;

-- Responsáveis que não têm estação associada
select r.nm_responsavel
  from t_fv_responsavel r
 where not exists (
   select 1
     from t_fv_estacao_tratamento e
    where e.ds_cpf = r.ds_cpf
);