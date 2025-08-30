# Create the EPUB file
$epubName = "LiberatingHumanity.epub"
$tempDir = "temp_epub"

# Remove existing files
Remove-Item -Path $epubName -Force -ErrorAction SilentlyContinue
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

# Create temporary directory
New-Item -ItemType Directory -Force -Path $tempDir

# Copy mimetype first (must be first file in the archive and uncompressed)
Copy-Item -Path "mimetype" -Destination "$tempDir/mimetype"

# Copy META-INF directory
Copy-Item -Path "epub/META-INF" -Destination "$tempDir/META-INF" -Recurse

# Copy OEBPS directory
Copy-Item -Path "epub/OEBPS" -Destination "$tempDir/OEBPS" -Recurse

# Create the EPUB file
Set-Location $tempDir
& "C:\Program Files\7-Zip\7z.exe" a -tzip "..\$epubName" "mimetype" -mx0
& "C:\Program Files\7-Zip\7z.exe" a -tzip "..\$epubName" * -x!mimetype
Set-Location ..

# Clean up
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "EPUB file created: $epubName" 