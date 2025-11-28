# 项目修改总结

## 1. RCA 自动化脚本 (`auto_rca.py`)
- **目的**: 自动化 `question_3` 场景的根因分析 (RCA) 工作流。
- **功能**:
    - 从 `question_3/problem.json` 读取问题描述和提示词 (prompt)。
    - 初始化 `autoagent` 环境（Docker 配置、代码/Web/文件环境）。
    - 实例化 `System Triage Agent` 和 `MetaChain` 客户端。
    - 使用提示词执行 Agent，支持多轮推理。
    - 从 Agent 的最终响应中提取“根因服务 (Root cause service)”。
    - 将完整的推理轨迹（消息、Agent 动作）和最终结论保存到 `output.json`。

## 2. 工具集成 (`autoagent/tools/parquet_tools.py`)
- **目的**: 提供工具让 Agent 能够交互式操作 Parquet 文件。
- **修改内容**:
    - 实现了 `list_tables_in_directory`: 扫描 Parquet 文件并返回元数据（行数、列信息）。
    - 实现了 `get_schema`: 返回特定 Parquet 文件的 Schema（列名、类型）。
    - 实现了 `query_parquet_files`: 使用 `duckdb` 对 Parquet 文件执行 SQL 查询。
    - **增强功能**:
        - 增加了健壮的路径处理，支持绝对路径和相对路径。
        - 增加了 Token 限制强制执行，防止过大的查询结果溢出上下文窗口。
        - 增加了对 datetime 对象的 JSON 序列化支持。

## 3. Agent 配置
- **目的**: 限制 Agent 的能力范围，使其专注于 RCA 任务。
- **修改内容**:
    - 配置 `System Triage Agent` 主要使用 `Coding Agent`。
    - 注册了 Parquet 工具 (`list_tables_in_directory`, `get_schema`, `query_parquet_files`) 供 Agent 使用。

## 4. 依赖管理
- **目的**: 确保必要的库可用。
- **修改内容**:
    - 确定了对 `duckdb` 和 `pydantic` 的需求。
    - （注：用户手动处理了一些安装步骤或环境配置）。

## 5. 输出生成
- **目的**: 结构化的分析输出。
- **修改内容**:
    - `auto_rca.py` 脚本生成 `output.json`，包含：
        - 初始提示词 (prompt)。
        - 完整的消息交互列表（推理步骤）。
        - 最终识别出的根因服务。
