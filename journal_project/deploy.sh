resource_group_name="inkwell-rg"
location="uksouth"
acr_name="inkwellacr"
image_name="inkwell-img"
app_plan_name="your-app-service-plan-name"
app_name="inkwell-app"

az group create --name $resource_group_name --location $location

az acr create --resource-group $resource_group_name --name $acr_name --sku Standard --admin-enabled true

az acr login --name $acr_name

docker build -t $acr_name.azurecr.io/$image_name:latest .
docker push $acr_name.azurecr.io/$image_name:latest

az appservice plan create --name $app_plan_name --resource-group $resource_group_name --sku F1 --is-linux
az webapp create --name $app_name --resource-group $resource_group_name --plan $app_plan_name --runtime "PYTHON|3.10"

az webapp config container set --name $app_name --resource-group $resource_group_name --docker-custom-image-name $acr_name.azurecr.io/$image_name:latest
