#!/usr/bin/env python3
"""
Test script for the object_get_bucket_sizes tool

This script demonstrates how to use the new bucket size calculation feature.
"""

import asyncio
import json
from server import ZadaraClient

async def test_bucket_sizes():
    """Test the bucket size calculation functionality"""
    
    client = ZadaraClient()
    
    print("=" * 80)
    print("Testing Bucket Size Calculation")
    print("=" * 80)
    print()
    
    # Test 1: Get all bucket names
    print("Test 1: List all buckets")
    print("-" * 80)
    try:
        result = await client.object_storage_request("GET", "/")
        if "xml_content" in result:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(result["xml_content"])
            namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
            
            bucket_names = []
            for bucket in root.findall('.//s3:Bucket', namespace):
                name_elem = bucket.find('s3:n', namespace)
                if name_elem is None:
                    name_elem = bucket.find('.//n')
                if name_elem is not None and name_elem.text:
                    bucket_names.append(name_elem.text)
            
            if not bucket_names:
                # Try without namespace
                for bucket in root.findall('.//Bucket'):
                    for child in bucket:
                        tag = child.tag.split('}')[-1]
                        if tag in ['Name', 'n'] and child.text:
                            bucket_names.append(child.text)
                            break
            
            print(f"Found {len(bucket_names)} buckets:")
            for name in bucket_names:
                print(f"  - {name}")
            print()
    except Exception as e:
        print(f"Error listing buckets: {e}")
        print()
    
    # Test 2: Calculate size for a single bucket
    print("Test 2: Calculate size for a single bucket")
    print("-" * 80)
    
    if bucket_names:
        test_bucket = bucket_names[0]
        print(f"Calculating size for bucket: {test_bucket}")
        
        try:
            total_size = 0
            total_objects = 0
            continuation_token = None
            
            while True:
                params = {"list-type": "2", "max-keys": "1000"}
                if continuation_token:
                    params["continuation-token"] = continuation_token
                
                result = await client.object_storage_request("GET", f"/{test_bucket}", params=params)
                
                if "xml_content" in result:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(result["xml_content"])
                    namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
                    
                    # Parse objects
                    contents = root.findall('.//s3:Contents', namespace)
                    if not contents:
                        contents = root.findall('.//Contents')
                    
                    for content in contents:
                        size_elem = None
                        for child in content:
                            tag = child.tag.split('}')[-1]
                            if tag == 'Size' and child.text:
                                size_elem = child
                                break
                        
                        if size_elem is not None:
                            total_size += int(size_elem.text)
                            total_objects += 1
                    
                    # Check for pagination
                    is_truncated = root.find('.//s3:IsTruncated', namespace)
                    if is_truncated is None:
                        is_truncated = root.find('.//IsTruncated')
                    
                    if is_truncated is not None and is_truncated.text == 'true':
                        next_token = root.find('.//s3:NextContinuationToken', namespace)
                        if next_token is None:
                            next_token = root.find('.//NextContinuationToken')
                        
                        if next_token is not None and next_token.text:
                            continuation_token = next_token.text
                        else:
                            break
                    else:
                        break
                else:
                    break
            
            # Format size
            if total_size >= 1024**3:
                size_str = f"{total_size / 1024**3:.2f} GB"
            elif total_size >= 1024**2:
                size_str = f"{total_size / 1024**2:.2f} MB"
            elif total_size >= 1024:
                size_str = f"{total_size / 1024:.2f} KB"
            else:
                size_str = f"{total_size} bytes"
            
            print(f"Bucket: {test_bucket}")
            print(f"Objects: {total_objects}")
            print(f"Size: {size_str} ({total_size:,} bytes)")
            print()
            
        except Exception as e:
            print(f"Error calculating bucket size: {e}")
            print()
    
    # Test 3: Calculate sizes for all buckets
    print("Test 3: Calculate sizes for all buckets")
    print("-" * 80)
    
    all_bucket_stats = []
    total_all_size = 0
    total_all_objects = 0
    
    for bucket_name in bucket_names[:3]:  # Limit to first 3 for demo
        print(f"Processing bucket: {bucket_name}...", end=" ")
        
        try:
            total_size = 0
            total_objects = 0
            continuation_token = None
            
            while True:
                params = {"list-type": "2", "max-keys": "1000"}
                if continuation_token:
                    params["continuation-token"] = continuation_token
                
                result = await client.object_storage_request("GET", f"/{bucket_name}", params=params)
                
                if "xml_content" in result:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(result["xml_content"])
                    namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
                    
                    contents = root.findall('.//s3:Contents', namespace)
                    if not contents:
                        contents = root.findall('.//Contents')
                    
                    for content in contents:
                        size_elem = None
                        for child in content:
                            tag = child.tag.split('}')[-1]
                            if tag == 'Size' and child.text:
                                size_elem = child
                                break
                        
                        if size_elem is not None:
                            total_size += int(size_elem.text)
                            total_objects += 1
                    
                    is_truncated = root.find('.//s3:IsTruncated', namespace)
                    if is_truncated is None:
                        is_truncated = root.find('.//IsTruncated')
                    
                    if is_truncated is not None and is_truncated.text == 'true':
                        next_token = root.find('.//s3:NextContinuationToken', namespace)
                        if next_token is None:
                            next_token = root.find('.//NextContinuationToken')
                        
                        if next_token is not None and next_token.text:
                            continuation_token = next_token.text
                        else:
                            break
                    else:
                        break
                else:
                    break
            
            # Format size
            if total_size >= 1024**3:
                size_str = f"{total_size / 1024**3:.2f} GB"
            elif total_size >= 1024**2:
                size_str = f"{total_size / 1024**2:.2f} MB"
            elif total_size >= 1024:
                size_str = f"{total_size / 1024:.2f} KB"
            else:
                size_str = f"{total_size} bytes"
            
            all_bucket_stats.append({
                "bucket": bucket_name,
                "size": size_str,
                "size_bytes": total_size,
                "objects": total_objects
            })
            
            total_all_size += total_size
            total_all_objects += total_objects
            
            print(f"{size_str} ({total_objects} objects)")
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    print()
    print("Summary:")
    print("-" * 80)
    
    # Format total
    if total_all_size >= 1024**3:
        total_str = f"{total_all_size / 1024**3:.2f} GB"
    elif total_all_size >= 1024**2:
        total_str = f"{total_all_size / 1024**2:.2f} MB"
    elif total_all_size >= 1024:
        total_str = f"{total_all_size / 1024:.2f} KB"
    else:
        total_str = f"{total_all_size} bytes"
    
    print(f"Total size: {total_str} ({total_all_size:,} bytes)")
    print(f"Total objects: {total_all_objects:,}")
    print(f"Buckets processed: {len(all_bucket_stats)}")
    print()
    
    print("=" * 80)
    print("Test completed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_bucket_sizes())
