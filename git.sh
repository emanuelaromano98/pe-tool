# git add .
# read -p "Enter commit message: " message

# if [ -z "$message" ]; then
#     message="update"
# fi

# git commit -m "$message"
# git push origin main

# echo "Changes committed and pushed to origin/main"


git add .
git commit -m "update"
git push origin main

echo "Changes committed and pushed to origin/main"