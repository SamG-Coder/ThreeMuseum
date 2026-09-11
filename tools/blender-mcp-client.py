"""Call the official Blender Lab MCP server over stdio, with an audit log.

Run with the Python environment containing Blender Lab's blender-mcp package.
Blender must already be serving its MCP add-on on localhost:9876.
"""
import argparse
import asyncio
import datetime
import json
import os
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tool')
    parser.add_argument('--args', default='{}')
    parser.add_argument('--code-file', type=Path)
    args = parser.parse_args()
    arguments = json.loads(args.args)
    if args.code_file:
        arguments['code'] = args.code_file.read_text(encoding='utf-8')
    params = StdioServerParameters(command=sys.executable,
        args=['-c', 'from blmcp import main; main()'],
        env={**os.environ, 'BLENDER_MCP_HOST': '127.0.0.1'})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if args.tool == 'list':
                response = await session.list_tools()
            else:
                response = await session.call_tool(args.tool, arguments)
            payload = response.model_dump(mode='json', exclude_none=True)
            log = Path(__file__).resolve().parents[1] / 'docs/validation/blender-mcp.jsonl'
            with log.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps({'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'tool': args.tool, 'arguments': arguments, 'response': payload}) + '\n')
            visible=payload.get('structuredContent', payload)
            if isinstance(visible,dict) and len(visible.get('stdout',''))>1000:
                visible={**visible, 'stdout':visible['stdout'][-1000:]}
            print(json.dumps(visible, indent=2))
            if getattr(response, 'isError', False) or (isinstance(visible,dict) and visible.get('status')=='error'):
                raise RuntimeError('Blender MCP tool returned an error')

if __name__ == '__main__':
    asyncio.run(main())
