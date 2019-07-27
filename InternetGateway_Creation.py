from Taging import attach_tag

def create_internetgateway(client,ig_name,vpc_id):
    
    # Check whether IG is already created or not
    
    internetGatewayId = find_internetgateway(client,ig_name)
    
    if internetGatewayId is None:
    
        response = client.create_internet_gateway()
        
        print(response)
        
        internetGatewayId = response['InternetGateway']['InternetGatewayId']
        
        response = client.attach_internet_gateway(
            InternetGatewayId=internetGatewayId,
            VpcId=vpc_id
        )
        
        print('Internet Gateway Created with ID: ', internetGatewayId)
        
        attach_tag(client,internetGatewayId,ig_name)
        
        return internetGatewayId
        
    else:
        return internetGatewayId
    
def find_internetgateway(client,ig_name):
    
    filters = [{'Name': 'tag:Name', 'Values': [ig_name] }]
    response = client.describe_internet_gateways(Filters = filters)
    
    if len(response['InternetGateways']) > 0:
        return response['InternetGateways'][0]['InternetGatewayId']
    else:
        return None
