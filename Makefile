REGISTRY_HOST=docker.io
USERNAME=ripl
#NAME=$(shell basename $(CURDIR))
NAME=uptimekuma-push-agent

IMAGE=$(USERNAME)/$(NAME)


.PHONY: pre-build docker-build build release \
	push cleanup up down pull remove update


#all:


up: ## bring up the container
	docker-compose -p $(NAME) up -d

down: ## bring down the container
	docker-compose -p $(NAME) down

pull: ## pull the latest image from dockerhub
	docker pull $(IMAGE)

remove:
	# Trying to remove uptimekuma-push-agent will throw an error if it doesn't exist
	@if [ "$(docker ps -f name=$(NAME) | grep -w $(NAME))" ]; then\
		docker rm $(NAME);\
	else \
    	echo "No container matching $(NAME) was found";\
	fi

update: pull down remove up ## TEST



# The targets below are relevant to building and pushing the image

build: pre-build docker-build ## builds a new version of the container image(s)


post-build:


pre-push:


post-push:


docker-build:

	# Build latest with multiple tags
	docker buildx build --platform linux/arm64/v8,linux/amd64 --tag $(IMAGE) -f Dockerfile .


release: build push	## builds a new version of your container image(s), and pushes it/them to the registry


push: pre-push do-push post-push ## pushes the images to dockerhub

do-push: 
	# Push latest
	docker buildx build --platform linux/arm64/v8,linux/amd64 --push --tag $(IMAGE)  -f Dockerfile .


cleanup: ## Remove images pulled/generated as part of the build process
	docker rmi $(IMAGE)
	


# Shows help
help:           ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | grep -v fgrep | sed -e 's/\([^:]*\):[^#]*##\(.*\)/printf '"'%-20s - %s\\\\n' '\1' '\2'"'/' |bash
