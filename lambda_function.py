import json
import boto3
import xlrd
from xlrd.book import open_workbook_xls
import xlwt
import sys

from VPC_Creation import create_vpc
from DHCP_Creation import create_dhcp
from Subnets_Creation import create_subnets
from RouteTable_Creation import create_routetable
from InternetGateway_Creation import create_internetgateway

def lambda_handler(event, context):
    # TODO implement
    
    ec2Resource = boto3.resource('ec2')
    ec2Client = boto3.client('ec2')
    
    bucketName = 's3_bucket_name' # Update with your bucket name
    filePath = 'vpc_detail.xls' # Update with your detials file name
    
    workbook = read_xls(bucketName,filePath)
    
    #Creating VPC
    data = read_vpc_detail(workbook)
    
    print('data: ' , data)
    
    # DHCP Creation
    try: 
        DhcpOptionsId = create_dhcp(ec2Client,data['DHCP'],'null')
        print('Dhcp Options ID : ' , DhcpOptionsId)
    except:
        print('DHCP Creation Exception')
        print(sys.exc_info())
    
    
    # VPC Creaetion
    try:
        vpc_id = create_vpc(ec2Resource,ec2Client,data['CidrBlock'],data['vpc_name'],DhcpOptionsId)
        print('VPC_ID: ', vpc_id)
    except:
        print('VPC Creation Exception')
        print(sys.exc_info())
        
    
    # Internet Gateway Creation
    
    try :
        InternetGatewayId = create_internetgateway(ec2Client,data['IG'],vpc_id)
        print('Internet Gateway ID: ', InternetGatewayId)
    except:
        print('Internet Gateway Creation Exception')

    
    # Public Route Table Creation
    
    try:
        RoutetableId = create_routetable(ec2Client,vpc_id,data['PRT'],InternetGatewayId,'Y')
        print('Public Route table ID:' , RoutetableId )
    except:
        print('Public Route Table Creation Exception')
        print(sys.exc_info())
    
    
    # private Route Table Creation
    
    try:
        RoutetableId = create_routetable(ec2Client,vpc_id,data['PRRT'],InternetGatewayId,'N')
        print('Private Route table ID:' , RoutetableId )
    except:
        print('Route Table Creation Exception')
        print(sys.exc_info())
    
    
    # Creating Subnets
    subnets = subnet_creation_from_xls(workbook,ec2Client,vpc_id)
    
    print(subnets)

    return {
        'body': 'Lambda Works!!!'
    }


def read_xls(bucketName,filePath):
    
    # Read File From S3 Bucket
    s3Client = boto3.client('s3')
    data = s3Client.get_object(Bucket=bucketName, Key=filePath)

    content = data['Body'].read()

    # Read xls File for API-Gateway Detail
    workbook = open_workbook_xls(file_contents=content)
    
    return workbook

def read_vpc_detail(workbook):
    
    data = {}
    
    sheet1 = workbook.sheet_by_index(0)
    
    data['vpc_name'] = sheet1.cell_value(0,1)
    data['CidrBlock'] = sheet1.cell_value(1,1)
    data['IG'] = sheet1.cell_value(2,1)
    data['PRT'] = sheet1.cell_value(3,1)
    data['PRRT'] = sheet1.cell_value(4,1)
    data['DHCP'] = sheet1.cell_value(5,1)
        
    return data
    
def subnet_creation_from_xls(workbook,client,vpc_id):
    
    sheet2 = workbook.sheet_by_index(1)
    subnets = {}
    #data = []
    #row = []
    index = 1
    
    while(True):
        
        if (sheet2.nrows == index):
            break
        
        #row.append(sheet2.cell_value(index,1))
        #row.append(sheet2.cell_value(index,2))
        
        # First Availability Zone
        
        CidrBlock = sheet2.cell_value(index,1)
        tag_name = sheet2.cell_value(index,2)
        availability_zone = sheet2.cell_value(index,3)
        IsPublic = sheet2.cell_value(index,7)
        
        try :
            subnet_id = create_subnets(client,CidrBlock,availability_zone,vpc_id,tag_name,IsPublic)
            subnets[tag_name] = subnet_id
        except : 
            print('Exception in subnet creation: ', tag_name)
            print(sys.exc_info())
        
        
        # Second Availability Zone
        
        CidrBlock = sheet2.cell_value(index,4)
        tag_name = sheet2.cell_value(index,5)
        availability_zone = sheet2.cell_value(index,6)        
        IsPublic = sheet2.cell_value(index,7)
        
        try : 
            subnet_id = create_subnets(client,CidrBlock,availability_zone,vpc_id,tag_name,IsPublic)
            subnets[tag_name] = subnet_id
        except:
            print('Exception in subnet creation: ', tag_name)
            print(sys.exc_info())
            
        index = index + 1
    
    return subnets    
