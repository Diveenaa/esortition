FROM --platform=linux/amd64 kong:latest as build

COPY prod_kong.yml /usr/local/kong/declarative/kong.yml
ENV KONG_DECLARATIVE_CONFIG="/usr/local/kong/declarative/kong.yml"