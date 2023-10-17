SELECT os.ordem_id AS ordem_id,
       pu.peca_utilizada_id AS codigo_peca_utilizada,
       pu.peca_id AS peca_id,
       pu.quant_utilizada AS quantidade,
       pu.preco_uni AS valor_unitario,
       (pu.quant_utilizada * pu.preco_uni) AS valor_total
FROM pecas_utilizadas pu
INNER JOIN ordem_servico os ON pu.ordem_id = os.ordem_id
INNER JOIN peca p ON pu.peca_id = p.peca_id
ORDER BY os.ordem_id