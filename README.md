## Coreon-MCP-Execution-Engine-audit-code
**Welcome to Coreon MCP Execution Engine**

## **Application Scenarios**：

##### 1.CLI

Execute Code:   cli/mcp_cli.py -> mian()

##### 2.Telegram Bot

Execute Code:   Bot/telegram_bot.py -> start_bot()

##### 3.Server API

Execute Code:  Server/mcp_server.py -> create_app()



## **Business Logic:** 

##### 1.Obtain User Input

```
toolcalls = planner.plan(user_input)
```

##### 2. Process User Natural Language into Planner Execution Steps

```
results = await execute_toolcall_chain(toolcalls, registry=tool_registry)
```

##### 3.  Execute Sequentially and Return Results

```
reply = generate_final_reply(user_input, results, lang=settings.MCP_LANG)
```



## **On-chain Interaction Capability**

##### 1.Query Market-related Information**

tools/market/logic

##### 2.Query Token-related Information

tools/token/logic