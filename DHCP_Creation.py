from Taging import attach_tag


def create_dhcp(client,dhcp_name,domain_name):
    
    # Check whether DHCP is created of not
    
    DhcpOptionsId = find_dhcp(client,dhcp_name)
    
    if DhcpOptionsId is None:
    
        response = client.create_dhcp_options(
            DhcpConfigurations=[
                {
                    'Key': 'domain-name-servers',
                    'Values': [
                        'AmazonProvidedDNS'
                    ],
                },
                {    
                     'Key': 'domain-name',
                     'Values': [ 
                         domain_name 
                    ],
                },
            ],
        )
        
        DhcpOptionsId = response['DhcpOptions']['DhcpOptionsId']
    
        attach_tag(client,DhcpOptionsId,dhcp_name)
        
        print('DHCP is created with ID: ', dhcp_id)
        
        return DhcpOptionsId
    
    else:
        return DhcpOptionsId


def find_dhcp(client,dhcp_name):
    
    filters = [{'Name': 'tag:Name', 'Values': [dhcp_name] }]
    response = client.describe_dhcp_options(Filters=filters)
    
    
    if len(response['DhcpOptions']) > 0:
        return response['DhcpOptions'][0]['DhcpOptionsId']
    else:
        return None
    
