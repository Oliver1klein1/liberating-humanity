# HTML to PDF Printing Setup Guide

## Overview
This guide provides everything you need to create professional, print-ready PDFs from HTML files with proper styling preservation, navigation handling, and optimized layout.

## Quick Start

### 1. Use the Enhanced PDF Script
```bash
python generate_pdf_enhanced.py
```

### 2. Test with Template
Open `pdf_print_template.html` in your browser and use Ctrl+P to see how the print styles work.

### 3. Apply to Your Book
Use the same print CSS patterns in your book's HTML files.

## Required Files

### Core Scripts
- `generate_pdf_enhanced.py` - Main PDF generation script
- `pdf_print_template.html` - Example template with print CSS
- `.cursorrules_pdf` - Cursor rules for PDF generation

### Dependencies (Choose One)
- **Puppeteer** (Node.js) - Recommended
- **wkhtmltopdf** - Alternative
- **Browser print** - Manual method

## Installation

### Option 1: Puppeteer (Recommended)
```bash
# Install Node.js first
# Then install Puppeteer
npm install puppeteer
```

### Option 2: wkhtmltopdf
```bash
# Windows
# Download from: https://wkhtmltopdf.org/downloads.html

# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf
```

## Print CSS Standards

### Page Setup
```css
@media print {
    @page {
        size: 16in 9in; /* Landscape */
        margin: 1in;
    }
}
```

### Navigation Handling
```css
@media print {
    .navigation,
    .nav-link,
    nav,
    .navbar,
    .menu,
    .breadcrumb {
        display: none !important;
    }
}
```

### Content Preservation
```css
@media print {
    .bible-quote {
        /* Preserve all original styles */
        font-style: italic;
        background: #f0f4f8;
        border-left: 4px solid #4299e1;
        padding: 1.2rem 1.5rem;
        page-break-inside: avoid;
    }
}
```

## HTML File Requirements

### Required Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your Book Title</title>
    <style>
        /* Screen styles */
        body { background: #f5f5f5; }
        
        /* Print styles */
        @media print {
            @page { size: 16in 9in; margin: 1in; }
            body { background: #fff; }
            .navigation { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="navigation">
        <a href="#" class="nav-link">Navigation</a>
    </div>
    
    <div class="bible-quote">
        "Your bible quote here"<br><br>
        — Reference
    </div>
</body>
</html>
```

### Required Classes
- **Navigation**: `class="navigation"` and `class="nav-link"`
- **Bible quotes**: `class="bible-quote"`
- **Highlights**: `class="highlight"` or `class="callout"`
- **Page breaks**: `class="page-break"`

## PDF Generation Methods

### Method 1: Enhanced Script (Recommended)
```bash
python generate_pdf_enhanced.py
```
- Automatically injects print CSS
- Multiple generation methods
- Quality verification

### Method 2: Puppeteer Direct
```javascript
const puppeteer = require('puppeteer');

async function generatePDF() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.goto('file:///path/to/file.html');
    await page.pdf({
        path: 'output.pdf',
        format: 'A4',
        printBackground: true,
        margin: { top: '1in', right: '1in', bottom: '1in', left: '1in' }
    });
    
    await browser.close();
}
```

### Method 3: wkhtmltopdf
```bash
wkhtmltopdf --page-size A4 --margin-top 1in --print-media-type input.html output.pdf
```

### Method 4: Browser Print
1. Open HTML file in browser
2. Press Ctrl+P
3. Choose "Save as PDF"
4. Adjust settings as needed

## Quality Checklist

### Before PDF Generation
- [ ] Print CSS includes all required styles
- [ ] Navigation elements properly hidden
- [ ] Page breaks appropriately placed
- [ ] Images properly referenced
- [ ] Fonts and colors defined for print

### After PDF Generation
- [ ] All styling preserved and visible
- [ ] Navigation elements completely hidden
- [ ] Page breaks occur at appropriate points
- [ ] Images display correctly
- [ ] Text is readable and properly formatted
- [ ] Bible quotes display with proper styling

### PDF Quality Check
- [ ] File size reasonable (not bloated)
- [ ] Text is selectable and searchable
- [ ] Images are crisp and clear
- [ ] Page margins consistent
- [ ] Fonts render correctly
- [ ] Colors print appropriately

## Common Issues and Solutions

### Navigation Still Visible
**Problem**: Navigation elements appear in PDF
**Solution**: Ensure print CSS includes:
```css
@media print {
    .navigation, .nav-link { display: none !important; }
}
```

### Styling Lost
**Problem**: CSS styles not preserved in PDF
**Solution**: Check print CSS preserves all styles:
```css
@media print {
    .bible-quote { /* preserve all original styles */ }
}
```

### Page Breaks Awkward
**Problem**: Content breaks in wrong places
**Solution**: Use page-break properties:
```css
@media print {
    h1, h2, h3 { page-break-after: avoid; }
    p, li { page-break-inside: avoid; }
    .page-break { page-break-before: always; }
}
```

### Images Not Displaying
**Problem**: Images missing in PDF
**Solution**: Check image paths and print CSS:
```css
@media print {
    img {
        max-width: 100% !important;
        height: auto !important;
        page-break-inside: avoid;
    }
}
```

## Best Practices

### 1. Always Test Print Preview
Use browser print preview (Ctrl+P) to check layout before generating PDF.

### 2. Preserve All Styling
Ensure print CSS maintains all visual elements from screen version.

### 3. Optimize for Readability
Use appropriate font sizes, line heights, and margins for print.

### 4. Test Multiple Methods
Different PDF generators may produce different results.

### 5. Keep File Sizes Reasonable
Optimize images and fonts for print to avoid bloated PDFs.

## File Naming Conventions

### HTML Files
- `introduction.html`
- `chapter1.html`, `chapter2.html`, etc.
- `part1.html`, `part2.html`, etc.

### PDF Files
- `[BookName]_Print.pdf` - Print-ready PDF
- `[BookName]_Draft.pdf` - Draft version
- `[BookName]_Final.pdf` - Final version

## Automation Commands

### Complete PDF Workflow
```bash
# 1. Ensure print CSS is included
# 2. Generate PDF
python generate_pdf_enhanced.py

# 3. Verify quality
# Check PDF properties and content
```

### Quick Quality Check
```bash
# Check PDF properties
pdfinfo output.pdf

# Extract text to verify content
pdftotext output.pdf -
```

## Success Criteria
- ✅ All styling preserved and visible in PDF
- ✅ Navigation elements completely hidden
- ✅ Page breaks occur at appropriate points
- ✅ Images display correctly and clearly
- ✅ Text is readable and properly formatted
- ✅ Bible quotes display with proper styling
- ✅ PDF file size is reasonable
- ✅ Text is selectable and searchable

## Troubleshooting

### Script Not Working
- Check Python installation
- Verify all dependencies installed
- Ensure HTML file exists and is valid

### PDF Generation Fails
- Check error messages in console
- Verify PDF generation tool installed
- Try alternative generation method

### Quality Issues
- Use browser print preview to identify problems
- Check print CSS is properly applied
- Verify all required styles are included

Remember: **Quality over speed** - Always verify PDF output before finalizing.
