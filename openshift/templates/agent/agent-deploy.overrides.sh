_includeFile=$(type -p overrides.inc)
if [ ! -z ${_includeFile} ]; then
  . ${_includeFile}
else
  _red='\033[0;31m'; _yellow='\033[1;33m'; _nc='\033[0m'; echo -e \\n"${_red}overrides.inc could not be found on the path.${_nc}\n${_yellow}Please ensure the openshift-developer-tools are installed on and registered on your path.${_nc}\n${_yellow}https://github.com/BCDevOps/openshift-developer-tools${_nc}"; exit 1;
fi

# ================================================================================================================
# Special deployment parameters needed for injecting a user supplied settings into the deployment configuration
# ----------------------------------------------------------------------------------------------------------------

if createOperation; then
  # Ask the user to supply the sensitive parameters ...
  readParameter "ADMIN_API_KEY - Please provide the key for the agent's Admin API.  If left blank, a 32 character long base64 encoded value will be randomly generated using openssl:" ADMIN_API_KEY $(generateKey 32) "false"
  readParameter "WALLET_KEY - Please provide the wallet encryption key for the environment.  If left blank, a 48 character long base64 encoded value will be randomly generated using openssl:" WALLET_KEY $(generateKey) "false"
  readParameter "WALLET_SEED - Please provide the indy wallet seed for the environment.  If left blank, a seed will be randomly generated using openssl:" WALLET_SEED $(generateSeed) "false"
  readParameter "WALLET_DID - Please provide the indy wallet did for the environment.  The default is an empty string:" WALLET_DID "" "false"
else
  # Secrets are removed from the configurations during update operations ...
  printStatusMsg "Update operation detected ...\nSkipping the prompts for ADMIN_API_KEY, WALLET_KEY, WALLET_SEED, and WALLET_DID secrets ... \n"
  writeParameter "ADMIN_API_KEY" "prompt_skipped" "false"
  writeParameter "WALLET_KEY" "prompt_skipped" "false"
  writeParameter "WALLET_SEED" "prompt_skipped" "false"
  writeParameter "WALLET_DID" "prompt_skipped" "false"
fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}