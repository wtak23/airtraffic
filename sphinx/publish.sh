#!/usr/bin/env bash
#=============================================================================#
# do all the make at once
#=============================================================================#
rsync -r build/html/ build_published
touch build_published/.nojekyll
