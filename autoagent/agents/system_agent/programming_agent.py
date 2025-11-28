from autoagent.types import Agent
from autoagent.tools.parquet_tools import (
    query_parquet_files, get_schema, list_tables_in_directory
)
from autoagent.registry import register_agent, register_plugin_agent
from typing import Union

def examples(context_variables):
    return []

@register_agent(name= "Coding Agent", func_name="get_coding_agent")
@register_plugin_agent(name= "Coding Agent", func_name="get_coding_agent")
def get_coding_agent(model: str, **kwargs):
    def instructions(context_variables):
      return """You are a specialized Data Analysis Agent capable of analyzing Parquet files directly.
Your goal is to perform Root Cause Analysis (RCA) or data exploration by querying parquet files.

You have access to the following tools:
1. `list_tables_in_directory(directory)`: Discover available parquet files.
2. `get_schema(parquet_file)`: Inspect the schema (columns, types) of a file.
3. `query_parquet_files(parquet_files, query, limit)`: Execute SQL queries against the files.

Workflow:
1. Always start by listing files to know what data is available.
2. Check schemas of relevant files to understand columns.
3. Construct SQL queries (DuckDB dialect) to analyze the data.
4. Use the query results to infer root causes or answer user questions.

Important:
- You do NOT need to write Python code or create files.
- Execute SQL queries directly using `query_parquet_files`.
- If a query fails, analyze the error and adjust the query.
- Use `transfer_back_to_triage_agent` when you have completed the analysis.
"""
    tool_list = [query_parquet_files, get_schema, list_tables_in_directory]
    
    return Agent(
    name="Coding Agent",
    model=model,
    instructions=instructions,
    functions=tool_list,
    examples=examples,
    tool_choice = "required", 
    parallel_tool_calls = False
    )