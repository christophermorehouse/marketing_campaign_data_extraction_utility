# Build executable
python setup.py build

# Remove cf_Freeze license
Remove-Item -Path ./marketing_campaign_data_extraction_utility/frozen_application_license.txt

# Create application zip for deployment
Set-Location ./build
Compress-Archive -Path ./marketing_campaign_data_extraction_utility -DestinationPath ./marketing_campaign_data_extraction_utility.zip