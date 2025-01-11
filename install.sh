#!/bin/bash
echo deactivating
if [[ "$VIRTUAL_ENV" == "" ]]; then
deactivate
fi
echo installing dependencies
poetry sync
echo creating symlink
sudo ln -sfn $PWD/bin/web_valueist /usr/bin/web_valueist
echo making web_valueist executable
chmod +x /usr/bin/web_valueist