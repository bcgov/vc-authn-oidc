FROM mcr.microsoft.com/dotnet/core/sdk:2.2 AS build-env
WORKDIR /app

# Copy sln and csproj and restore as distinct layers
COPY oidc-controller/src/*.sln ./
COPY oidc-controller/src/*/*.csproj ./

RUN for file in $(ls *.csproj); do mkdir -p ./${file%.*}/ && mv $file ./${file%.*}/; done

RUN dotnet restore

# Copy everything else and build
COPY oidc-controller/src ./
RUN dotnet publish -c Release -o /app/out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:2.2

EXPOSE 5000

WORKDIR /app

COPY --from=build-env /app/out .

CMD ["dotnet", "VCAuthn.dll"]