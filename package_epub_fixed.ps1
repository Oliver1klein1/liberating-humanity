# Remove existing files if they exist
if (Test-Path "temp.zip") {
    Remove-Item "temp.zip"
}
if (Test-Path "liberating-humanity.epub") {
    Remove-Item "liberating-humanity.epub"
}

# Create ZIP file with mimetype first (no compression)
Compress-Archive -Path "epub/mimetype" -DestinationPath "temp.zip" -CompressionLevel NoCompression

# Add the rest of the files with compression
$files = Get-ChildItem -Path "epub" -Exclude "mimetype" -Recurse
foreach ($file in $files) {
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\epub\", "")
    Compress-Archive -Path $file.FullName -Update -DestinationPath "temp.zip"
}

# Rename to .epub
Rename-Item -Path "temp.zip" -NewName "liberating-humanity.epub"

Write-Host "EPUB file created successfully!"