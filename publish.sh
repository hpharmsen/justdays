start_time=$(date +%s)
pip install --upgrade pip
pip install twine build
/bin/rm -f dist/*
export VERSION=`python bumpversion.py -v patch`
python -m build
twine upload dist/*
git commit -v -a -m "publish `date`"
git tag -a $VERSION -m "version $VERSION"
git push origin $VERSION
git push origin main
duration=$(($(date +%s) - start_time))
echo "${GREEN}Published in $duration secs${NC}"
echo ""
echo "run:"
echo "pip install git+https://github.com/hpharmsen/justdays@$VERSION"
echo "of:"
echo "python -m pip install --upgrade pip; pip install justdays==$VERSION"
