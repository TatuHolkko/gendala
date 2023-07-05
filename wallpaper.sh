#!/bin/bash
pushd ~/gitrepos/gendala/common/
python main.py
popd
gsettings set org.gnome.desktop.background picture-uri "file:///home/tatu/gitrepos/gendala/exports/result.png"