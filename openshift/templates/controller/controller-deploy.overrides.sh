_includeFile=$(type -p overrides.inc)
if [ ! -z ${_includeFile} ]; then
  . ${_includeFile}
else
  _red='\033[0;31m'; _yellow='\033[1;33m'; _nc='\033[0m'; echo -e \\n"${_red}overrides.inc could not be found on the path.${_nc}\n${_yellow}Please ensure the openshift-developer-tools are installed on and registered on your path.${_nc}\n${_yellow}https://github.com/BCDevOps/openshift-developer-tools${_nc}"; exit 1;
fi

# ======================================================
# Special Deployment Parameters needed for DB Deployment
# ------------------------------------------------------
# The results need to be encoded as OpenShift template
# parameters for use with oc process.
# ======================================================

if createOperation; then
  # Randomly generate an api-key without asking ...
  readParameter "CONTROLLER_API_KEY - Please provide the key for the controller REST APIS.  If left blank, a 32 character long base64 encoded value will be randomly generated using openssl:" CONTROLLER_API_KEY $(generateKey 32) "false"
else
  # Secrets are removed from the configurations during update operations ...
  printStatusMsg "Update operation detected ...\nSkipping the prompts for CONTROLLER_API_KEY secret ... \n"
  writeParameter "CONTROLLER_API_KEY" "prompt_skipped" "false"
fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}