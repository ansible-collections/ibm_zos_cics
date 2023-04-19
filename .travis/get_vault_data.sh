#!/usr/bin/env bash

# Wiki page on Vault Integration:
# https://cicswiki.hursley.ibm.com:9443/wiki/CICS_Explorer/artifactory_vault

VAULT_ONETIME_TOKEN=$(curl -k -s --request POST --data '{"role_id":"'"$VAULT_ROLE_ID"'","secret_id":"'"$VAULT_SECRET_ID"'"}' "$VAULT_URL"/auth/approle/login | jq -r ".auth.client_token")
ARTI=$(curl -k -s --header "X-Vault-Token: $VAULT_ONETIME_TOKEN" "$VAULT_URL"/"$VAULT_PATH"/"artifactory" | jq -r ".data.data")
export "ARTIFACTORY_USER"="$(jq -r ".user" <<<"$ARTI")"
export "ARTIFACTORY_TOKEN"="$(jq -r ".token" <<<"$ARTI")"

PLEX=$(curl -k -s --header "X-Vault-Token: $VAULT_ONETIME_TOKEN" "$VAULT_URL"/"$VAULT_PATH"/plex2 | jq -r ".data.data")
export "CMCI_USER"="$(jq -r ".username" <<<"$PLEX")"
export "CMCI_PASS"="$(jq -r ".password" <<<"$PLEX")"

CMCI=$(curl -k -s --header "X-Vault-Token: $VAULT_ONETIME_TOKEN" "$VAULT_URL"/"$VAULT_PATH"/cmci | jq -r ".data.data")
export "CMCI_HOST"="$(jq -r ".url" <<<"$CMCI")"
export "CMCI_PORT"="$(jq -r ".port" <<<"$CMCI")"
export "CMCI_SECURE_PORT"="$(jq -r ".secure_port" <<<"$CMCI")"
export "CMCI_SCOPE"="$(jq -r ".scope" <<<"$CMCI")"
export "CMCI_REGION_1"="$(jq -r ".region_1" <<<"$CMCI")"
export "CMCI_REGION_2"="$(jq -r ".region_2" <<<"$CMCI")"
export "CMCI_CONTEXT"="$(jq -r ".context" <<<"$CMCI")"
