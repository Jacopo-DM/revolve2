# This script will:
# 0. Instal pipreqs if not already installed.
# 1. Run the following command >> pipreqs . --mode compat --force; in the
#    current directory.
# 2. Recursively enter all the directories and subdirectories and run the above
#    command in each of them.

# Install pipreqs if not already installed
pip install pipreqs

# Recursively enter all the directories and subdirectories
for dir in $(find . -type d)
do
    # Run the command in each of the directories
    pipreqs $dir --mode no-pin --force
done