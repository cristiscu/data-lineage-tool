"""
Created By:    Cristian Scutaru
Creation Date: Aug 2023
Company:       XtractPro Software
"""

import os, webbrowser, configparser, argparse, urllib.parse
import snowflake.connector

def addTable(tables, isSource, name, alt=None):

    # source object is sometimes empty, but given by source Accessed
    if alt is not None and name is None: name = alt
    if name is None or len(name) == 0:
        name = "_START_" if isSource else "_END_"

    # skip database and schema name prefix
    parts = name.split('.')
    if (len(parts)) == 3: name = parts[2]
    elif (len(parts)) == 4: name = parts[2] + '.' + parts[3]

    # add table if not there
    parts = name.split('.')
    tableName = parts[0]
    if tableName not in tables: tables[tableName] = Table(tableName)
    table = tables[tableName]

    # add table column if not there
    columnName = parts[1] if len(parts) > 1 else None
    if columnName is not None and columnName not in table.columns:
        table.columns[columnName] = Column(columnName, tableName)
    return name

def addLink(tables, sourceName, targetName, tooltip):

    # create link between columns or tables
    link = Link(sourceName, targetName, tooltip)
    key = link.getLinkKey()

    # add link to source table or column
    parts = sourceName.split('.')
    sourceTableName = parts[0]
    table = tables[sourceTableName]
    if len(parts) == 1: table.links[key] = link
    else: table.columns[parts[1]].links[key] = link

    # add redundant link between tables only
    targetTableName = targetName.split('.')[0]
    key = f'{sourceTableName} -> {targetTableName}'
    if key not in table.links:
        link = Link(sourceTableName, targetTableName)
        table.links[key] = link
    return None

class Table:
    def __init__(self, name):
        self.columns = {}
        self.links = {}
        self.name = name

    def getNodeSignature(self, skipColumns=False):
        if self.name == "_START_" or self.name == "_END_":
            return f'\n\t{self.name} [label=""]'
        else:
            return f'\n\t{self.name} [shape=Mrecord label="{self.getColumnNames(skipColumns)}"];'

    def getColumnNames(self, skipColumns=False):
        if skipColumns: return self.name
        s = f"<{self.name}> {self.name}"
        for columnName in self.columns:
            s += f"|<{columnName}> {columnName}"
        return s

class Column:
    def __init__(self, name, tableName):
        self.links = {}
        self.name = name
        self.fullname = tableName + "." + name

class Link:
    def __init__(self, source, target, tooltip=""):
        self.source = source
        self.target = target
        self.tooltip = tooltip
        print(f'{self.getLinkKey()} [{tooltip}]')

    def getLinkSignature(self):
        return f'\n\t{self.getLinkKey()} [tooltip="{self.tooltip}"];'

    def getLinkKey(self):
        source = self.source.replace(".", ":")
        target = self.target.replace(".", ":")
        return f'{source} -> {target}'

# create dot graph link, for GraphViz
def makeLineage(tables, tablesOnly=False):

    # show all table nodes
    s = ''
    for tableName in tables:
        s += tables[tableName].getNodeSignature(tablesOnly)

    # show all links
    for tableName in tables:
        table = tables[tableName]

        # show only links between tables if tablesOnly
        for linkKey in table.links:
            link = table.links[linkKey]
            if (tablesOnly and '.' not in link.target) \
                or (not tablesOnly and len(link.tooltip) > 0):
                s += link.getLinkSignature()

        # show links between columns if not tablesOnly
        if not tablesOnly:
            for columnName in table.columns:
                column = table.columns[columnName]
                for linkKey in column.links:
                    link = column.links[linkKey]
                    s += link.getLinkSignature()

    # make Graphviz dot graph and save in file
    s = (f'digraph structs {{\n\trankdir=LR;{s}\n}}')
    print(s)
    filename = f"output/table-lineage.dot" if tablesOnly else f"output/column-lineage.dot"
    with open(filename, "w") as file:
        file.write(s)

    # URL encode as query string for remote Graphviz Visual Editor
    s = urllib.parse.quote(s)
    s = f'http://magjac.com/graphviz-visual-editor/?dot={s}'
    print(s)
    return s

def main(argv):

    # get database name
    argparser = argparse.ArgumentParser()
    argparser.add_argument('database')
    args = argparser.parse_args()

    # connect to Snowflake
    parser = configparser.ConfigParser()
    parser.read("profiles_db.conf")

    con = snowflake.connector.connect(
        account=parser.get("default", "account"),
        user=parser.get("default", "user"),
        password = os.getenv('SNOWFLAKE_PASSWORD'))
    cur = con.cursor()

    # load column lineage for the direct objects, for the database
    with open(f"sql/query-access-history.sql", "r") as file:
        sql = file.read()
    sql = sql.replace("{{database}}", args.database)
    results = cur.execute(sql).fetchall()
    con.close()

    # separate result entries into a graph object model
    tables = {};
    for row in results:
        addLink(tables,
            sourceName=addTable(tables, True, str(row[1]), str(row[3])),
            targetName=addTable(tables, False, str(row[2])),
            tooltip=str(row[0]).replace('"', "'"))

    # generate two online GraphViz interactive images
    webbrowser.open(makeLineage(tables, False))
    webbrowser.open(makeLineage(tables, True))

if __name__ == "__main__":
    main('')
