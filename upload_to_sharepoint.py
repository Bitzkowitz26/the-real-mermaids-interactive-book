#!/usr/bin/env python3

import os
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

def upload_file_to_sharepoint():
    # SharePoint site URL
    site_url = "https://agenticforceaillc193.sharepoint.com/sites/AgenticForceAI"
    
    # Credentials
    username = "Bitzkowitz@agenticforce.dev"
    password = "Itzkowitz@89"
    
    # File to upload
    file_path = "/workspace/InsightBridge_Analysis_Phase0_Recommendations.pdf"
    
    # Target folder in SharePoint
    target_folder = "/sites/AgenticForceAI/Shared Documents/AgenticForce/Sales/Projects/Report Engine - Greg/Scope of Work"
    
    try:
        # Create client context
        ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
        
        # Get the target folder
        target_folder_obj = ctx.web.get_folder_by_server_relative_url(target_folder)
        
        # Read the file
        with open(file_path, 'rb') as file_content:
            file_name = os.path.basename(file_path)
            
            # Upload the file
            target_file = target_folder_obj.upload_file(file_name, file_content.read())
            ctx.execute_query()
            
            print(f"File '{file_name}' uploaded successfully to SharePoint!")
            print(f"File URL: {target_file.serverRelativeUrl}")
            
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    upload_file_to_sharepoint()