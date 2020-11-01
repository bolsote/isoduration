$version = (Get-Content VERSION).Trim()

git tag $version
git push --tags
