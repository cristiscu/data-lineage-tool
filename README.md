Data Lineage Viewer for Snowflake
=================================

Queries the ACCESS_HISTORY and QUERY_HISTORY views, from the SNOWFLAKE.ACCOUNT_USAGE schema, and generates two interactive GraphViz visual diagrams online, in a visual editor:

* one for [**column lineage**](http://magjac.com/graphviz-visual-editor/?dot=digraph%20structs%20%7B%0A%09rankdir%3DLR%3B%0A%09_START_%20%5Blabel%3D%22%22%5D%0A%09T1%20%5Bshape%3DMrecord%20label%3D%22%3CT1%3E%20T1%7C%3CCONTENT%3E%20CONTENT%22%5D%3B%0A%09T6%20%5Bshape%3DMrecord%20label%3D%22%3CT6%3E%20T6%7C%3CCONTENT%3E%20CONTENT%22%5D%3B%0A%09T2%20%5Bshape%3DMrecord%20label%3D%22%3CT2%3E%20T2%7C%3CID%3E%20ID%7C%3CNAME%3E%20NAME%22%5D%3B%0A%09S1%20%5Bshape%3DMrecord%20label%3D%22%3CS1%3E%20S1%22%5D%3B%0A%09T3%20%5Bshape%3DMrecord%20label%3D%22%3CT3%3E%20T3%7C%3CCUSTOMER_INFO%3E%20CUSTOMER_INFO%22%5D%3B%0A%09T4%20%5Bshape%3DMrecord%20label%3D%22%3CT4%3E%20T4%7C%3CID%3E%20ID%7C%3CNAME%3E%20NAME%22%5D%3B%0A%09T7%20%5Bshape%3DMrecord%20label%3D%22%3CT7%3E%20T7%7C%3CCONTENT%3E%20CONTENT%22%5D%3B%0A%09_START_%20-%3E%20T1%3ACONTENT%20%5Btooltip%3D%22insert%20into%20T1%28content%29%20select%20parse_json%28%27%7B%27name%27%3A%20%27A%27%2C%20%27id%27%3A1%7D%27%29%3B%22%5D%3B%0A%09_START_%20-%3E%20S1%20%5Btooltip%3D%22copy%20into%20%40S1%20from%20T1%3B%22%5D%3B%0A%09_START_%20-%3E%20T3%3ACUSTOMER_INFO%20%5Btooltip%3D%22copy%20into%20T3%20from%20%40S1%3B%22%5D%3B%0A%09T1%3ACONTENT%20-%3E%20T6%3ACONTENT%20%5Btooltip%3D%22insert%20into%20T6%20select%20%2A%20from%20T1%3B%22%5D%3B%0A%09T1%3ACONTENT%20-%3E%20T2%3AID%20%5Btooltip%3D%22create%20table%20T2%20as%20select%20content%3A%27name%27%20as%20name%2C%20content%3A%27id%27%20as%20id%20from%20T1%3B%22%5D%3B%0A%09T1%3ACONTENT%20-%3E%20T2%3ANAME%20%5Btooltip%3D%22create%20table%20T2%20as%20select%20content%3A%27name%27%20as%20name%2C%20content%3A%27id%27%20as%20id%20from%20T1%3B%22%5D%3B%0A%09T1%3ACONTENT%20-%3E%20T4%3AID%20%5Btooltip%3D%22insert%20into%20T4%28name%2C%20id%29%20select%20content%3A%27name%27%2C%20content%3A%27id%27%20from%20T1%3B%22%5D%3B%0A%09T1%3ACONTENT%20-%3E%20T4%3ANAME%20%5Btooltip%3D%22insert%20into%20T4%28name%2C%20id%29%20select%20content%3A%27name%27%2C%20content%3A%27id%27%20from%20T1%3B%22%5D%3B%0A%09T6%3ACONTENT%20-%3E%20T7%3ACONTENT%20%5Btooltip%3D%22create%20table%20T7%20as%20select%20%2A%20from%20T6%3B%22%5D%3B%0A%7D)
* the other for [**table lineage**](http://magjac.com/graphviz-visual-editor/?dot=digraph%20structs%20%7B%0A%09rankdir%3DLR%3B%0A%09_START_%20%5Blabel%3D%22%22%5D%0A%09T1%20%5Bshape%3DMrecord%20label%3D%22T1%22%5D%3B%0A%09T6%20%5Bshape%3DMrecord%20label%3D%22T6%22%5D%3B%0A%09T2%20%5Bshape%3DMrecord%20label%3D%22T2%22%5D%3B%0A%09S1%20%5Bshape%3DMrecord%20label%3D%22S1%22%5D%3B%0A%09T3%20%5Bshape%3DMrecord%20label%3D%22T3%22%5D%3B%0A%09T4%20%5Bshape%3DMrecord%20label%3D%22T4%22%5D%3B%0A%09T7%20%5Bshape%3DMrecord%20label%3D%22T7%22%5D%3B%0A%09_START_%20-%3E%20T1%20%5Btooltip%3D%22%22%5D%3B%0A%09_START_%20-%3E%20S1%20%5Btooltip%3D%22copy%20into%20%40S1%20from%20T1%3B%22%5D%3B%0A%09_START_%20-%3E%20T3%20%5Btooltip%3D%22%22%5D%3B%0A%09T1%20-%3E%20T6%20%5Btooltip%3D%22%22%5D%3B%0A%09T1%20-%3E%20T2%20%5Btooltip%3D%22%22%5D%3B%0A%09T1%20-%3E%20T4%20%5Btooltip%3D%22%22%5D%3B%0A%09T6%20-%3E%20T7%20%5Btooltip%3D%22%22%5D%3B%0A%7D)

The generated DOT Graphviz models are also saved in the output/ folder.

# Database Profile File

To connect to Snowflake, create a **profiles_db.conf** copy of the **profiles_db_template.conf** file, and customize it with your own Snowflake connection parameters, the user name and the account. Your top [default] profile is the active profile, considered by our tool.

Save your password in a SNOWFLAKE_PASSWORD local environment variable. Never add the password or any other sensitive information to your code or to profile files. All names must be case sensitive, with no quotes.

# CLI Executable File

Without an executable, you can use the source file directly:

**<code>python data-lineage.py TEST_DB</code>**  

To compile into a CLI executable:

**<code>pip install pyinstaller</code>**  
**<code>pyinstaller --onefile data-lineage.py</code>**  
**<code>dist/data-lineage TEST_DB</code>**  

# The Query Result for the Lineage Graph

To repro, you may run the **sql/create-script.sql** file in Snowflake, which is similar to the one described [in the documentation samples](https://docs.snowflake.com/en/user-guide/access-history#example-column-lineage). Wait a few hours, until the changes are propagated in the ACCOUNT_USAGE views.

Then run the **sql/query-access-history.sql** query to get lineage info about the created test tables. {{database}} must be replaced by TEST_DB for our use case here:

![Table Lineage](/images/query-column-lineage.png)

# The Column Lineage Graph

This diagram shows how data moved between the table columns in the TEST_DB database. You may go over the links and the SQL query that made that transformation appears as tooltip.

![Table Lineage](/images/column-lineage.png)

# The Table Lineage Graph

The table lineage graph is a simplified derived diagram, in which there are no columns, and all column dependencies appear as one single link at the container table level:

![Table Lineage](/images/table-lineage.png)
