rm *.so *.py
find ../../c-modules-build -name "*.so" -exec ln -sf {} \;
find ../../c-modules-build -name "*.py" -exec ln -sf {} \;
