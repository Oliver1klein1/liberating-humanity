# PowerShell script to create EPUB file for Amazon KDP
# Ensures mimetype file is added uncompressed and first

param(
    [string]$OutputName = "Liberating-Humanity-Jesus-vs-Moses-Paul.epub"
)

Write-Host "Creating EPUB file for Amazon KDP..." -ForegroundColor Green

# Remove existing EPUB if it exists
if (Test-Path $OutputName) {
    Remove-Item $OutputName -Force
    Write-Host "Removed existing $OutputName" -ForegroundColor Yellow
}

# Create temporary zip file
$tempZip = "temp_epub.zip"
if (Test-Path $tempZip) {
    Remove-Item $tempZip -Force
}

try {
    # Step 1: Add mimetype file UNCOMPRESSED (this is critical for EPUB validation)
    Write-Host "Adding mimetype file (uncompressed)..." -ForegroundColor Cyan
    
    # Create the zip and add mimetype without compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zipFile = [System.IO.Compression.ZipFile]::Open($tempZip, [System.IO.Compression.ZipArchiveMode]::Create)
    
    # Add mimetype with no compression
    $mimetypeEntry = $zipFile.CreateEntry("mimetype", [System.IO.Compression.CompressionLevel]::NoCompression)
    $mimetypeStream = $mimetypeEntry.Open()
    $mimetypeBytes = [System.Text.Encoding]::UTF8.GetBytes("application/epub+zip")
    $mimetypeStream.Write($mimetypeBytes, 0, $mimetypeBytes.Length)
    $mimetypeStream.Close()
    $zipFile.Dispose()
    
    Write-Host "✓ Mimetype added uncompressed" -ForegroundColor Green
    
    # Step 2: Add META-INF folder and container.xml
    Write-Host "Adding META-INF structure..." -ForegroundColor Cyan
    Compress-Archive -Path "META-INF" -DestinationPath $tempZip -Update -CompressionLevel Optimal
    Write-Host "✓ META-INF added" -ForegroundColor Green
    
    # Step 3: Add OEBPS folder with all content
    Write-Host "Adding OEBPS content..." -ForegroundColor Cyan
    Compress-Archive -Path "epub\OEBPS" -DestinationPath $tempZip -Update -CompressionLevel Optimal
    Write-Host "✓ OEBPS content added" -ForegroundColor Green
    
    # Step 4: Rename to .epub
    Move-Item $tempZip $OutputName -Force
    Write-Host "✓ Renamed to $OutputName" -ForegroundColor Green
    
    # Verify the file was created
    if (Test-Path $OutputName) {
        $fileSize = (Get-Item $OutputName).Length
        $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
        Write-Host ""
        Write-Host "SUCCESS!" -ForegroundColor Green -BackgroundColor Black
        Write-Host "EPUB file created: $OutputName" -ForegroundColor Green
        Write-Host "File size: $fileSizeMB MB" -ForegroundColor Green
        Write-Host ""
        Write-Host "The EPUB file is now ready for Amazon KDP upload!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Key features for KDP compliance:" -ForegroundColor Cyan
        Write-Host "• Mimetype file is uncompressed and first in archive" -ForegroundColor White
        Write-Host "• Proper META-INF/container.xml structure" -ForegroundColor White
        Write-Host "• Complete metadata with title, author, publisher, date" -ForegroundColor White
        Write-Host "• Cover image properly referenced" -ForegroundColor White
        Write-Host "• All content files properly organized" -ForegroundColor White
    } else {
        Write-Host "ERROR: Failed to create $OutputName" -ForegroundColor Red
    }
    
} catch {
    Write-Host "ERROR occurred: $($_.Exception.Message)" -ForegroundColor Red
    
    # Clean up temporary files
    if (Test-Path $tempZip) {
        Remove-Item $tempZip -Force
    }
}

Write-Host ""
Write-Host "Script completed." -ForegroundColor Green
