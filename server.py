#!/usr/bin/env python3
"""
Zadara Storage MCP Server

This MCP server provides access to Zadara Storage APIs:
- VPSA Storage Array / VPSA Flash Array
- Object Storage
"""

import asyncio
import base64
import hashlib
import hmac
import json
import os
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

import httpx
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
    
    def _sign_aws_request(
        self,
        method: str,
        url: str,
        headers: dict,
        payload: bytes = b""
    ) -> dict:
        """Generate AWS Signature V4 for request"""
        if not self.object_access_key or not self.object_secret_key:
            return headers
        
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or "/"
        
        # Current timestamp
        now = datetime.utcnow()
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = now.strftime("%Y%m%d")
        
        # Calculate payload hash
        payload_hash = hashlib.sha256(payload).hexdigest()
        
        # Canonical headers
        canonical_headers = f"host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
        signed_headers = "host;x-amz-content-sha256;x-amz-date"
        
        # Canonical request
        canonical_request = f"{method}\n{path}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
        
        # String to sign
        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = f"{date_stamp}/us-east-1/s3/aws4_request"
        string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}"
        
        # Calculate signature
        def sign(key, msg):
            return hmac.new(key, msg.encode(), hashlib.sha256).digest()
        
        k_date = sign(f"AWS4{self.object_secret_key}".encode(), date_stamp)
        k_region = sign(k_date, "us-east-1")
        k_service = sign(k_region, "s3")
        k_signing = sign(k_service, "aws4_request")
        signature = hmac.new(k_signing, string_to_sign.encode(), hashlib.sha256).hexdigest()
        
        # Authorization header
        authorization = f"{algorithm} Credential={self.object_access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        
        # Update headers
        headers["Authorization"] = authorization
        headers["x-amz-date"] = amz_date
        headers["x-amz-content-sha256"] = payload_hash
        headers["Host"] = host
        
        return headers
    
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
    
    async def object_storage_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        content_type: str = "application/json"
    ) -> dict:
        """Make a request to Object Storage API with AWS Signature V4"""
        if not self.object_storage_url:
            raise ValueError("Object Storage URL not configured")
        
        url = urljoin(self.object_storage_url, endpoint)
        
        # Prepare request body
        body = b""
        if data:
            body = json.dumps(data).encode('utf-8')
        
        # Prepare headers for AWS Signature V4
        headers = {
            "Content-Type": content_type
        }
        
        # Add AWS Signature V4 authentication if credentials are provided
        if self.object_access_key and self.object_secret_key:
            headers = self._sign_aws_request(method, url, headers, body)
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body if body else None,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            
            # Handle different response types
            content_type_header = response.headers.get("content-type", "")
            if "application/json" in content_type_header:
                return response.json()
            elif "application/xml" in content_type_header or "text/xml" in content_type_header:
                # For XML responses (like S3 ListBucket), return the text
                return {"xml_content": response.text}
            else:
                return {"content": response.text, "status_code": response.status_code}
    
    async def upload_object(
        self,
        bucket_name: str,
        object_key: str,
        content: bytes,
        content_type: str = "application/octet-stream"
    ) -> dict:
        """Upload an object to Object Storage"""
        if not self.object_storage_url:
            raise ValueError("Object Storage URL not configured")
        
        url = urljoin(self.object_storage_url, f"/{bucket_name}/{object_key}")
        headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(content))
        }
        
        # Sign the request with AWS Signature V4
        headers = self._sign_aws_request("PUT", url, headers, content)
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=url,
                content=content,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "bucket": bucket_name,
                "key": object_key,
                "size": len(content)
            }
    
    async def download_object(
        self,
        bucket_name: str,
        object_key: str
    ) -> dict:
        """Download an object from Object Storage"""
        if not self.object_storage_url:
            raise ValueError("Object Storage URL not configured")
        
        url = urljoin(self.object_storage_url, f"/{bucket_name}/{object_key}")
        headers = {}
        
        # Sign the request with AWS Signature V4
        headers = self._sign_aws_request("GET", url, headers)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content,
                "content_type": response.headers.get("content-type", ""),
                "size": len(response.content)
            }
    
    async def delete_object(
        self,
        bucket_name: str,
        object_key: str
    ) -> dict:
        """Delete an object from Object Storage"""
        if not self.object_storage_url:
            raise ValueError("Object Storage URL not configured")
        
        url = urljoin(self.object_storage_url, f"/{bucket_name}/{object_key}")
        headers = {}
        
        # Sign the request with AWS Signature V4
        headers = self._sign_aws_request("DELETE", url, headers)
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url=url,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "bucket": bucket_name,
                "key": object_key
            }


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
            name="object_upload",
            description="Upload an object to object storage. Provide file content as base64-encoded string.",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Object key/path (e.g., 'document.pdf' or 'folder/file.txt')"
                    },
                    "content_base64": {
                        "type": "string",
                        "description": "Base64-encoded file content"
                    },
                    "content_type": {
                        "type": "string",
                        "description": "MIME type (default: application/octet-stream)"
                    }
                },
                "required": ["bucket_name", "object_key", "content_base64"]
            }
        ),
        Tool(
            name="object_download",
            description="Download an object from object storage. Returns base64-encoded content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Object key/path"
                    }
                },
                "required": ["bucket_name", "object_key"]
            }
        ),
        Tool(
            name="object_delete",
            description="Delete an object from object storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Object key/path to delete"
                    }
                },
                "required": ["bucket_name", "object_key"]
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
            result = await client.object_storage_request("GET", "/")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_create_bucket":
            bucket_name = arguments["bucket_name"]
            data = {}
            if "region" in arguments:
                data["CreateBucketConfiguration"] = {
                    "LocationConstraint": arguments["region"]
                }
            
            result = await client.object_storage_request("PUT", f"/{bucket_name}", data=data)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_delete_bucket":
            bucket_name = arguments["bucket_name"]
            result = await client.object_storage_request("DELETE", f"/{bucket_name}")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_list_objects":
            bucket_name = arguments["bucket_name"]
            params = {}
            if "prefix" in arguments:
                params["prefix"] = arguments["prefix"]
            if "max_keys" in arguments:
                params["max-keys"] = arguments["max_keys"]
            
            result = await client.object_storage_request("GET", f"/{bucket_name}", params=params)
            
            # Parse XML response if present
            if "xml_content" in result:
                try:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(result["xml_content"])
                    
                    # Parse S3 ListBucket response
                    objects = []
                    
                    # Try different XML structures
                    # First try with namespace
                    namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
                    contents = root.findall('.//s3:Contents', namespace)
                    
                    # If not found, try without namespace
                    if not contents:
                        contents = root.findall('.//Contents')
                    
                    # If still not found, try root level Contents
                    if not contents:
                        for child in root:
                            if child.tag.endswith('Contents') or child.tag == 'Contents':
                                contents.append(child)
                    
                    for content in contents:
                        # Try to find Key
                        key_elem = None
                        size_elem = None
                        modified_elem = None
                        
                        for child in content:
                            tag = child.tag.split('}')[-1]  # Remove namespace if present
                            if tag == 'Key':
                                key_elem = child
                            elif tag == 'Size':
                                size_elem = child
                            elif tag == 'LastModified':
                                modified_elem = child
                        
                        # Only add if we found a Key
                        if key_elem is not None and key_elem.text:
                            obj = {
                                "Key": key_elem.text,
                                "Size": int(size_elem.text) if size_elem is not None and size_elem.text else 0,
                                "LastModified": modified_elem.text if modified_elem is not None and modified_elem.text else ""
                            }
                            objects.append(obj)
                    
                    formatted_result = {
                        "Bucket": bucket_name,
                        "Objects": objects,
                        "Count": len(objects)
                    }
                    
                    # If no objects found, show raw XML for debugging
                    if len(objects) == 0:
                        return [TextContent(type="text", text=f"No objects found. Raw XML for debugging:\n\n{result['xml_content']}")]
                    
                    return [TextContent(type="text", text=json.dumps(formatted_result, indent=2))]
                except Exception as e:
                    return [TextContent(type="text", text=f"XML parsing error: {str(e)}\n\nRaw XML response:\n{result['xml_content']}")]
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_get_bucket_policy":
            bucket_name = arguments["bucket_name"]
            result = await client.object_storage_request("GET", f"/{bucket_name}?policy")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_set_bucket_policy":
            bucket_name = arguments["bucket_name"]
            policy = arguments["policy"]
            result = await client.object_storage_request("PUT", f"/{bucket_name}?policy", data=policy)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_get_bucket_versioning":
            bucket_name = arguments["bucket_name"]
            result = await client.object_storage_request("GET", f"/{bucket_name}?versioning")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_set_bucket_versioning":
            bucket_name = arguments["bucket_name"]
            data = {
                "VersioningConfiguration": {
                    "Status": arguments["status"]
                }
            }
            result = await client.object_storage_request("PUT", f"/{bucket_name}?versioning", data=data)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_upload":
            bucket_name = arguments["bucket_name"]
            object_key = arguments["object_key"]
            content_base64 = arguments["content_base64"]
            content_type = arguments.get("content_type", "application/octet-stream")
            
            # Decode base64 content
            content = base64.b64decode(content_base64)
            
            result = await client.upload_object(bucket_name, object_key, content, content_type)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_download":
            bucket_name = arguments["bucket_name"]
            object_key = arguments["object_key"]
            
            result = await client.download_object(bucket_name, object_key)
            
            # Encode content as base64 for transport
            content_base64 = base64.b64encode(result["content"]).decode()
            
            response = {
                "bucket": bucket_name,
                "key": object_key,
                "content_type": result["content_type"],
                "size": result["size"],
                "content_base64": content_base64
            }
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
        
        elif name == "object_delete":
            bucket_name = arguments["bucket_name"]
            object_key = arguments["object_key"]
            
            result = await client.delete_object(bucket_name, object_key)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Custom Request Tools
        elif name == "vpsa_custom_request":
            method = arguments["method"]
            endpoint = arguments["endpoint"]
            data = arguments.get("data")
            params = arguments.get("params")
            
            result = await client.vpsa_request(method, endpoint, data=data, params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "object_custom_request":
            method = arguments["method"]
            endpoint = arguments["endpoint"]
            data = arguments.get("data")
            params = arguments.get("params")
            
            result = await client.object_storage_request(method, endpoint, data=data, params=params)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
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
