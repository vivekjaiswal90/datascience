select
(
select count(*) from linkedin.main where designation like '%ceo%'
)as ceo
,
(
select count(*) from linkedin.main where designation like '%professor%'
)as prof
,
(
select count(*) from linkedin.main where designation like '%dean%'
)as dean

