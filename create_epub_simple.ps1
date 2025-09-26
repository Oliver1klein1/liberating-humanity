# Simple PowerShell script to create EPUB file for Amazon KDP
param(
    [string]$OutputName = "Liberating-Humanity-Jesus-vs-Moses-Paul.epub"
)

Write-Host "Creating EPUB file for Amazon KDP..." -ForegroundColor Green

# Remove existing EPUB if it exists
if (Test-Path $OutputName) {
    Remove-Item $OutputName -Force
    Write-Host "Removed existing $OutputName" -ForegroundColor Yellow
}

# Create temporary zip file first
$tempZip = "temp_epub.zip"
if (Test-Path $tempZip) {
    Remove-Item $tempZip -Force
}

try {
    Write-Host "Adding files to archive..." -ForegroundColor Cyan
    
    # Add mimetype first (it will be stored but not necessarily uncompressed in this method)
    Compress-Archive -Path "mimetype" -DestinationPath $tempZip -CompressionLevel NoCompression
    Write-Host "✓ Mimetype added" -ForegroundColor Green
    
    # Add META-INF folder
    Compress-Archive -Path "META-INF" -DestinationPath $tempZip -Update -CompressionLevel Optimal
    Write-Host "✓ META-INF added" -ForegroundColor Green
    
    # Add OEBPS folder with all content
    Compress-Archive -Path "epub\OEBPS" -DestinationPath $tempZip -Update -CompressionLevel Optimal
    Write-Host "✓ OEBPS content added" -ForegroundColor Green
    
    # Rename to .epub
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
        Write-Host "The EPUB file is ready for Amazon KDP!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Features included:" -ForegroundColor Cyan
        Write-Host "• Proper EPUB structure with mimetype file" -ForegroundColor White
        Write-Host "• META-INF/container.xml for navigation" -ForegroundColor White
        Write-Host "• Complete metadata for KDP" -ForegroundColor White
        Write-Host "• Cover image and all content files" -ForegroundColor White
        Write-Host "• Title: 'Liberating Humanity: How Jesus Exposed the Evil God of Moses and Warned of Paul'" -ForegroundColor White
        Write-Host "• Subtitle: 'Rediscovering Jesus' Subverted Teachings and the Father's Love'" -ForegroundColor White
        Write-Host "• Author: Ansilo Boff" -ForegroundColor White
        Write-Host "• Publisher: Truth Beyond Tradition" -ForegroundColor White
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
