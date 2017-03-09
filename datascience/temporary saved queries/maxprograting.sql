select connection_id,skill,max(convert(rating,signed integer))as convertedRate from linkedin.skill where skill='programming';
