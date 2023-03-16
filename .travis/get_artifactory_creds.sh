#!/usr/bin/env bash

# Wiki page on Vault Integration:
# https://cicswiki.hursley.ibm.com:9443/wiki/CICS_Explorer/artifactory_vault

VAULT_ONETIME_TOKEN=$(curl -k -s --request POST --data '{"role_id":"'"$VAULT_ROLE_ID"'","secret_id":"'"$VAULT_SECRET_ID"'"}' "$VAULT_URL"/auth/approle/login | jq -r ".auth.client_token")
ARTI=$(curl -k -s --header "X-Vault-Token: $VAULT_ONETIME_TOKEN" "$VAULT_URL"/"$VAULT_PATH" | jq -r ".data.data")
export "ARTIFACTORY_USER"="$(jq -r ".user" <<<"$ARTI")"
export "ARTIFACTORY_TOKEN"="$(jq -r ".token" <<<"$ARTI")"
