.PHONY: all build test clean

WORKINGDIR:=./Debug
ORIGINALS:=./remoniproject/
FAKES:=./Debug/remoniproject/zwave/fakes

# Create Local Test project to run Unit Tests in ./Debug

all: build test clean
build:
		@echo "Building Local Test App"
		@mkdir -p ${WORKINGDIR}
		@cp ./tests/tests_multisensor.py ${WORKINGDIR}
		@cp -r ${ORIGINALS} ${WORKINGDIR}
		@cp ${FAKES}/fake_gateway.py ${WORKINGDIR}
		@cp ${FAKES}/fake_ozwnetwork.py ${WORKINGDIR}
		@rm ${WORKINGDIR}/remoniproject/test_application.py
		@rm -r ${WORKINGDIR}/remoniproject/__pycache__/
		@echo "Done Building!"
		
test:
		@echo ""
		@echo ""
		@echo "Testing using Unittest Framework"
		@cd ./Debug; python -m unittest -v tests_multisensor.py
		
clean:	
		@echo ""
		@echo ""
		@rm -r ./Debug
		@echo "Done cleaning up!"