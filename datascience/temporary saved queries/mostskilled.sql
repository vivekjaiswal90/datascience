create view mostskill as
select connection_id,skill,id,max(convert(rating,signed integer)) from linkedin.skill;
