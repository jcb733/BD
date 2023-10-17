select o.ordem_id
   , c.cliente_id 
   , c.nome
   , t.tecnico_id 
   , o.data_abertura
   , o.data_conclusao
   , o.status_os
   , o.solucao
   , o.custo_total
  from LABDATABASE.ordem_servico o
  inner join LABDATABASE.clientes2 c
  on c.CLIENTE_ID = o.CLIENTE_ID
  inner join LABDATABASE.tecnico t
  on t.TECNICO_ID = o.TECNICO_ID
  order by o.ordem_id