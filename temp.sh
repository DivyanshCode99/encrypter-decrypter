#!/bin/bash

echo "# Encrypter Decrypter" >> README.md
git init
git add README.md
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/DivyanshCode99/encrypter-decrypter.git
git push -u origin main
