import json
import os
import re
from autoagent.core import MetaChain
from autoagent.agents.system_agent.system_triage_agent import get_system_triage_agent
from autoagent.cli import get_config, create_environment

def get_prompt():
    prompt_path = 'question_3/problem.json'
    if not os.path.exists(prompt_path):
        print(f"Warning: {prompt_path} not found.")
        return ""
    
    with open(prompt_path, 'r') as f:
        content = f.read().strip()
        
    # Handle the case where the file content is a Python variable assignment
    # TASK_DESCRIPTION = """..."""
    match = re.search(r'TASK_DESCRIPTION\s*=\s*"""(.*?)"""', content, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback: return content as is if it doesn't match the pattern
    return content

def main():
    # 初始化配置和环境
    docker_config = get_config("deepresearch", 12346)
    code_env, web_env, file_env = create_environment(docker_config)
    
    context_variables = {
        "working_dir": docker_config.workplace_name,
        "code_env": code_env,
        "web_env": web_env,
        "file_env": file_env
    }
    
    # 初始化 agent 和 client
    agent = get_system_triage_agent(model="gpt-4-turbo")
    client = MetaChain()
    
    # 从文件读取 prompt
    prompt = get_prompt()
    if not prompt:
        print("Error: Could not load prompt from question_3/problem.json")
        return

    print("Starting Auto-Deep-Research agent with prompt from file...")
    messages = [{"role": "user", "content": prompt}]
    
    # 执行查询 - 这会自动处理所有多轮循环
    response = client.run(
        agent=agent,
        messages=messages,
        context_variables=context_variables,
        debug=False
    )
    
    # 尝试从最后一条消息中提取 Root cause service
    final_answer = "UNKNOWN"
    if response.messages:
        last_msg = response.messages[-1]['content']
        # Look for "Root cause service: ..."
        rc_match = re.search(r'Root cause service:\s*(.*)', last_msg)
        if rc_match:
            final_answer = f"Root cause service: {rc_match.group(1).strip()}"
        else:
            final_answer = last_msg # Fallback to full message if pattern not found

    # response.messages 已经包含了所有轮次的完整推理轨迹
    reasoning_trace = {
        "prompt": prompt,
        "messages": response.messages,  # 这里包含所有轮次
        "final_agent": response.agent.name if response.agent else None,
        "total_turns": len(response.messages),
        "final_answer": final_answer
    }
    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(reasoning_trace, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"推理轨迹已保存到 output.json,共 {len(response.messages)} 轮")

if __name__ == "__main__":
    main()