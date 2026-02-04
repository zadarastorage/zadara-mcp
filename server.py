#!/usr/bin/env python3
"""
Zadara Storage MCP Server

This MCP server provides access to Zadara Storage APIs:
- VPSA Storage Array / VPSA Flash Array
- Object Storage
"""

import asyncio
import json
import os
from typing import Any, Optional
from urllib.parse import urljoin

import boto3
import httpx
from botocore.exceptions import ClientError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Initialize server
app = Server("zadara-storage-mcp")

# Configuration
VPSA_BASE_URL = os.getenv("ZADARA_VPSA_URL", "")
VPSA_API_KEY = os.getenv("ZADARA_VPSA_API_KEY", "")
OBJECT_STORAGE_URL = os.getenv("ZADARA_OBJECT_STORAGE_URL", "")
OBJECT_STORAGE_ACCESS_KEY = os.getenv("ZADARA_OBJECT_ACCESS_KEY", "")
OBJECT_STORAGE_SECRET_KEY = os.getenv("ZADARA_OBJECT_SECRET_KEY", "")


class ZadaraClient:
    """Client for Zadara Storage APIs"""
    
    def __init__(self):
        self.vpsa_base_url = VPSA_BASE_URL
        self.vpsa_api_key = VPSA_API_KEY
        self.object_storage_url = OBJECT_STORAGE_URL
        self.object_access_key = OBJECT_STORAGE_ACCESS_KEY
        self.object_secret_key = OBJECT_STORAGE_SECRET_KEY
        
        # Initialize boto3 S3 client for object storage
        self.s3_client = None
        if self.object_storage_url and self.object_access_key and self.object_secret_key:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.object_storage_url,
                aws_access_key_id=self.object_access_key,
                aws_secret_access_key=self.object_secret_key,
                region_name='us-east-1',  # Default region for S3-compatible storage
                config=boto3.session.Config(signature_version='s3v4')
            )
    
    async def vpsa_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None
    ) -> dict:
        """Make a request to VPSA API"""
        if not self.vpsa_base_url or not self.vpsa_api_key:
            raise ValueError("VPSA credentials not configured")
        
        url = urljoin(self.vpsa_base_url, f"/api/{endpoint}")
        headers = {
            "X-Access-Key": self.vpsa_api_key,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()


# Initialize client
client = ZadaraClient()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        # VPSA Storage Array Tools
        Tool(
            name="vpsa_list_volumes",
            description="List all volumes in the VPSA storage array",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of volumes to return"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination"
                    }
                }
            }
        ),
        Tool(
            name="vpsa_create_volume",
            description="Create a new volume in the VPSA storage array",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the volume"
                    },
                    "capacity": {
                        "type": "integer",
                        "description": "Capacity in GB"
                    },
                    "pool": {
                        "type": "string",
                        "description": "Storage pool name or ID"
                    },
                    "block_size": {
                        "type": "integer",
                        "description": "Block size in KB (optional)"
                    }
                },
                "required": ["name", "capacity", "pool"]
            }
        ),
        Tool(
            name="vpsa_get_volume",
            description="Get details of a specific volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_id": {
                        "type": "string",
                        "description": "Volume ID or name"
                    }
                },
                "required": ["volume_id"]
            }
        ),
        Tool(
            name="vpsa_delete_volume",
            description="Delete a volume from the VPSA storage array",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_id": {
                        "type": "string",
                        "description": "Volume ID or name to delete"
                    }
                },
                "required": ["volume_id"]
            }
        ),
        Tool(
            name="vpsa_list_pools",
            description="List all storage pools in the VPSA",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="vpsa_list_servers",
            description="List all servers connected to the VPSA",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="vpsa_create_snapshot",
            description="Create a snapshot of a volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_id": {
                        "type": "string",
                        "description": "Volume ID to snapshot"
                    },
                    "snapshot_name": {
                        "type": "string",
                        "description": "Name for the snapshot"
                    }
                },
                "required": ["volume_id", "snapshot_name"]
            }
        ),
        Tool(
            name="vpsa_list_snapshots",
            description="List all snapshots",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_id": {
                        "type": "string",
                        "description": "Filter by volume ID (optional)"
                    }
                }
            }
        ),
        Tool(
            name="vpsa_get_performance",
            description="Get performance metrics for the VPSA",
            inputSchema={
                "type": "object",
                "properties": {
                    "interval": {
                        "type": "string",
                        "description": "Time interval (e.g., '1h', '24h', '7d')"
                    }
                }
            }
        ),
        Tool(
            name="vpsa_list_controllers",
            description="List all controllers in the VPSA",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # Object Storage Tools
        Tool(
            name="object_list_buckets",
            description="List all buckets in object storage",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="object_create_bucket",
            description="Create a new bucket in object storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket to create"
                    },
                    "region": {
                        "type": "string",
                        "description": "Region for the bucket (optional)"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="object_delete_bucket",
            description="Delete a bucket from object storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket to delete"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="object_list_objects",
            description="List objects in a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "prefix": {
                        "type": "string",
                        "description": "Prefix filter for object keys (optional)"
                    },
                    "max_keys": {
                        "type": "integer",
                        "description": "Maximum number of keys to return"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="object_get_bucket_policy",
            description="Get the policy of a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="object_set_bucket_policy",
            description="Set the policy of a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "policy": {
                        "type": "object",
                        "description": "Bucket policy JSON"
                    }
                },
                "required": ["bucket_name", "policy"]
            }
        ),
        Tool(
            name="object_get_bucket_versioning",
            description="Get versioning configuration of a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="object_set_bucket_versioning",
            description="Set versioning configuration of a bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["Enabled", "Suspended"],
                        "description": "Versioning status"
                    }
                },
                "required": ["bucket_name", "status"]
            }
        ),
        Tool(
            name="vpsa_custom_request",
            description="Make a custom API request to VPSA Storage Array. Use this for endpoints not covered by other tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "description": "HTTP method"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path (without /api/ prefix)"
                    },
                    "data": {
                        "type": "object",
                        "description": "Request body data (optional)"
                    },
                    "params": {
                        "type": "object",
                        "description": "Query parameters (optional)"
                    }
                },
                "required": ["method", "endpoint"]
            }
        ),
        Tool(
            name="object_custom_request",
            description="Make a custom API request to Object Storage. Use this for endpoints not covered by other tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "description": "HTTP method"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "API endpoint path"
                    },
                    "data": {
                        "type": "object",
                        "description": "Request body data (optional)"
                    },
                    "params": {
                        "type": "object",
                        "description": "Query parameters (optional)"
                    }
                },
                "required": ["method", "endpoint"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    try:
        # VPSA Storage Array Tools
        if name == "vpsa_list_volumes":
            params = {}
            if "limit" in arguments:
                params["limit"] = arguments["limit"]
            if "offset" in arguments:
                params["offset"] = arguments["offset"]
            
            result = await client.vpsa_request("GET", "volumes.json", params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_create_volume":
            data = {
                "name": arguments["name"],
                "capacity": arguments["capacity"],
                "pool": arguments["pool"]
            }
            if "block_size" in arguments:
                data["block_size"] = arguments["block_size"]
            
            result = await client.vpsa_request("POST", "volumes.json", data=data)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_get_volume":
            volume_id = arguments["volume_id"]
            result = await client.vpsa_request("GET", f"volumes/{volume_id}.json")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_delete_volume":
            volume_id = arguments["volume_id"]
            result = await client.vpsa_request("DELETE", f"volumes/{volume_id}.json")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_list_pools":
            result = await client.vpsa_request("GET", "pools.json")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_list_servers":
            result = await client.vpsa_request("GET", "servers.json")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_create_snapshot":
            data = {
                "volume": arguments["volume_id"],
                "display_name": arguments["snapshot_name"]
            }
            result = await client.vpsa_request("POST", "snapshots.json", data=data)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_list_snapshots":
            params = {}
            if "volume_id" in arguments:
                params["volume"] = arguments["volume_id"]
            
            result = await client.vpsa_request("GET", "snapshots.json", params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_get_performance":
            params = {}
            if "interval" in arguments:
                params["interval"] = arguments["interval"]
            
            result = await client.vpsa_request("GET", "performance.json", params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "vpsa_list_controllers":
            result = await client.vpsa_request("GET", "vcontrollers.json")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Object Storage Tools
        elif name == "object_list_buckets":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            response = client.s3_client.list_buckets()
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_create_bucket":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            kwargs = {"Bucket": bucket_name}
            
            if "region" in arguments:
                kwargs["CreateBucketConfiguration"] = {
                    "LocationConstraint": arguments["region"]
                }
            
            response = client.s3_client.create_bucket(**kwargs)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_delete_bucket":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            response = client.s3_client.delete_bucket(Bucket=bucket_name)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_list_objects":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            kwargs = {"Bucket": bucket_name}
            
            if "prefix" in arguments:
                kwargs["Prefix"] = arguments["prefix"]
            if "max_keys" in arguments:
                kwargs["MaxKeys"] = arguments["max_keys"]
            
            response = client.s3_client.list_objects_v2(**kwargs)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_get_bucket_policy":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            response = client.s3_client.get_bucket_policy(Bucket=bucket_name)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_set_bucket_policy":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            policy = arguments["policy"]
            # Convert policy dict to JSON string if needed
            if isinstance(policy, dict):
                policy = json.dumps(policy)
            
            response = client.s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_get_bucket_versioning":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            response = client.s3_client.get_bucket_versioning(Bucket=bucket_name)
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        elif name == "object_set_bucket_versioning":
            if not client.s3_client:
                raise ValueError("Object Storage not configured")
            
            bucket_name = arguments["bucket_name"]
            status = arguments["status"]
            
            response = client.s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={"Status": status}
            )
            return [TextContent(type="text", text=json.dumps(response, indent=2, default=str))]
        
        # Custom Request Tools
        elif name == "vpsa_custom_request":
            method = arguments["method"]
            endpoint = arguments["endpoint"]
            data = arguments.get("data")
            params = arguments.get("params")
            
            result = await client.vpsa_request(method, endpoint, data=data, params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_custom_request":
            return [TextContent(type="text", text="Custom object storage requests are not supported when using boto3. Please use specific tool methods instead.")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
