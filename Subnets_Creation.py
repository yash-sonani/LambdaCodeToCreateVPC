from Taging import attach_tag

def create_subnets(client,CidrBlock,availability_zone,VpcId,subnet_name,IsPublic):
    
    # check whether sunet is already created or not
    
    SubnetId = find_subnet(client,VpcId,CidrBlock,availability_zone,subnet_name)
    
    if SubnetId is None:
    
        response = client.create_subnet(
            AvailabilityZone=availability_zone,
            CidrBlock=CidrBlock,
            VpcId=VpcId
        )
        
        
        SubnetId = response['Subnet']['SubnetId']
        
        if IsPublic == 'Y' :
        
            response = client.modify_subnet_attribute(
                MapPublicIpOnLaunch={
                    'Value': True
                },
                SubnetId=SubnetId
            )
        
        attach_tag(client,SubnetId,subnet_name)
        
        print('Subnet is created with ID: ',SubnetId)
        
        return SubnetId
        
    else:
        
        return SubnetId
    
def find_subnet(client,VpcId,CidrBlock,availability_zone,subnet_name):
    
    filters = [
        {'Name': 'tag:Name', 'Values': [subnet_name]},
        {'Name' : 'vpc-id' , 'Values' : [VpcId]},
        {'Name': 'cidr-block' , 'Values' : [CidrBlock]},
        {'Name': 'availability-zone' , 'Values' : [availability_zone]}
    ]
    response = client.describe_subnets(Filters=filters)
    
    if len(response['Subnets']) > 0:
        return response['Subnets'][0]['SubnetId']
    else:
        return None
