select qh.query_text,
   ah.objects_modified, ah.object_modified_by_ddl,
   ah.direct_objects_accessed, ah.base_objects_accessed
   from snowflake.account_usage.access_history ah
      left join snowflake.account_usage.query_history qh
      on ah.query_id = qh.query_id
where ah.objects_modified::string like '%{{database}}%'
   or ah.object_modified_by_ddl::string like '%{{database}}%'
   or ah.direct_objects_accessed::string like '%{{database}}%'
   or ah.base_objects_accessed::string like '%{{database}}%'
order by ah.query_start_time;
