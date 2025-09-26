# Remove existing EPUB file if it exists
if (Test-Path "liberating-humanity.epub") {
    Remove-Item "liberating-humanity.epub"
}

# Create EPUB file with mimetype first (no compression)
Compress-Archive -Path "epub/mimetype" -DestinationPath "liberating-humanity.epub" -CompressionLevel NoCompression

# Add the rest of the files with compression
$files = Get-ChildItem -Path "epub" -Exclude "mimetype" -Recurse
foreach ($file in $files) {
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\epub\", "")
    Compress-Archive -Path $file.FullName -Update -DestinationPath "liberating-humanity.epub"
}

Write-Host "EPUB file created successfully!"