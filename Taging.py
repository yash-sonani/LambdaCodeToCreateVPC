def attach_tag(client,resourceId,tagName):
    
    tagresponse = client.create_tags(Resources = [resourceId], Tags=[{"Key": "Name", "Value": tagName}])
    
    print('Tag attached for ', resourceId)
