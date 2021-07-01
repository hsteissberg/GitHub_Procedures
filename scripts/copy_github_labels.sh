#!/bin/bash

# This script uses the GitHub Labels REST API
# https://developer.github.com/v3/issues/labels/

# Provide a personal access token that can
# access the source and target repositories.
# This is how you authorize with the GitHub API.
# https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line
GH_TOKEN="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"

# If you use GitHub Enterprise, change this to "https://<your_domain>/api/v3"
GH_DOMAIN="https://api.github.com"

# The source repository whose labels to copy.
SRC_GH_USER="EnvironmentalSystems"
SRC_GH_REPO="ClearWater"

# The target repository to add or update labels.
TGT_GH_USER="EnvironmentalSystems"
TGT_GH_REPO="ProjectManagement"
# repos=('ACTIONS' 'ACT-ACF' 'CE-QUAL-W2' 'Contracts' 'Distribution' 'EcoFutures' 'General-Environmental-Water-Model' 'Geospatial' 'GitHub' 'HEC-HMS-WQ' 'HEC-RAS-WQ' 'HEC-ResSim-WQ' 'HEC-WAT-CE-QUAL-W2' 'Ideas-and-Communication' 'IDF' 'MiddleEastModeling' 'Papers' 'ProjectManagement' 'Proposals' 'Ras2D_to_TecPlot' 'SatelliteTools' 'Satellite-HAB-Research' 'ScreamingPlants' 'Training' 'WQ-Prototypes-and-Scripts')
TGT_GH_REPO='ACTIONS'
TGT_GH_REPO='ACT-ACF'
TGT_GH_REPO='CE-QUAL-W2'
TGT_GH_REPO='Contracts'
TGT_GH_REPO='Distribution'
TGT_GH_REPO='EcoFutures'
TGT_GH_REPO='General-Environmental-Water-Model'
TGT_GH_REPO='Geospatial'
TGT_GH_REPO='GitHub'
TGT_GH_REPO='HEC-HMS-WQ'
TGT_GH_REPO='HEC-RAS-WQ'
TGT_GH_REPO='HEC-ResSim-WQ'
TGT_GH_REPO='HEC-WAT-CE-QUAL-W2'
TGT_GH_REPO='Ideas-and-Communication'
TGT_GH_REPO='IDF'
TGT_GH_REPO='MiddleEastModeling'
TGT_GH_REPO='Papers'
TGT_GH_REPO='ProjectManagement'
TGT_GH_REPO='Proposals'
TGT_GH_REPO='Ras2D_to_TecPlot'
TGT_GH_REPO='SatelliteTools'
TGT_GH_REPO='Satellite-HAB-Research'
# TGT_GH_REPO='ScreamingPlants'
# TGT_GH_REPO='Training'
# TGT_GH_REPO='WQ-Prototypes-and-Scripts'

# ---------------------------------------------------------

# Headers used in curl commands
GH_ACCEPT_HEADER="Accept: application/vnd.github.symmetra-preview+json"
GH_AUTH_HEADER="Authorization: Bearer $GH_TOKEN"

# Bash for-loop over JSON array with jq
# https://starkandwayne.com/blog/bash-for-loop-over-json-array-using-jq/
sourceLabelsJson64=$(curl --silent -H "$GH_ACCEPT_HEADER" -H "$GH_AUTH_HEADER" "${GH_DOMAIN}/repos/${SRC_GH_USER}/${SRC_GH_REPO}/labels?per_page=100" | jq '[ .[] | { "name": .name, "color": .color, "description": .description } ]' | jq -r '.[] | @base64' )

# for each label from source repo,
# invoke github api to create or update
# the label in the target repo
for sourceLabelJson64 in $sourceLabelsJson64; do

    # base64 decode the json
    sourceLabelJson=$(echo ${sourceLabelJson64} | base64 --decode | jq -r '.')

    # for TGT_GH_REPO in $repos; do
    # try to create the label
    # POST /repos/:owner/:repo/labels { name, color, description }
    # https://developer.github.com/v3/issues/labels/#create-a-label
    createLabelResponse=$(echo $sourceLabelJson | curl --silent -X POST -d @- -H "$GH_ACCEPT_HEADER" -H "$GH_AUTH_HEADER" "${GH_DOMAIN}/repos/${TGT_GH_USER}/${TGT_GH_REPO}/labels")

    # if creation failed then the response doesn't include an id and jq returns 'null'
    createdLabelId=$(echo $createLabelResponse | jq -r '.id')

    # if label wasn't created maybe it's because it already exists, try to update it
    if [ "$createdLabelId" == "null" ]
    then
        updateLabelResponse=$(echo $sourceLabelJson | curl --silent -X PATCH -d @- -H "$GH_ACCEPT_HEADER" -H "$GH_AUTH_HEADER" ${GH_DOMAIN}/repos/${TGT_GH_USER}/${TGT_GH_REPO}/labels/$(echo $sourceLabelJson | jq -r '.name | @uri'))
        echo "Update label response:\n"$updateLabelResponse"\n"
    else
        echo "Create label response:\n"$createLabelResponse"\n"
    fi
    # done
done
