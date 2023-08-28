select qh.query_text,
   trim(ifnull(src.value:objectName::string, '')
      || '.' || ifnull(src.value:columnName::string, ''), '.') as source,
   trim(ifnull(om.value:objectName::string, '')
      || '.' || ifnull(col.value:columnName::string, ''), '.') as target,
   obj.value:objectName::string as sourceAccessed,
   ah.objects_modified, ah.direct_objects_accessed, ah.base_objects_accessed
   from snowflake.account_usage.access_history ah
      left join snowflake.account_usage.query_history qh
      on ah.query_id = qh.query_id,
   lateral flatten(input => objects_modified) om,
      lateral flatten(input => om.value: "columns", outer => true) col,
      lateral flatten(input => col.value:directSources, outer => true) src,
   lateral flatten(input => direct_objects_accessed, outer => true) obj
where ifnull(src.value:objectName::string, '') like '{{database}}%'
   or ifnull(om.value:objectName::string, '') like '{{database}}%'
   or ifnull(obj.value:objectName::string, '') like '{{database}}%'
order by ah.query_start_time;