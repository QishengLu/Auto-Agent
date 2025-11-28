FROM tjbtech1/metachain:amd64_latest

# 安装 duckdb 用于 parquet 文件查询
# 虽然 parquet_tools.py 只依赖 duckdb，但在 RCA 分析中，
# Agent 可能会编写使用 pandas/pyarrow 的代码来处理数据，因此建议一并安装。
RUN pip install duckdb pandas pyarrow
