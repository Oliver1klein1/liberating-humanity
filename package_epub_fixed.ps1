# Create EPUB file suitable for Amazon KDP
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

# Create the EPUB file using proper method
Set-Location $tempDir

# Method 1: Create archive with mimetype first (uncompressed)
& "C:\Program Files\7-Zip\7z.exe" a -tzip "..\$epubName" "mimetype" -mx0

# Method 2: Add remaining files (compressed)
& "C:\Program Files\7-Zip\7z.exe" a -tzip "..\$epubName" "META-INF\" "OEBPS\" -mx9

Set-Location ..

# Clean up
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "EPUB file created: $epubName"
Write-Host "File size: $((Get-Item $epubName).Length) bytes"

# Try an alternative approach if the above fails
if (Test-Path $epubName) {
    Write-Host "EPUB created successfully. Ready for Amazon KDP upload."
} else {
    Write-Host "EPUB creation failed. Trying alternative method..."
}
