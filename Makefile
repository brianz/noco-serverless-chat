NAME = "brianz/serverless:1.38.0"

ENVDIR=envs
SERVERLESS_DIR=serverless
LIBS_DIR=$(SERVERLESS_DIR)/lib
SLS_ARGS=

run = docker run --rm -it \
		-v `pwd`:/code \
		--env ENV=$(ENV) \
		--env-file envs/$(ENV) \
		--name=noco-sls-chat-$(ENV) $(NAME) $1


shell : guard-ENV env-dir
	$(call run,bash)
.PHONY: shell

bash : guard-ENV
	docker exec -it noco-sls-chat-$(ENV) bash
.PHONY: bash

env-dir :
	@test -d $(ENVDIR) || mkdir -p $(ENVDIR)
.PHONY: env-dir

clean :
	@test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
	rm -rf $(LIBS_DIR)/*
.PHONY: clean

# make libs should be run from inside the container
libs :
	@test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
	pip install -t $(LIBS_DIR) -r requirements.txt
	rm -rf $(LIBS_DIR)/*.dist-info
	find $(LIBS_DIR) -name '*.pyc' | xargs -r rm
	find $(LIBS_DIR) -name tests | xargs -r rm -rf
	(cd $(SERVERLESS_DIR) && [ -f package.json ] && npm install || echo )
.PHONY: libs

# NOTE:
#
# 	Deployments assume you are already running inside the docker container
#
#	To deploy everything, simply: make deploy
#	To deploy a single function: make deploy function=FunctionName, where
#		FunctionName is the named function in your serverless.yml file
#
deploy : guard-ENV
ifeq ($(strip $(function)),)
	cd serverless && sls deploy -s $(ENV) $(SLS_ARGS)
else
	cd serverless && sls deploy function -s $(ENV) -f $(function)
endif
.PHONY: deploy

destroy : guard-ENV check_remove
	cd serverless && sls remove -s $(ENV)
.PHONY: destroy

check_remove:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
.PHONY: check_remove

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "\033[31mEnvironment variable $* required but not set\033[0m"; \
		exit 1; \
	fi
