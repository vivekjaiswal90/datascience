create view skillgroups as
select groups.connection_id, groups.groups, skill.skill, skill.rating from skill inner join groups on skill.connection_id=groups.connection_id;