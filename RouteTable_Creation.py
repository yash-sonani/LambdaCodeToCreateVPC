from Taging import attach_tag

def create_routetable(client,vpc_Id,rt_name,InternetGatewayId,flag):
    
    # check whether route table already created or not
    
    routeTableId = find_routetable(client,rt_name)
    
    if routeTableId is None:
    
        response = client.create_route_table(
            VpcId=vpc_Id
        )
        
        routeTableId = response['RouteTable']['RouteTableId']
        
        print('Route Table created with ID: ', routeTableId)
        
        attach_tag(client,routeTableId,rt_name)
        
        if flag == 'Y':
        
            create_route(client,InternetGatewayId,routeTableId)
            print('Route Created in Table with IG: ', InternetGatewayId)
        
        return routeTableId
    
    else:
        
        return routeTableId
    
def create_route(client,InternetGatewayId,routeTableId):
    
    response = client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        #EgressOnlyInternetGatewayId=InternetGatewayId,
        GatewayId=InternetGatewayId,
        RouteTableId=routeTableId
    )
    
    print('Route Entry added for : ', routeTableId)
    
    return response['Return']

def find_routetable(client,rt_name):
    
    filters = [{'Name': 'tag:Name', 'Values': [rt_name] }]
    response = client.describe_route_tables(Filters = filters)
    
    if len(response['RouteTables']) > 0:
        return response['RouteTables'][0]['RouteTableId']
    else:
        return None
