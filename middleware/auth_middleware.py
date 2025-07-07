from fastmcp.server.middleware import MiddlewareContext
from mcp.types import ErrorData
from mcp import McpError

class AuthMiddleware:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def __call__(self, context: MiddlewareContext, call_next):
        # Only check authentication for HTTP requests (not stdio)
        try:
            if hasattr(context.fastmcp_context, 'request_context') and context.fastmcp_context.request_context:
                request_obj = context.fastmcp_context.request_context.request
                api_key = request_obj.headers.get('x-api-key')
                
                # Check if API key matches the server API key
                if api_key != self.api_key:
                    # Return an error response for unauthorized access
                    raise McpError(
                        ErrorData(
                            code=-32001,  # Custom error code for unauthorized
                            message="Unauthorized: Invalid API key"
                        )
                    )
                
        except McpError:
            # Re-raise MCP errors (like our unauthorized error)
            raise
        
        return await call_next(context)