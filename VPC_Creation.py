from Taging import attach_tag

def create_vpc(resource,client,cicd_block,vpc_name,DhcpOptionsId):
    
    
    # Check whether VPC is already created or not
    
    vpc_id = find_vpc(client,vpc_name)
    
    if vpc_id is None:
    
        response = resource.create_vpc(
            CidrBlock=cicd_block,
            AmazonProvidedIpv6CidrBlock=False,
            InstanceTenancy='default'    
        )
        
        vpc_id = response.id
        
        # Attached Tag in created VPC
        attach_tag(client,response.id,vpc_name)
        
        client.modify_vpc_attribute( VpcId = vpc_id , EnableDnsSupport = { 'Value': True } )
        client.modify_vpc_attribute( VpcId = vpc_id , EnableDnsHostnames = { 'Value': True } )
        
        attach_dhcp(client,vpc_id,DhcpOptionsId)
        
        print('VPC Created with ID: ', vpc_id)
        
        return vpc_id
        
    else:
        return vpc_id
    
def attach_dhcp(client,vpc_id,dhcp_id):
    
    response = client.associate_dhcp_options(
        DhcpOptionsId=dhcp_id,
        VpcId=vpc_id
    )
    
    print('DHCP is attached')
    
def find_vpc(client,vpc_name):
    
    filters = [{'Name': 'tag:Name', 'Values': [vpc_name] }]
    response = client.describe_vpcs(Filters=filters)
    
    if len(response['Vpcs']) > 0:
        return response['Vpcs'][0]['VpcId']
    else:
        return None
